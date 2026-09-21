<h1 align="center">🌍 World Labs Toolkit — 3D as Code</h1>

<p align="center">
  <b>One line of text, or one photograph. Out comes a 3D world you can walk through, export to Blender, and ship to the web.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/World%20Labs-Marble%20API-6E59F7" alt="Marble">
  <img src="https://img.shields.io/badge/python-%E2%89%A53.8-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/skill-Claude%20Code%20%2F%20MCP-orange" alt="Skill">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT">
</p>

<p align="center">
  <img src="test-data/cozy-office/thumbnail.jpg" alt="A 3D world generated from one line of text" width="640">
</p>
<p align="center"><sub>👆 <i>"A cozy futuristic startup office, plants, warm light, city view"</i> — one prompt, one explorable 3D world. <a href="https://marble.worldlabs.ai/world/2c86dc39-f177-4f95-8894-dbc99389bc4b">Walk it →</a> · the real mesh and splats are in <a href="test-data/cozy-office">test-data/</a></sub></p>

**Any of 50+ [Agent Skills](https://agentskills.io) hosts — Claude Code, Codex, Cursor, Copilot, Gemini CLI:**

```
npx skills add mohamed-amine-ben-mallessa/worldlabs-toolkit -g
```

**Plain Python, no agent:**

```
git clone https://github.com/mohamed-amine-ben-mallessa/worldlabs-toolkit
```

---

> **Text became the universal interface for software. 3D is becoming it for space.**

## Why this exists

Image and video models hand you a flat frame: pretty, frozen, unusable the moment you need
another angle. A **world** is different. It's a structured, versionable artifact you can
generate, inspect, export and reuse — a mesh for Blender, Gaussian splats for the web, a
panorama, a walkable URL.

That's the **3D-as-code** idea from [World Labs](https://www.worldlabs.ai/blog/3d-as-code).
This repo packages it as a zero-dependency Python client plus an agent skill, so your agent
can build worlds the same way it writes files.

| Image/video generators | **This toolkit** |
|---|---|
| Output a flat frame | Output an **explorable 3D world** |
| Throwaway pixels | **Persistent, exportable artifact** (GLB, splats, pano) |
| Can't edit the space | Re-generate from tweaked intent — like recompiling |
| Heavy SDKs | **Pure Python stdlib**, one file |

## Quick start

```bash
# free key + credits at platform.worldlabs.ai
export WORLDLABS_API_KEY=...

# text → world, wait for it, download all assets
python scripts/marble.py text "A mystical forest with glowing mushrooms" --name Forest --wait --out worlds/forest

# the headline move — a PHOTO becomes a navigable 3D space
python scripts/marble.py image https://example.com/livingroom.jpg --name Room --wait --out worlds/room
```

You get `mesh.glb` (Blender/Unity/Unreal), `splat_*.spz` (web/VR), `panorama.jpg`, and a
`marble_url` to walk the world in the browser.

## Commands

| Command | Does |
|---|---|
| `text "<prompt>"` | text → 3D world |
| `image <url> [--prompt …] [--pano]` | image → 3D world |
| `poll <operation_id>` | status, progress, credit cost |
| `get <world_id>` | world record + asset URLs |
| `download <id> --out <dir>` | grab thumbnail + mesh + splats + metadata |

Add `--wait --out <dir>` to generate, block until done, and download in one shot.

## The exports

- **`mesh.glb`** — geometry + collider, drops straight into Blender / Unity / Unreal
- **Gaussian splats** (`.spz`, 100k → full-res) — photoreal, web-navigable
- **360° panorama** — equirectangular still
- **marble_url** — explore the world in the browser

## Install

| Surface | Install | Updates |
|---|---|---|
| **Claude Code, Codex, Cursor, Copilot, Gemini CLI, or any of 50+ [Agent Skills](https://agentskills.io) hosts** | `npx skills add mohamed-amine-ben-mallessa/worldlabs-toolkit -g` | `npx skills update 3d-as-code -g` |
| **Any MCP-style agent** | Point it at [`skills/3d-as-code/SKILL.md`](skills/3d-as-code/SKILL.md) | `git pull` |
| **Plain Python** (no agent) | `git clone https://github.com/mohamed-amine-ben-mallessa/worldlabs-toolkit` then run `scripts/marble.py` | `git pull` |

`-g` installs globally for your user, across all projects. Drop it to scope per-project.

**Requirements:** Python ≥ 3.8 (standard library only — nothing to `pip install`) and a
World Labs API key from [platform.worldlabs.ai](https://platform.worldlabs.ai).

## What's inside

```
scripts/marble.py        zero-dep client: text→world · image→world · poll · download
skills/3d-as-code/       an agent SKILL.md (Claude Code / Cursor / any MCP-style agent)
test-data/cozy-office/   a real generated world: thumbnail + mesh.glb + splats + metadata
```

The `test-data/` world is real output, committed on purpose — you can open the mesh and the
splats before spending a single credit.

## ⚠️ Read before you ship

- 💳 **Paid beyond free credits.** A world ≈ 1500 credits + ~80 for the panorama. Generate deliberately.
- ⏳ **Asset URLs expire** (limited TTL). The world stays on your Marble account, but the direct download links die within hours — **download right after generating**.
- 🖼️ **`image → world` needs a public image URL** (jpg/png/webp). Host the image somewhere reachable first.

## Combos

- **Blender** → import `mesh.glb`, light it, render or animate a fly-through.
- **HyperFrames** → use a world panorama/render as a launch-video backdrop
  ([hyperframes-free-agent](https://github.com/mohamed-amine-ben-mallessa/hyperframes-free-agent)).
- **Concept-art loop** → generate an image with any image model, host it, then `image → world`.

## Credits & links

Built on **[World Labs](https://www.worldlabs.ai)** Marble. Concept: [3D as Code](https://www.worldlabs.ai/blog/3d-as-code) · vision: [Building Spatial Intelligence](https://radical.vc/building-spatial-intelligence-how-world-labs-is-creating-the-next-frontier-in-ai/).

> Independent open-source toolkit. Not affiliated with or endorsed by World Labs. "Marble" and "World Labs" are trademarks of their owners.

## License

MIT.

---

<p align="center">
  <sub>Built by <a href="https://github.com/mohamed-amine-ben-mallessa">Mohamed Amine Ben Mallessa</a> · ⭐ star it if you generated a world you actually kept</sub>
</p>
