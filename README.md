# Remotion Explainer Architect Pro 🎬📐

[![GitHub Repo](https://img.shields.io/badge/GitHub-farizziezhi%2Fremotion--architect-blue?logo=github)](https://github.com/farizziezhi/remotion-architect)
[![Agent Skill](https://img.shields.io/badge/Type-Agent%20Skill-purple)](SKILL.md)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Remotion Three](https://img.shields.io/badge/Remotion-Three.js-orange)](https://remotion.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Agent Skill Resmi untuk Perancangan Seri Video Explainer Motion Graphics & Anatomi 3D Berbasis Remotion + Three.js (`@remotion/three`).**

`remotion-explainer-architect-pro` adalah **Agent Skill** (berstandar Antigravity / Agent Skills Specification) yang memberikan kemampuan kepada AI Coding Assistant untuk merancang, membuat storyboard, menyintesis audio, dan mengonstruksi video edukasi teknis berkualitas tinggi (*gaya Joni Bongkar, ZackD CGI, & Taken Apart Blueprint*).

---

## 📁 Struktur Skill (Pure Agent Skill Standard)

```text
remotion-explainer-architect-pro/
├── SKILL.md                          # Instruksi inti & SOP sistem produksi untuk AI
├── README.md                         # Dokumentasi panduan penggunaan skill
├── episode.schema.json               # Kontrak JSON Schema validasi storyboard & rig
├── .gitignore                        # Konfigurasi file yang diabaikan git
├── references/                       # Knowledge base teknis untuk AI
│   ├── remotion-composition-rig.md   # Boilerplate & aturan emas Three.js deterministik
│   └── threejs-exploded-rig.md       # Preset token desain, material, & PartSpec 3D
├── scripts/                          # Tooling otomasi audio & generator
│   ├── generate_voice_and_sfx.py     # Generator voiceover Edge-TTS & WAV SFX prosedural
│   └── new_episode.py                # Generator kerangka storyboard episode baru
└── examples/                         # Contoh implementasi storyboard nyata
    ├── battery-thermal-runaway/      # Contoh 1: Baterai Sepeda Listrik (Format 16:9)
    │   └── storyboard.json
    └── asal-usul-kota-palu/          # Contoh 2: Asal Usul Nama Kota Palu (Format 9:16)
        └── storyboard.json
```

---

## 🏛️ 5 Pilar Sistem Produksi Skill Ini

1. **Reusable Visual & 3D Object Library**: Library komponen parametrik Three.js (`<CylinderCellAssembly />`, `<FluidPumpAndBoiler3D />`, dll.) dan Kartu UI 2D (`<ThreeStageFlowCard />`, `<ComparisonVerdictCard />`, dll.).
2. **Audio-First Storyboard Schema**: Pacing berbasis tag ritme `AKSI` (gerakan cepat), `FOKUS` (penjelasan inti/zoom), dan `JEDA` (kesempatan menyerap materi).
3. **Locked Visual Presets**: Pilihan tema desain terkunci (*Taken Apart Blueprint*, *Editorial Cutaway*, *ZackD CGI*, *Dan Koe Glow*, *Comic Vector*).
4. **Declarative Animation Rigs**: Rig animasi modular Three.js murni berbasis fungsi `useCurrentFrame()` (**Zero-Delta Rule** untuk rendering tanpa stutter).
5. **One-Sentence Pipeline**: Input satu kalimat topik $\rightarrow$ AI menghasilkan Lembar Kontak 3x3, Papan Storyboard 16 Frame Kunci, audio tersinkronisasi, dan kode Remotion.

---

## 🚀 Cara Menggunakan Skill Ini

### 1. Pemasangan Skill
Tempatkan folder skill ini di direktori skills Antigravity Anda:
- **Global:** `~/.gemini/antigravity/skills/remotion-explainer-architect-pro/` atau `~/.gemini/config/skills/`
- **Workspace:** Langsung di folder proyek Anda.

### 2. Meminta AI Merancang Episode Baru
Cukup instruksikan AI Anda dengan 1 kalimat topik:
> *"Gunakan skill remotion-explainer-architect-pro untuk merancang video: Kenapa mesin espresso butuh tekanan 9 bar? Durasi 60 detik, format vertikal 9:16"*

AI akan otomatis menghasilkan:
- **Lembar Kontak (3x3 Asset Blueprint):** Katalog komponen 3D, kartu UI, dan palet material.
- **Papan Storyboard 16 Frame Kunci:** Cap waktu frame-akurat dengan tag `AKSI`, `FOKUS`, `JEDA`, serta teks dialog bersubtitel pill.
- **Storyboard JSON:** File data terstruktur sesuai `episode.schema.json`.

### 3. Generate Audio & SFX Prosedural
Jalankan skrip pembantu untuk membuat sulih suara AI berbahasa Indonesia dan 5 efek suara WAV tanpa dependensi eksternal:

```bash
# Install edge-tts jika belum ada
pip install edge-tts

# Jalankan generator audio
python scripts/generate_voice_and_sfx.py \
  --storyboard examples/asal-usul-kota-palu/storyboard.json \
  --output-dir ./public \
  --fps 30
```

Hasil kompilasi:
- `public/audio/voiceover.mp3`: Sulih suara utuh.
- `public/audio/scene_*.mp3`: Audio per-scene (anti audio-drift).
- `public/audio/*.wav`: 5 file SFX (`servo_explode`, `whoosh_xray`, `ui_pop`, `electric_hum`, `verdict_stamp`).
- `public/timeline.json`: Pemetaan frame-akurat yang siap dibaca oleh komposisi Remotion.

---

## 🎨 Preset Gaya Visual (Theme Presets)

| Preset Key | Nama Tampilan | Nuansa Visual | Jenis Kamera |
|---|---|---|---|
| `taken-apart-blueprint` | **Taken Apart Blueprint** | Kertas arsip krem (`#F2EFE9`), garis tinta teknik, HUD metadata Fig 1 | Orthographic |
| `joni-bongkar-cutaway` | **Joni Bongkar Cutaway** | Warm off-white (`#F5F2EB`), irisan cross-section, UI card data | Orthographic |
| `zackd-cgi` | **ZackD Films Macro CGI** | Dark studio PBR (`#141820`), pencahayaan dramatis, macro fly-through | Perspective |
| `dan-koe-glow` | **Dan Koe Glow Wireframe** | Obsidian void (`#07080C`), garis neon bercahaya (`#38BDF8`) | Orthographic |
| `comic-vector` | **Comic / Pop Vector** | Garis tebal kartun (`#09090B`), warna cerah pop, halftone pattern | Orthographic |

---

## 📤 Sinkronisasi ke GitHub

Untuk mengunggah skill ini ke repositori resmi Anda:

```bash
git add .
git commit -m "chore: clean up pure agent skill repository structure"
git push origin main
```

---

## 📄 Lisensi

Distributed under the MIT License. Bebas digunakan dan diperluas untuk proyek personal maupun komersial.

🔗 **Repository:** [https://github.com/farizziezhi/remotion-architect](https://github.com/farizziezhi/remotion-architect)
