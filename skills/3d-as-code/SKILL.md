---
name: 3d-as-code
description: >
  Generate persistent, explorable 3D worlds from text or images — programmatically — with the
  World Labs Marble API. Use when the user wants to create a 3D world/scene/environment, turn a
  photo into a navigable 3D space, produce assets for Blender/Unity/Unreal/web (mesh GLB, Gaussian
  splats, 360° panorama), or build "3D as code" pipelines. Keywords: 3D world, world model, Marble,
  World Labs, text to 3D, image to 3D, gaussian splat, GLB, panorama, spatial, scene generation,
  digital twin, VR environment.
license: MIT
---

# 3D as Code — generate explorable worlds with World Labs Marble

> Text became the universal interface for software. **3D is becoming it for space.**
> A world becomes a structured, versionable artifact you can generate, inspect, export, and reuse.

Use the bundled `scripts/marble.py` (stdlib only, no install) to drive the Marble API. Requires `WORLDLABS_API_KEY` (free key + credits at https://platform.worldlabs.ai).

## The model: world as a structured artifact
A generated world is **persistent** and **exportable** — not a throwaway render:
- **mesh GLB** → drop into Blender / Unity / Unreal (geometry + collider)
- **Gaussian splats** (`.spz`, multiple resolutions) → photoreal, web-navigable rendering
- **360° panorama** → equirectangular still
- **marble_url** → explore/walk the world in the browser

## Commands
```bash
# text → world (returns an operation_id immediately)
python scripts/marble.py text "A cozy futuristic startup office, plants, warm light, city view" --name "Office"

# poll until done, then download all assets in one go
python scripts/marble.py text "<prompt>" --name "X" --wait --out ./worlds/x

# IMAGE → world (the headline capability): a photo becomes a navigable 3D space
python scripts/marble.py image https://example.com/room.jpg --prompt "keep the mood" --name "Room" --wait --out ./worlds/room
#   add --pano if the image is a 360° panorama

# inspect / fetch
python scripts/marble.py poll <operation_id>     # status + cost + progress
python scripts/marble.py get  <world_id>         # world record + asset URLs
python scripts/marble.py download <op_or_world_id> --out ./worlds/x   # grab assets (TTL-limited!)
```

## Recommended flow (the "3D as code" loop)
1. **Intent → prompt.** Describe the space (or pass an image URL). For images, the source photo's composition and mood carry into the world.
2. **Generate.** `text`/`image` → `operation_id`. Generation is async (a world takes a few minutes).
3. **Poll.** `--wait` blocks and streams progress, or `poll <id>` manually.
4. **Export.** Download `mesh.glb` for editing, splats for web/VR, panorama for stills.
5. **Iterate.** Re-generate with a tweaked prompt or a `seed` for variations — edits to intent re-"compile" the world.

## Models & cost
- `marble-1.1` (default) · `marble-1.1-plus` (higher fidelity).
- ⚠️ **Paid beyond the free credits.** A full world generation costs ~1500 credits + ~80 for the panorama. Check balance at platform.worldlabs.ai. Generate deliberately.

## ⏳ Assets expire
Downloadable asset URLs have a **limited TTL** (the world stays on your Marble account, but the direct CDN links expire within hours). **Download right after generation** — don't rely on fetching them days later.

## Combos
- **+ Blender** (`sollea-blender` / Blender MCP): import `mesh.glb`, light it, render or animate.
- **+ HyperFrames**: use a panorama/render as a backdrop in a launch video.
- **+ image-gen** (OpenRouter): generate a concept image first, host it, then `image → world`.

## Setup
`WORLDLABS_API_KEY` in the environment. No pip install — the helper is pure Python stdlib.
