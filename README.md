# Remotion Explainer Architect Pro 🎬📐

[![GitHub Repo](https://img.shields.io/badge/GitHub-farizziezhi%2Fremotion--architect-blue?logo=github)](https://github.com/farizziezhi/remotion-architect)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/farizziezhi/remotion-architect/blob/main/notebooks/remotion_colab_runner.ipynb)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Remotion Three](https://img.shields.io/badge/Remotion-Three.js-orange)](https://remotion.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistem & Workflow Produksi Terpadu untuk Seri Video Explainer Motion Graphics & Anatomi 3D Berbasis Remotion + Three.js (`@remotion/three`).**

`remotion-architect` dirancang untuk memecahkan masalah umum dalam produksi video teknis berdurasi 60–120 detik: transisi animasi yang kaku, rendering Three.js yang patah (*frame delta stutter*), serta audio AI yang sering tidak sinkron dengan visual. Sistem ini mengubah **1 kalimat topik** menjadi paket video utuh yang siap tayang di YouTube (16:9) maupun TikTok/Reels/Shorts (9:16).

---

## 📑 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Struktur Proyek](#-struktur-proyek)
- [5 Pilar Sistem Produksi](#-5-pilar-sistem-produksi)
- [Panduan Lengkap Google Colab (Step-by-Step)](#-panduan-lengkap-google-colab-step-by-step)
  - [Metode 1: 1-Click Open in Colab](#metode-1-1-click-open-in-colab)
  - [Metode 2: Setup Manual dari Kosong](#metode-2-setup-manual-dari-kosong)
  - [Metode 3: Simpan Otomatis ke Google Drive](#metode-3-simpan-otomatis-ke-google-drive)
  - [Troubleshooting & Tips Colab](#troubleshooting--tips-colab)
- [Panduan Penggunaan Lokal (PC / Mac)](#-panduan-penggunaan-lokal-pc--mac)
- [Preset Gaya Visual (Theme Presets)](#-preset-gaya-visual-theme-presets)
- [Skema & Validasi Storyboard](#-skema--validasi-storyboard)
- [Cara Push ke GitHub](#-cara-push-ke-github)
- [Lisensi](#-lisensi)

---

## ⚡ Fitur Utama

- **Aturan Emas Remotion (Zero-Delta Three.js)**: Animasi Three.js murni berbasis fungsi `useCurrentFrame()`. Bebas *stuttering* atau desinkronisasi saat rendering *headless*.
- **Synthesizer SFX Prosedural Murni**: Menghasilkan 5 sound effect mekanikal & UI (`servo_explode`, `whoosh_xray`, `ui_pop`, `electric_hum`, `verdict_stamp`) menggunakan pustaka bawaan Python (`wave`, `struct`, `math`) tanpa dependensi eksternal.
- **Sintesis Suara AI (Edge-TTS)**: Menggunakan model neural berbahasa Indonesia yang jernih (`id-ID-ArdiNeural` / `id-ID-GadisNeural`) lengkap dengan ekstraksi *Word Boundary*.
- **Pencegahan Audio Drift**: Tiap scene dihitung durasi bicaranya secara presisi dari *word boundaries* TTS, sehingga transisi `<Series.Sequence>` di Remotion selalu sinkron dengan ucapan pengisi suara.
- **Kamera & Frustum Adaptif**: Zoom kamera orthografis otomatis mengompensasi pembesaran objek saat `explodeFactor` bernilai `1.0`. Mendukung format **16:9** (YouTube) dan **9:16** (TikTok / Reels / Shorts).

---

## 📁 Struktur Proyek

```text
remotion-architect/
├── .gitignore                        # Konfigurasi file yang diabaikan git
├── SKILL.md                          # Knowledge base & panduan sistem produksi
├── README.md                         # Dokumentasi panduan lengkap
├── episode.schema.json               # Kontrak JSON Schema untuk validasi storyboard
├── notebooks/
│   └── remotion_colab_runner.ipynb   # Jupyter Notebook siap jalan di Google Colab
├── references/
│   ├── remotion-composition-rig.md   # Boilerplate implementasi Remotion + Three.js
│   └── threejs-exploded-rig.md       # Preset token gaya visual, material, & PartSpec 3D
├── scripts/
│   └── generate_voice_and_sfx.py     # Generator audio TTS & synthesizer WAV SFX
└── examples/
    └── battery-thermal-runaway/
        └── storyboard.json           # Contoh implementasi storyboard 60s
```

---

## 🏛️ 5 Pilar Sistem Produksi

1. **Reusable Visual & 3D Object Library**: Kumpulan komponen parametrik Three.js (`<CylinderCellAssembly />`, `<FluidPumpAndBoiler3D />`, `<CircuitPCBModule3D />`) dan Kartu UI 2D (`<ThreeStageFlowCard />`, `<ComparisonVerdictCard />`, `<MythStampCard />`).
2. **Audio-First Storyboard**: Pacing berbasis tag ritme `AKSI` (dinamis/cepat), `FOKUS` (penjelasan inti/zoom), dan `JEDA` (kesempatan menyerap materi).
3. **Locked Visual Presets**: Pilihan tema desain terkunci (misal: *Taken Apart Blueprint*, *Editorial Cutaway*, *ZackD CGI*, *Dan Koe Glow*).
4. **Declarative Animation Rigs**: Rig animasi modular (`useExplodeRig`, `useXRayClip`, `useWordSyncSubtitles`).
5. **One-Sentence Pipeline**: Input satu kalimat pertanyaan/topik $\rightarrow$ Output storyboard, aset audio, dan kode Remotion siap jalan.

---

## ☁️ Panduan Lengkap Google Colab (Step-by-Step)

Skrip generator audio dan timeline (`scripts/generate_voice_and_sfx.py`) **100% kompatibel dan siap dijalankan di Google Colab** tanpa memerlukan GPU berbayar (cukup runtime CPU standar gratis).

### Metode 1: 1-Click Open in Colab

Cara paling mudah adalah mengklik tombol badge berikut:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/farizziezhi/remotion-architect/blob/main/notebooks/remotion_colab_runner.ipynb)

Notebook akan langsung terbuka di akun Google Colab Anda dengan semua sel perintah yang siap dijalankan secara berurutan.

---

### Metode 2: Setup Manual dari Kosong

Jika Anda ingin membuat notebook Colab baru sendiri dari nol:

#### Langkah 1: Buka Google Colab
1. Kunjungi [colab.research.google.com](https://colab.research.google.com/).
2. Klik **New Notebook** (Notebook Baru).
3. (Opsional) Ubah nama notebook di kiri atas, misalnya menjadi `remotion_studio.ipynb`.
4. Runtime default (CPU) sudah sangat cepat untuk sintesis audio. Jika nanti ingin sekaligus me-render video Remotion, Anda bisa beralih ke GPU: **Runtime > Change runtime type > T4 GPU**.

#### Langkah 2: Clone Repository
Ketik perintah berikut di sel pertama lalu jalankan (`Shift + Enter`):

```python
# Clone repositori remotion-architect
!git clone https://github.com/farizziezhi/remotion-architect.git
%cd remotion-architect
```

#### Langkah 3: Install Dependensi TTS
Sintesis efek suara (SFX) dibuat menggunakan matematika murni tanpa paket luar. Anda hanya perlu menginstal `edge-tts`:

```python
!pip install edge-tts
```

#### Langkah 4: Jalankan Kompilasi Audio & Timeline
Jalankan script dengan menunjuk ke file storyboard:

```python
!python scripts/generate_voice_and_sfx.py \
  --storyboard examples/battery-thermal-runaway/storyboard.json \
  --output-dir ./public \
  --fps 30 \
  --voice id-ID-ArdiNeural
```

> **Pilihan Model Suara Bahasa Indonesia:**
> - `id-ID-ArdiNeural` : Suara pria, tenang, otoritatif, sangat cocok untuk sains, teknologi, dan eksplorasi mesin.
> - `id-ID-GadisNeural`: Suara wanita, energetik, ramah, cocok untuk tutorial cepat dan reels.

#### Langkah 5: Dengarkan Hasil Audio Langsung di Colab
Anda dapat langsung memutar hasil render suara dan efek suara tanpa perlu mendownload terlebih dahulu:

```python
from IPython.display import Audio, display

print("🎧 1. Full Master Voiceover:")
display(Audio("./public/audio/voiceover.mp3"))

print("🎧 2. Procedural SFX (Servo Explode):")
display(Audio("./public/audio/servo_explode.wav"))

print("🎧 3. Procedural SFX (Whoosh X-Ray):")
display(Audio("./public/audio/whoosh_xray.wav"))
```

#### Langkah 6: Download Hasil Output (`/public`)
Untuk mengambil semua file audio dan `timeline.json` ke komputer Anda:

```python
!zip -r remotion_public_assets.zip ./public
from google.colab import files
files.download("remotion_public_assets.zip")
```

Setelah diunduh, ekstrak isi zip tersebut langsung ke folder `public/` di proyek Remotion Anda.

---

### Metode 3: Simpan Otomatis ke Google Drive

Jika Anda tidak ingin mengunduh file `.zip` manual setiap kali render, sambungkan Google Drive Anda:

```python
from google.colab import drive
drive.mount('/content/drive')

# Simpan langsung ke folder di Google Drive Anda
!cp -r ./public "/content/drive/MyDrive/remotion_output"
print("Aset berhasil disalin ke Google Drive!")
```

---

### Troubleshooting & Tips Colab

1. **Jaringan Edge-TTS Timeout**: Jika koneksi ke server Microsoft TTS terputus, skrip memiliki modul *fallback* deterministik otomatis (`mock_scene_word_boundaries`). Skrip akan tetap menghasilkan file audio dan kalkulasi frame tanpa menyebabkan crash.
2. **Custom Storyboard**: Jika Anda membuat storyboard baru, Anda cukup mengunggah file `.json` Anda melalui panel file di sebelah kiri Colab, lalu ubah flag `--storyboard /content/storyboard_saya.json`.

---

## 💻 Panduan Penggunaan Lokal (PC / Mac)

### 1. Prasyarat
- Python 3.9+
- Node.js 18+ & npm / pnpm
- Proyek Remotion aktif

### 2. Sintesis Voiceover & SFX
```bash
# Clone repo
git clone https://github.com/farizziezhi/remotion-architect.git
cd remotion-architect

# Install edge-tts
pip install edge-tts

# Jalankan script kompilator
python scripts/generate_voice_and_sfx.py --storyboard examples/battery-thermal-runaway/storyboard.json --output-dir ./public --fps 30
```

Script akan menghasilkan:
- `public/audio/voiceover.mp3`: Gabungan sulih suara lengkap.
- `public/audio/scene_*.mp3`: Potongan audio per-scene untuk sinkronisasi tanpa drift.
- `public/audio/*.wav`: 5 file efek suara prosedural (`ui_pop`, `servo_explode`, `whoosh_xray`, `electric_hum`, `verdict_stamp`).
- `public/timeline.json`: Data durasi, metadata, dan *word boundaries* per frame untuk Remotion.

### 3. Setup Komposisi Remotion
Install dependensi Three.js pada proyek Remotion Anda:
```bash
npm install @remotion/three three @types/three
```

Jalankan preview interaktif di browser:
```bash
npx remotion preview
```

Render video final MP4:
```bash
npx remotion render ExplainerMain out/video.mp4
```

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

## 📋 Skema & Validasi Storyboard

Setiap episode divalidasi terhadap [`episode.schema.json`](episode.schema.json). Struktur dasarnya:

```json
{
  "metadata": {
    "topic": "Bongkar Cara Kerja Baterai Sepeda Motor Listrik",
    "durationMode": "60s",
    "stylePreset": "taken-apart-blueprint",
    "aspectRatio": "16:9",
    "fps": 30,
    "voice": "id-ID-ArdiNeural"
  },
  "contactSheet": {
    "totalParts": 18,
    "totalAssemblies": 5,
    "assemblies": [ ... ],
    "uiCards": [ ... ]
  },
  "scenes": [
    {
      "id": "scene_01_hook",
      "timeSec": 0.0,
      "durationSec": 4.0,
      "rhythmTag": "AKSI",
      "narration": "Pernahkah kamu berpikir, kenapa baterai motor listrik bisa terbakar hebat?",
      "highlights": ["terbakar hebat"],
      "rigState": {
        "explodeFactor": 0.0,
        "xrayClip": 0.0,
        "cameraPose": "iso-wide",
        "activeCallouts": [],
        "sfxCue": "electric_hum"
      }
    }
  ]
}
```

---

## 🚀 Cara Push ke GitHub

Untuk menghubungkan dan mengunggah kode dari komputer lokal Anda ke repositori GitHub:

```bash
# 1. Masuk ke direktori proyek
cd f:\skills\remotion-explainer-architect-pro

# 2. Inisialisasi Git (jika belum ada)
git init

# 3. Tambahkan semua file
git add .

# 4. Buat initial commit
git commit -m "feat: initial commit for remotion-architect system"

# 5. Set branch utama ke main
git branch -M main

# 6. Hubungkan ke repository GitHub Anda
git remote add origin https://github.com/farizziezhi/remotion-architect.git

# 7. Push ke remote repository
git push -u origin main
```

---

## 📄 Lisensi

Distributed under the MIT License. Bebas digunakan dan dimodifikasi untuk proyek personal maupun komersial.

🔗 **Repository:** [https://github.com/farizziezhi/remotion-architect](https://github.com/farizziezhi/remotion-architect)
