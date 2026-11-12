---
name: remotion-explainer-architect-pro
description: End-to-end production system and reusable workflow for Remotion + Three.js (@remotion/three) explainer and motion graphics video series (60 to 120 seconds). Turns a single-sentence topic into a complete video package using a reusable 3D/2D Visual Asset Library (Three.js exploded anatomy, cutaway primitives, UI cards), locked Theme & Style Presets (Taken Apart Blueprint, Cutaway, ZackD CGI, Dan Koe Glow, Comic/Vector), frame-accurate Storyboards with AKSI/FOKUS/JEDA pacing, edge-tts voiceover + procedural SFX generators, and declarative Remotion animation rigs. Use when the user asks to plan, storyboard, script, or build an explainer motion graphic video, 3D exploded anatomy ("bongkar"), or reusable Remotion video series.
---

# Remotion Explainer Architect Pro (v2 — System & 3D Series Engine)

A system-driven production engine for building high-retention explainer motion graphic series in **Remotion + Three.js (`@remotion/three`)**. Instead of relying on ad-hoc prompting per video, this skill enforces a **5-Pillar Reusable Production System**:
1. **Reusable Visual & 3D Object Library** (Three.js procedural primitives, exploded-view assemblies, and 2D UI cards)
2. **Audio-First Storyboard & Narration Schema** (`AKSI` / `FOKUS` / `JEDA` scene blocks + word-level highlight tokens)
3. **Locked Theme & Visual Direction Presets** (typography, semantic material palettes, shaders, camera lenses)
4. **Declarative Animation Rigs** (`useExplodeRig`, `useXRayClip`, `useFlowParticles`, `useCameraChoreography`)
5. **One-Sentence Reusable Workflow** (input 1 topic sentence -> output complete Lembar Kontak, Storyboard, Audio/SFX script, and Remotion + Three.js code)

## When to Use

- The user provides a 1-sentence topic or question (e.g., *"Kenapa mesin espresso butuh tekanan 9 bar?"*, *"Bongkar cara kerja baterai sepeda listrik"*) and wants a complete explainer video or interactive studio preview.
- The user wants to build or expand a reusable visual/3D object library, exploded anatomy animation (`TAKEN APART` style), or series template in Remotion.
- The user asks for a storyboard, asset contact sheet ("Lembar Kontak"), narration script, or `edge-tts` + SFX integration for a 60s, 90s, or 120s video.

---

## ⚡ The 3 Golden Rules of Remotion + Three.js

When implementing or generating code with this skill, strictly enforce:
1. **Deterministic Frame Animation (Zero `delta` in `useFrame`)**:
   Never use `delta` or `requestAnimationFrame` accumulators in Three.js hooks. All rotations, transforms, and shader uniforms **must** be pure deterministic functions of `frame = useCurrentFrame()`. See [references/remotion-composition-rig.md](references/remotion-composition-rig.md).
2. **Dynamic Audio Synchronization via `<Series>`**:
   Voiceover audio duration varies dynamically with AI speech synthesis (`edge-tts`). Never hardcode fixed frame durations for scenes. Always calculate `<Series.Sequence durationInFrames={Math.ceil(scene.durationSec * fps)}>` from `timeline.json`.
3. **Explode Frustum & Aspect Ratio Adaptability**:
   When `explodeFactor` reaches `1.0`, outer components expand outward. The camera zoom must scale dynamically (`interpolate(explodeProgress, [0, 1], [baseZoom, baseZoom * 0.72])`) to prevent parts from clipping outside the frame. Both `16:9` (1920x1080) and `9:16` (1080x1920 TikTok/Reels) must be supported.

---

## Pillar 1: Theme & Visual Direction Presets (`theme.config.ts`)

Always lock the visual direction at the start. If the user does not specify a style, default to **`taken-apart-blueprint`** (combining editorial contact sheets with `"Taken Apart"` Three.js exploded orthographic anatomy). See detailed tokens in [references/threejs-exploded-rig.md](references/threejs-exploded-rig.md).

1. **`taken-apart-blueprint` (3D Exploded Technical Anatomy)**
   - **Aesthetic:** Warm cream archival paper (`#F2EFE9`), crisp technical ink outlines (`#1E2022`), orthographic isometric Three.js camera, custom Cel/Toon shader with edge-detection outline pass.
   - **HUD Frame:** Corner registration marks, top metadata (`Fig 1`, `ANATOMY · [OBJECT NAME]`), bottom telemetry (`TAKEN APART`, `[X] parts · [Y] assemblies`).
   - **Typography:** Display serif/sans header + `JetBrains Mono` uppercase tracking for technical labels.

2. **`joni-bongkar-cutaway` (Editorial Cutaway + Code UI Cards)**
   - **Aesthetic:** Warm off-white (`#F5F2EB`), isometric cross-section cutaway illustrations + crisp data UI cards (`KARTU UI`), semantic **Palet Material** legend, pill-highlighted subtitles (`#1E8E5A` green / `#E87A24` orange).

3. **`zackd-cgi` (ZackD Films 3D Macro Fly-Through)**
   - **Aesthetic:** Smooth studio PBR lighting, perspective camera with aggressive macro zoom-ins through internal mechanical chambers, real-time Three.js `ClippingPlane` cross-sections, soft ambient occlusion.

4. **`dan-koe-glow` / `glow-sketch` (Minimalist High-Contrast Cyber/Mental Models)**
   - **Aesthetic:** Deep obsidian void (`#07080C`), glowing vector wireframes and neon Three.js line geometries (`#38BDF8`, `#A855F7`), kinetic dot-matrix grids.

5. **`comic-vector` (Pop Ink & Halftone Stylized)**
   - **Aesthetic:** High-contrast thick ink contours (`#09090B`), vibrant flat color fills, halftone dot overlays, dynamic comic impact action lines.

---

## Pillar 2: Reusable Visual & 3D Object Library (`assets/library.ts`)

Every episode draws from and contributes back to a modular catalog of reusable 3D assemblies (`@remotion/three` / Three.js) and 2D UI Cards:

### A. Three.js Procedural 3D Assemblies (`<ThreeCanvas />`)
Each 3D object is built as a parametric group of named sub-meshes (`parts` & `assemblies`) with an `explodeOffset: [x, y, z]` and `materialKey` adhering to [episode.schema.json](episode.schema.json):
- **`<CylinderCellAssembly />`**: Outer casing, spiral electrode core, separator membrane, top anode cap, gas vent valve (batteries, capacitors, boilers, pistons).
- **`<FluidPumpAndBoiler3D />`**: Water reservoir, copper heating coil, high-pressure boiler cylinder, portafilter/nozzle, pressure gauge, drip tray (espresso machines, hydraulic systems, cooling loops).
- **`<CircuitPCBModule3D />`**: Fiberglass board, MOSFET/IC chips, copper trace paths, LED indicator, connector cables (BMS, smartphones, IoT, power supplies).
- **`<EnclosureShell3D />`**: Top lid, side panels, internal chassis frame with automated `clipPlane` or `explodeFactor` support.

### B. Reusable 2D Code UI Cards (`KARTU UI`)
- **`<ThreeStageFlowCard />`**: 3-column progression card (e.g., `DERAS -> MELAMBAT -> BERHENTI`) with animated current/progress bar underneath.
- **`<ComparisonVerdictCard />`**: Side-by-side metric duel (`80% vs 96%`, `SEHAT vs DIPAKSA`) with animated counters and winner/loser badges.
- **`<MythStampCard />`**: Checklist summary + spring-physics rubber stamp (`MITOS` / `FAKTA` / `AMAN`).

### C. Semantic Palet Material
Every object part maps to a semantic material key rather than arbitrary colors:
- `shell` (`#B8BCC2` Abu Bodi)
- `structural` (`#2B2E33` Arang Plastik/Besi)
- `core_component` (`#3B6EE8` Biru Teknis)
- `control_bms` (`#1E8E5A` Hijau Satpam/Aman)
- `medium_fluid` (`#E8D882` Kuning Cairan/Elektrolit)
- `hazard_heat` (`#E87A24` Oranye Panas/Tembaga)
- `energy_current` (`#F5C400` Kuning Arus Listrik)

---

## Pillar 3: Duration Modes & Storyboard Pacing (`episode.schema.json`)

Support 3 locked duration tiers (default to **90s** if unspecified):

- **60s Mode (Fast Explainer — ~140 words):** 9 Lembar Kontak Panels (6 3D/Cutaway + 3 UI Cards) | **16 Keyframes** (10 `AKSI`, 4 `JEDA`, 2 `FOKUS`).
- **90s Mode (Standard Deep-Dive — ~200 words):** 10-11 Lembar Kontak Panels | **20-22 Keyframes** (13 `AKSI`, 5 `JEDA`, 4 `FOKUS`). Adds microscopic/internal sub-assembly explosion and side-by-side fault simulation.
- **120s Mode (Full Documentary Breakdown — ~280 words):** 12 Lembar Kontak Panels | **24-28 Keyframes** (16 `AKSI`, 6 `JEDA`, 6 `FOKUS`). Adds multi-culprit forensic breakdown, long-term degradation curve, and 3-step actionable solution card.

Each keyframe in the storyboard must specify:
1. **`timeSec`** and **Rhythm Tag** (`AKSI` green, `FOKUS` amber, `JEDA` neutral).
2. **`narration`**: Punchy Indonesian explainer prose with `[[highlight]]` tags around 1-2 focal words per sentence.
3. **`rigState`**: Declarative parameters driving the 3D/2D scene:
   - `explodeFactor`: `0.0` (assembled) to `1.0` (fully exploded).
   - `xrayClip`: `0.0` (solid shell) to `1.0` (full internal cutaway).
   - `cameraPose`: `[azimuth, elevation, zoom]` or preset (`"iso-wide"`, `"macro-core"`, `"top-down"`).
   - `activeCallouts`: Array of component labels to pop up with leader lines.
   - `sfxCue`: Sound trigger (`whoosh_xray`, `servo_explode`, `ui_pop`, `electric_hum`, `verdict_stamp`).

---

## Pillar 4: Declarative Animation Rigs (Remotion + Three.js)

Never animate meshes manually frame-by-frame. Bind `useCurrentFrame()` and `timeline.json` timestamps to these core rigs:

1. **`useExplodeRig(frame, triggerFrame, partOffsetVector)`**:
   Uses `spring({ frame: frame - triggerFrame, fps, config: { damping: 14, stiffness: 120 } })` to smoothly separate 3D sub-assemblies along axial vectors while updating the HUD parts counter.
2. **`useXRayClip(frame, startFrame, endFrame)`**:
   Interpolates a Three.js `THREE.Plane` clipping constant or SVG clip-path to slice open the outer shell (`UTUH` -> `TEMBUS PANDANG`).
3. **`useFlowParticles(frame, speed, pathPoints)`**:
   Animates instanced 3D spheres or SVG dashed strokes along internal conduits to visualize electricity, water pressure, heat, or gas bubbles.
4. **`useWordSyncSubtitles(frame, words)`**:
   Reads `edge-tts` `WordBoundary` timestamps to highlight spoken words in real time and trigger `<CalloutBadge />` pop-ups on exact keyword frames.

---

## Pillar 5: One-Sentence Reusable Workflow (Deliverables)

When the user gives **a single sentence topic** (or asks to build/preview an episode), automatically execute the full pipeline:

1. **Lembar Kontak (9-12 Asset Blueprint + Palet Material + 3D Part Count):**
   Define the reusable 3D assemblies (`X parts · Y assemblies`), AI cutaway prompts, and Code UI cards.
2. **Keyframe Storyboard (16-28 Frames with `AKSI` / `FOKUS` / `JEDA`):**
   Complete timestamped script with `[[highlight]]` tokens, camera choreography, and `explodeFactor` / `xrayClip` states according to [episode.schema.json](episode.schema.json).
3. **Audio & SFX Compilation:**
   Run [scripts/generate_voice_and_sfx.py](scripts/generate_voice_and_sfx.py) to synthesize:
   - `voiceover.mp3` (`id-ID-ArdiNeural` / `id-ID-GadisNeural`)
   - Procedural WAV SFX (`servo_explode.wav`, `whoosh_xray.wav`, `ui_pop.wav`, `electric_hum.wav`, `verdict_stamp.wav`)
   - `timeline.json` (mapped word boundaries + frame indices).
4. **Interactive Studio / Remotion + Three.js Project:**
   Provide ready-to-run `@remotion/three` compositions following [references/remotion-composition-rig.md](references/remotion-composition-rig.md).

