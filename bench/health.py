"""Health check: one tiny call per provider in providers.yaml. Writes results/health.md (overwritten each time)."""
import os, json, time, pathlib, datetime, urllib.request, urllib.error, yaml
import run

root = pathlib.Path(__file__).resolve().parent.parent
providers = yaml.safe_load((root / "providers.yaml").read_text())
lines = [f"# Provider health {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC", "",
         "| provider | model | status | latency s | note |", "|---|---|---|---|---|"]
for name, cfg in providers.items():
    p = run.PROVIDERS[name]
    if not os.environ.get(p["key"]):
        lines.append(f"| {name} | {cfg['model']} | no key | | |"); continue
    note = ""
    t0 = time.time()
    try:
        r = run.http(p["base"] + "/chat/completions",
                     {"model": cfg["model"], "messages": [{"role": "user", "content": "Reply with the single word OK."}], "max_tokens": 200},
                     run.headers(p))
        status = "ok" if "ok" in (r["choices"][0]["message"].get("content") or "").lower() else "answered, unexpected text"
    except Exception as e:
        status, note = "error", str(e)[:140].replace("|", "/")
        if "404" in note or "not found" in note.lower() or "does not exist" in note.lower():
            try:
                ids = [m["id"] for m in run.http(p["base"] + "/models", h=run.headers(p)).get("data", [])][:8]
                note += " — available e.g.: " + ", ".join(ids)
            except Exception:
                pass
    exp = cfg.get("expires")
    if exp and (datetime.date.fromisoformat(str(exp)) - datetime.date.today()).days < 21:
        note += f" — quota expires {exp}"
    lines.append(f"| {name} | {cfg['model']} | {status} | {time.time() - t0:.1f} | {note} |")
    time.sleep(2)
(root / "results" / "health.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
