#!/usr/bin/env python3
"""
marble.py — minimal, dependency-free client for the World Labs Marble API ("3D as code").

Generate persistent, explorable 3D worlds from text or images, poll to completion,
and download the assets (panorama, mesh GLB, Gaussian splats).

  python marble.py text   "A mystical forest with glowing mushrooms"  --name forest
  python marble.py image  https://example.com/room.jpg  --prompt "cozy loft"  --name loft
  python marble.py poll   <operation_id>
  python marble.py get    <world_id>
  python marble.py download <operation_id|world_id>  --out ./worlds

Env: WORLDLABS_API_KEY  (get a key + free credits at https://platform.worldlabs.ai)
Stdlib only. stdout = JSON or human text; never secrets.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

BASE = "https://api.worldlabs.ai/marble/v1"

def _key():
    k = os.environ.get("WORLDLABS_API_KEY", "").strip()
    if not k:
        sys.exit("Set WORLDLABS_API_KEY (free key + credits at https://platform.worldlabs.ai).")
    return k

def _req(method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "WLT-Api-Key": _key(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"World Labs API HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}")

# ── generation ──────────────────────────────────────────────────────────────
def generate_text(prompt, name="", model="marble-1.1"):
    return _req("POST", "/worlds:generate", {
        "display_name": name, "model": model,
        "world_prompt": {"type": "text", "text_prompt": prompt}})

def generate_image(image_url, prompt="", name="", model="marble-1.1", is_pano=False):
    ip = {"source": "uri", "uri": image_url}
    if is_pano:
        ip["is_pano"] = True
    wp = {"type": "image", "image_prompt": ip}
    if prompt:
        wp["text_prompt"] = prompt
    return _req("POST", "/worlds:generate", {"display_name": name, "model": model, "world_prompt": wp})

def get_operation(op_id):
    return _req("GET", f"/operations/{op_id}")

def get_world(world_id):
    return _req("GET", f"/worlds/{world_id}")

def wait(op_id, interval=10, timeout=600):
    """Poll an operation until done. Returns the final operation dict."""
    start = time.time()
    while True:
        op = get_operation(op_id)
        if op.get("done"):
            return op
        if time.time() - start > timeout:
            sys.exit(f"Timed out after {timeout}s (operation still running: {op_id}).")
        prog = (op.get("metadata") or {}).get("progress", {})
        print(f"  … {prog.get('status','RUNNING')} — {prog.get('description','')}", file=sys.stderr)
        time.sleep(interval)

# ── assets ──────────────────────────────────────────────────────────────────
def _flatten_assets(world):
    """Return a {label: url} map of downloadable assets from a world response."""
    a = world.get("assets", {}) or {}
    out = {}
    if a.get("thumbnail_url"): out["thumbnail.jpg"] = a["thumbnail_url"]
    pano = (a.get("imagery") or {}).get("pano_url")
    if pano: out["panorama.jpg"] = pano
    mesh = (a.get("mesh") or {}).get("collider_mesh_url")
    if mesh: out["mesh.glb"] = mesh
    for res, url in ((a.get("splats") or {}).get("spz_urls") or {}).items():
        out[f"splat_{res}.spz"] = url
    return out

def download(world, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    assets = _flatten_assets(world)
    if not assets:
        sys.exit("No assets found (world may be expired — assets have a limited TTL).")
    for fname, url in assets.items():
        req = urllib.request.Request(url, headers={"WLT-Api-Key": _key()})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            open(os.path.join(out_dir, fname), "wb").write(data)
            print(f"  ✓ {fname} ({len(data)//1024} KB)")
        except urllib.error.HTTPError as e:
            print(f"  ✗ {fname}: HTTP {e.code}", file=sys.stderr)
    # write a metadata sidecar
    meta = {"world_id": world.get("world_id"), "display_name": world.get("display_name"),
            "caption": world.get("assets", {}).get("caption"),
            "marble_url": "https://marble.worldlabs.ai/world/" + str(world.get("world_id"))}
    open(os.path.join(out_dir, "world.json"), "w", encoding="utf-8").write(json.dumps(meta, indent=2, ensure_ascii=False))
    print(f"\n  Explore: {meta['marble_url']}")

def _world_from(op_or_world):
    """Accept an operation dict (with .response) or a world dict."""
    return op_or_world.get("response") or op_or_world

def main():
    ap = argparse.ArgumentParser(description="World Labs Marble — 3D worlds as code (stdlib only).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("text"); p.add_argument("prompt"); p.add_argument("--name", default=""); p.add_argument("--wait", action="store_true"); p.add_argument("--out", default="")
    p = sub.add_parser("image"); p.add_argument("image_url"); p.add_argument("--prompt", default=""); p.add_argument("--name", default=""); p.add_argument("--pano", action="store_true"); p.add_argument("--wait", action="store_true"); p.add_argument("--out", default="")
    p = sub.add_parser("poll"); p.add_argument("operation_id")
    p = sub.add_parser("get"); p.add_argument("world_id")
    p = sub.add_parser("download"); p.add_argument("id"); p.add_argument("--out", default="./world")
    args = ap.parse_args()

    if args.cmd in ("text", "image"):
        op = generate_text(args.prompt, args.name) if args.cmd == "text" \
             else generate_image(args.image_url, args.prompt, args.name, is_pano=args.pano)
        oid = op["operation_id"]
        print(f"operation_id: {oid}", file=sys.stderr)
        if args.wait:
            op = wait(oid)
            if op.get("error"):
                sys.exit(f"Generation failed: {op['error']}")
            world = _world_from(op)
            print(json.dumps({"world_id": world.get("world_id"),
                              "marble_url": "https://marble.worldlabs.ai/world/" + str(world.get("world_id"))}, indent=2))
            if args.out:
                download(world, args.out)
        else:
            print(json.dumps({"operation_id": oid}, indent=2))
    elif args.cmd == "poll":
        print(json.dumps(get_operation(args.operation_id), indent=2, ensure_ascii=False))
    elif args.cmd == "get":
        print(json.dumps(get_world(args.world_id), indent=2, ensure_ascii=False))
    elif args.cmd == "download":
        # try as operation first, then as world
        try:
            world = _world_from(get_operation(args.id))
        except SystemExit:
            world = get_world(args.id)
        download(world, args.out)

if __name__ == "__main__":
    main()
