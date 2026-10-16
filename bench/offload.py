"""Full run outputs (raw/*.txt, debug.json) live in the private B2 bucket plyn-bench-results;
results/<run>/objects.json lists them. Standard library only; B2 Native API.

python bench/offload.py results/<run>   upload, verify SHA1, write objects.json, remove the local copies
fetch(run_dir)                          {name: text} for a run, from raw/ if present, else from B2
Credentials: B2_APPLICATION_KEY_ID, B2_APPLICATION_KEY (repository Secrets; the key cannot delete files)."""
import base64, hashlib, json, os, pathlib, sys, urllib.parse, urllib.request

BUCKET = "plyn-bench-results"

def _auth():
    kid, key = os.environ.get("B2_APPLICATION_KEY_ID"), os.environ.get("B2_APPLICATION_KEY")
    if not (kid and key):
        return None
    req = urllib.request.Request("https://api.backblazeb2.com/b2api/v4/b2_authorize_account",
                                 headers={"Authorization": "Basic " + base64.b64encode(f"{kid}:{key}".encode()).decode()})
    a = json.load(urllib.request.urlopen(req, timeout=60))
    s = a["apiInfo"]["storageApi"]
    return {"token": a["authorizationToken"], "api": s["apiUrl"], "download": s["downloadUrl"],
            "bucket_id": next(b["id"] for b in s["allowed"]["buckets"] if b["name"] == BUCKET)}

def _post(a, method, body):
    req = urllib.request.Request(f"{a['api']}/b2api/v4/{method}", data=json.dumps(body).encode(),
                                 headers={"Authorization": a["token"]})
    return json.load(urllib.request.urlopen(req, timeout=60))

def offload(run_dir):
    run = pathlib.Path(run_dir)
    files = sorted((run / "raw").glob("*.txt")) + [p for p in [run / "debug.json"] if p.exists()]
    if not files:
        return print("offload: nothing to upload in", run)
    a = _auth()
    if a is None:
        return print("offload: B2 credentials not set; outputs stay in git")
    up = _post(a, "b2_get_upload_url", {"bucketId": a["bucket_id"]})
    listing = {"bucket": BUCKET, "files": {}}
    for p in files:
        data, rel = p.read_bytes(), p.relative_to(run).as_posix()
        name, sha1 = f"{run.name}/{rel}", hashlib.sha1(data).hexdigest()
        req = urllib.request.Request(up["uploadUrl"], data=data, headers={
            "Authorization": up["authorizationToken"], "X-Bz-File-Name": urllib.parse.quote(name),
            "Content-Type": "text/plain" if p.suffix == ".txt" else "application/json", "X-Bz-Content-Sha1": sha1})
        r = json.load(urllib.request.urlopen(req, timeout=120))
        if r.get("contentSha1") != sha1 or r.get("contentLength") != len(data):
            raise RuntimeError(f"offload: verification failed for {name}")
        listing["files"][rel] = {"object": name, "size": len(data), "sha1": sha1}
    (run / "objects.json").write_text(json.dumps(listing, indent=1) + "\n")
    for p in files:
        p.unlink()
    if (run / "raw").exists() and not any((run / "raw").iterdir()):
        (run / "raw").rmdir()
    print(f"offload: {len(files)} files to b2://{BUCKET}/{run.name}/")

def fetch(run_dir):
    run = pathlib.Path(run_dir)
    if (run / "raw").exists():
        return {f.stem: f.read_text() for f in (run / "raw").glob("*.txt")}
    if not (run / "objects.json").exists():
        return {}
    a = _auth()
    if a is None:
        raise RuntimeError("raw outputs are in B2; set B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY")
    texts = {}
    for rel, o in json.loads((run / "objects.json").read_text())["files"].items():
        if rel.startswith("raw/"):
            url = f"{a['download']}/file/{BUCKET}/{urllib.parse.quote(o['object'])}"
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": a["token"]}), timeout=60).read()
            texts[pathlib.PurePosixPath(rel).stem] = data.decode()
    return texts

if __name__ == "__main__":
    offload(sys.argv[1])
