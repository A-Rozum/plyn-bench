"""Runner: prompts each model under each condition (bare | base) and start, N repetitions,
scores with the task's checks and writes results/<run>/. Hard limits: MAX_CALLS, MAX_TOKENS."""
import os, sys, json, urllib.error, time, difflib, itertools, importlib.util, pathlib, urllib.request, datetime
import yaml, subprocess

# Providers with OpenAI-compatible chat endpoints. Model ids are "<provider>/<model>".
PROVIDERS = {
    "gemini": {"base": "https://generativelanguage.googleapis.com/v1beta/openai", "key": "GEMINI_API_KEY"},
    "openrouter": {"base": "https://openrouter.ai/api/v1", "key": "OPENROUTER_API_KEY"},
    "zai": {"base": "https://api.z.ai/api/paas/v4", "key": "ZAI_API_KEY"},
    "groq": {"base": "https://api.groq.com/openai/v1", "key": "GROQ_API_KEY"},
    "cohere": {"base": "https://api.cohere.ai/compatibility/v1", "key": "COHERE_API_KEY"},
    "qwen": {"base": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1", "key": "QWEN_API_KEY"},
    "hf": {"base": "https://router.huggingface.co/v1", "key": "HF_API_KEY"},
    "nvidia": {"base": "https://integrate.api.nvidia.com/v1", "key": "NVIDIA_API_KEY"},
}

# Conditions: the same model three ways. "bare" and "base" run with reasoning off; "think" with it on.
CONDITIONS = [c.strip() for c in os.environ.get("CONDITIONS", "bare,think,base").split(",") if c.strip()]

def reasoning_variants(provider, on):
    """Request parameters that switch reasoning on or off, tried in order until one is accepted."""
    if provider == "gemini":
        return [{"reasoning_effort": "high"}] if on else [{"reasoning_effort": e} for e in ("none", "minimal", "low")]
    if provider == "openrouter":
        return [{"reasoning": {"effort": "high"}}] if on else [{"reasoning": {"enabled": False}}, {"reasoning": {"effort": "low"}}]
    if provider == "zai":
        return [{"thinking": {"type": "enabled"}}] if on else [{"thinking": {"type": "disabled"}}, {}]
    if provider == "groq":
        return [{"reasoning_effort": "high"}, {"reasoning_effort": "default"}] if on else [{"reasoning_effort": "none"}, {"reasoning_effort": "low"}, {}]
    if provider == "qwen":
        return [{"enable_thinking": True}] if on else [{"enable_thinking": False}, {}]
    if provider == "cohere":
        return [{"reasoning_effort": "high"}] if on else [{}]
    return [{}]
MAX_CALLS = int(os.environ.get("MAX_CALLS", "40"))
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "800"))          # reasoning off: the answer itself is short
MAX_TOKENS_THINK = int(os.environ.get("MAX_TOKENS_THINK", "4000"))  # reasoning on: room for the reasoning
PAUSE = float(os.environ.get("PAUSE", "13"))
REPS = int(os.environ.get("REPS", "2"))
TASK = os.environ.get("TASK", "meeting-actions")
BASE = os.environ.get("BASE", "minimal")
MODELS = [m.strip() for m in os.environ.get("MODELS", "gemini/gemini-3.5-flash-lite,gemini/gemini-3.5-flash").split(",") if m.strip()]

def split(model):
    prov, _, name = model.partition("/")
    return PROVIDERS[prov], name

def headers(p):
    return {"Authorization": f"Bearer {os.environ.get(p['key'], '')}", "Content-Type": "application/json",
            "User-Agent": "plyn-bench/0.1"}   # some providers' firewalls reject Python's default agent

DEBUG = []

def http(url, body=None, h=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=h or {})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read(); status = r.status; ctype = r.headers.get("Content-Type")
    except urllib.error.HTTPError as e:
        raw = e.read(); status = e.code; ctype = e.headers.get("Content-Type")
    try:
        data = json.loads(raw)
    except Exception:
        data = None
    if status >= 400 or data is None:
        DEBUG.append({"url": url, "status": status, "content_type": ctype, "body": raw[:500].decode("utf-8", "replace")})
        raise RuntimeError(f"HTTP {status}: {raw[:200]!r}")
    return data

def catalog_ids():
    ids = set()
    for name, p in PROVIDERS.items():
        if not os.environ.get(p["key"]):
            continue
        try:
            for m in http(p["base"] + "/models", h=headers(p)).get("data", []):
                ids.add(f"{name}/{m['id'].removeprefix('models/')}".lower())
        except Exception as e:
            print("catalog unavailable for", name, e)
    return ids or None

def call(model, system, user, think):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    p, name = split(model)
    prov = model.split("/", 1)[0]
    last = None
    for extra in reasoning_variants(prov, think):
        t0 = time.time()
        try:
            r = http(p["base"] + "/chat/completions", {"model": name, "messages": msgs, "max_tokens": MAX_TOKENS_THINK if think else MAX_TOKENS, **extra}, headers(p))
        except RuntimeError as e:
            last = e
            if "HTTP 400" in str(e):
                continue          # this way of switching reasoning is not accepted; try the next
            raise
        dt = time.time() - t0
        break
    else:
        raise last
    ch = r["choices"][0]
    if ch.get("finish_reason") == "length":
        raise RuntimeError("truncated: output hit MAX_TOKENS (thinking tokens count too)")
    usage = r.get("usage", {}) or {}
    meta = {"reasoning_param": extra, "served_model": r.get("model"), "served_provider": r.get("provider"),
            "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")}
    return ch["message"]["content"] or "", usage, dt, meta

def sim(a, b):
    norm = lambda t: "\n".join(sorted(l.strip().lower() for l in t.splitlines() if l.strip()))
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    tdir = root / "tasks" / TASK
    task = yaml.safe_load((tdir / "task.yaml").read_text())
    context = ''
    if task.get('context'):
        cfg = task['context']
        fixture = (tdir / cfg['repo']).resolve()
        if not fixture.is_relative_to(tdir.resolve()): raise ValueError('context fixture must be inside task directory')
        subprocess.run([sys.executable, str(root / '.system/tools/plyn_compile.py'), str(fixture),
                        *[f'{k}={v}' for k,v in cfg['facets'].items()]], check=True)
        context = (fixture / '.context/task.md').read_text()
    spec = importlib.util.spec_from_file_location("checks", tdir / "checks.py"); checks = importlib.util.module_from_spec(spec); spec.loader.exec_module(checks)
    base = (root / "bases" / BASE / "base.md").read_text()
    variants = task.get("variants")          # A/B tasks: conditions are variant names, system text per variant
    conds = list(variants) if variants else CONDITIONS
    have = catalog_ids()
    models = MODELS
    for m in MODELS:
        if have is not None and m.lower() not in have: print("not in catalog (trying anyway):", m)
    if have is not None:
        print("catalog sample:", sorted(have)[:60])
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
    (root / "results" / ".current").write_text(f"{run_id}-{TASK}")
    out = root / "results" / f"{run_id}-{TASK}"; (out / "raw").mkdir(parents=True)
    plan = list(itertools.product(models, conds, task["starts"].keys(), range(REPS)))
    if len(plan) > MAX_CALLS:
        print(f"plan {len(plan)} calls > MAX_CALLS {MAX_CALLS}; truncating"); plan = plan[:MAX_CALLS]
    rows = []
    for i, (model, cond, start, rep) in enumerate(plan):
        user = task["prompt"] + "\n\n" + task.get("notes", "") + ("\n" + task["starts"][start] if task["starts"][start] else "")
        if context: user += '\n\nCOMPILED TASK CONTEXT:\n' + context
        err = None
        for attempt in range(2):   # one retry after a pause when the provider is overloaded or rate-limited
            try:
                system = variants[cond] if variants else (base if cond == "base" else "")
                text, usage, dt, meta = call(model, system, user, cond == "think")
                err = None
                break
            except Exception as e:
                text, usage, dt, meta, err = "", {}, 0.0, {}, str(e)[:300]
                if not ("HTTP 429" in err or "HTTP 503" in err) or attempt:
                    break
                time.sleep(30)
        res = checks.run(text) if not err else {}
        row = {"model": model, "condition": cond, "start": start, "rep": rep, "latency_s": round(dt, 2),
               "tokens": usage.get("total_tokens"), "error": err, **meta,
               "checks": {k: {"kind": v[0], "pass": v[1]} for k, v in res.items()}}
        rows.append(row)
        (out / "raw" / f"{model.replace('/', '_')}-{cond}-{start}-{rep}.txt").write_text(text or f"ERROR: {err}")
        (out / "rows.json").write_text(json.dumps(rows, indent=1))   # saved after every call
        print(i + 1, model, cond, start, rep, "err" if err else f"{sum(v[1] for v in res.values())}/{len(res)}", flush=True)
        time.sleep(PAUSE)
    (out / "rows.json").write_text(json.dumps(rows, indent=1))
    (out / "debug.json").write_text(json.dumps({"catalog": sorted(x for x in have if not x.startswith("openrouter/") or x.endswith(":free")) if have else None, "http_errors": DEBUG[:10]}, indent=1))
    summarise(rows, out, run_id)

def summarise(rows, out, run_id):
    import statistics as st
    groups = {}
    for r in rows:
        if not r["error"]:
            groups.setdefault((r["model"], r["condition"], r["start"]), []).append(r)
    texts = {}
    for f in (out / "raw").glob("*.txt"):
        texts[f.stem] = f.read_text()
    lines = [f"# Run {run_id}", "", f"Task: {TASK}. Base: {BASE}. Reps: {REPS}.", "",
             "| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    agg = {}
    for (m, c, s), rs in sorted(groups.items()):
        def share(kind=None):
            vals = [v["pass"] for r in rs for v in r["checks"].values() if kind is None or v["kind"] == kind]
            return round(sum(vals) / len(vals), 2) if vals else None
        outs = [texts.get(f"{m.replace('/', '_')}-{c}-{s}-{r['rep']}", "") for r in rs]
        conv = round(st.mean(sim(a, b) for a, b in itertools.combinations(outs, 2)), 2) if len(outs) > 1 else None
        tok = round(st.mean(r["tokens"] for r in rs if r["tokens"])) if any(r["tokens"] for r in rs) else None
        lat = round(st.mean(r["latency_s"] for r in rs), 1)
        a = dict(score=share(), fidelity=share("fidelity"), boundary=share("boundary"), selectivity=share("selectivity"),
                 cleanliness=share("cleanliness"), convergence=conv, tokens=tok, latency=lat)
        agg[(m, c, s)] = a
        lines.append(f"| {m} | {c} | {s} | {len(rs)} | " + " | ".join(str(a[k]) for k in a) + " |")
    errs = [r for r in rows if r["error"]]
    if errs:
        lines += ["", f"Errors: {len(errs)}. First: {errs[0]['error']}"]
    lines += ["", "## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)", ""]
    for m in sorted({k[0] for k in agg}):
        for s in ["clean", "flawed"]:
            b = agg.get((m, "bare", s))
            for c in ["think", "base"]:
                x = agg.get((m, c, s))
                if b and x and b["score"] is not None and x["score"] is not None:
                    lines.append(f"- {m}, {s}: bare {b['score']} → {c} {x['score']} (gain {round(x['score'] - b['score'], 2)}; tokens {b['tokens']} → {x['tokens']}; latency {b['latency']} → {x['latency']} s)")
        for c in ["bare", "think", "base"]:
            cl, fl = agg.get((m, c, "clean")), agg.get((m, c, "flawed"))
            if cl and fl and cl["score"] is not None and fl["score"] is not None:
                lines.append(f"- {m}, {c}: recovery gap {round(cl['score'] - fl['score'], 2)} (0 = full recovery)")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

def summarise_dir(out):
    out = pathlib.Path(out)
    rows = json.loads((out / "rows.json").read_text())
    summarise(rows, out, out.name)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--summarise":
        summarise_dir(sys.argv[2])
    else:
        main()
