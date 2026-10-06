"""Runner: prompts each model under each condition (bare | base) and start, N repetitions,
scores with the task's checks and writes results/<run>/. Hard limits: MAX_CALLS, MAX_TOKENS."""
import os, sys, json, time, difflib, itertools, importlib.util, pathlib, urllib.request, datetime
import yaml

ENDPOINT = "https://models.github.ai/inference/chat/completions"
CATALOG = "https://models.github.ai/catalog/models"
TOKEN = os.environ["GITHUB_TOKEN"]
MAX_CALLS = int(os.environ.get("MAX_CALLS", "40"))
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "700"))
PAUSE = float(os.environ.get("PAUSE", "7"))
REPS = int(os.environ.get("REPS", "3"))
TASK = os.environ.get("TASK", "meeting-actions")
BASE = os.environ.get("BASE", "minimal")
MODELS = [m.strip() for m in os.environ.get("MODELS", "openai/gpt-4.1-mini,meta/llama-3.3-70b-instruct").split(",") if m.strip()]
H = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
     "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"}

def http(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=H)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())

def catalog_ids():
    try:
        return {m["id"].lower() for m in http(CATALOG)}
    except Exception as e:
        print("catalog unavailable:", e); return None

def call(model, system, user):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    t0 = time.time()
    r = http(ENDPOINT, {"model": model, "messages": msgs, "max_tokens": MAX_TOKENS})
    dt = time.time() - t0
    return r["choices"][0]["message"]["content"] or "", r.get("usage", {}), dt

def sim(a, b):
    norm = lambda t: "\n".join(sorted(l.strip().lower() for l in t.splitlines() if l.strip()))
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    tdir = root / "tasks" / TASK
    task = yaml.safe_load((tdir / "task.yaml").read_text())
    spec = importlib.util.spec_from_file_location("checks", tdir / "checks.py"); checks = importlib.util.module_from_spec(spec); spec.loader.exec_module(checks)
    base = (root / "bases" / BASE / "base.md").read_text()
    have = catalog_ids()
    models = [m for m in MODELS if have is None or m.lower() in have]
    for m in MODELS:
        if m not in models: print("skipped, not in catalog:", m)
    if have is not None:
        print("catalog sample:", sorted(have)[:60])
    run_id = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    out = root / "results" / f"{run_id}-{TASK}"; (out / "raw").mkdir(parents=True)
    plan = list(itertools.product(models, ["bare", "base"], task["starts"].keys(), range(REPS)))
    if len(plan) > MAX_CALLS:
        print(f"plan {len(plan)} calls > MAX_CALLS {MAX_CALLS}; truncating"); plan = plan[:MAX_CALLS]
    rows = []
    for i, (model, cond, start, rep) in enumerate(plan):
        user = task["prompt"] + "\n\n" + task["notes"] + ("\n" + task["starts"][start] if task["starts"][start] else "")
        try:
            text, usage, dt = call(model, base if cond == "base" else "", user)
            err = None
        except Exception as e:
            text, usage, dt, err = "", {}, 0.0, str(e)[:300]
        res = checks.run(text) if not err else {}
        row = {"model": model, "condition": cond, "start": start, "rep": rep, "latency_s": round(dt, 2),
               "tokens": usage.get("total_tokens"), "error": err,
               "checks": {k: {"kind": v[0], "pass": v[1]} for k, v in res.items()}}
        rows.append(row)
        (out / "raw" / f"{model.replace('/', '_')}-{cond}-{start}-{rep}.txt").write_text(text or f"ERROR: {err}")
        print(i + 1, model, cond, start, rep, "err" if err else f"{sum(v[1] for v in res.values())}/{len(res)}")
        time.sleep(PAUSE)
    (out / "rows.json").write_text(json.dumps(rows, indent=1))
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
    lines += ["", "## Gain of base over bare (score), and recovery (flawed vs clean)", ""]
    for m in sorted({k[0] for k in agg}):
        for s in ["clean", "flawed"]:
            b, x = agg.get((m, "bare", s)), agg.get((m, "base", s))
            if b and x and b["score"] is not None and x["score"] is not None:
                lines.append(f"- {m}, {s}: bare {b['score']} → base {x['score']} (gain {round(x['score'] - b['score'], 2)})")
        for c in ["bare", "base"]:
            cl, fl = agg.get((m, c, "clean")), agg.get((m, c, "flawed"))
            if cl and fl and cl["score"] is not None and fl["score"] is not None:
                lines.append(f"- {m}, {c}: recovery gap {round(cl['score'] - fl['score'], 2)} (0 = full recovery)")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
