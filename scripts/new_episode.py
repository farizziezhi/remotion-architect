#!/usr/bin/env python3
"""
scripts/new_episode.py
Remotion Explainer Architect Pro - New Episode Scaffolder

Membuat kerangka episode baru (storyboard.json) berdasarkan 1 kalimat topik.
Usage:
  python scripts/new_episode.py --topic "Kenapa Mesin Espresso Butuh Tekanan 9 Bar?" --duration 60s --style taken-apart-blueprint
"""

import os
import re
import json
import argparse

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def create_scaffold(topic: str, duration: str = "60s", style: str = "taken-apart-blueprint", aspect_ratio: str = "16:9"):
    slug = slugify(topic)
    out_dir = os.path.join("episodes", slug)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "storyboard.json")

    # Template episode baru
    data = {
        "metadata": {
            "topic": topic,
            "durationMode": duration,
            "stylePreset": style,
            "aspectRatio": aspect_ratio,
            "fps": 30,
            "voice": "id-ID-ArdiNeural"
        },
        "contactSheet": {
            "totalParts": 6,
            "totalAssemblies": 3,
            "assemblies": [
                {
                    "id": "casing_outer",
                    "label": "Bodi Luar & Sasis Pelindung",
                    "assemblyGroup": "casing",
                    "geometry": "box",
                    "args": [2.2, 3.2, 1.8],
                    "basePos": [0, 0, 0],
                    "explodeOffset": [0, 3.0, 0],
                    "materialKey": "shell",
                    "isOuterShell": True
                },
                {
                    "id": "core_unit",
                    "label": "Komponen Inti Mesin",
                    "assemblyGroup": "core",
                    "geometry": "cylinder",
                    "args": [0.8, 0.8, 2.4, 32],
                    "basePos": [0, 0, 0],
                    "explodeOffset": [0, 0, 0],
                    "materialKey": "core_component"
                },
                {
                    "id": "control_module",
                    "label": "Modul Sensor & Kontrol Elektronik",
                    "assemblyGroup": "electronics",
                    "geometry": "box",
                    "args": [1.2, 0.2, 1.2],
                    "basePos": [0, 1.5, 0],
                    "explodeOffset": [2.0, 1.0, 0],
                    "materialKey": "control_bms"
                }
            ],
            "uiCards": [
                {
                    "id": "card_stages",
                    "cardType": "ThreeStageFlowCard",
                    "title": "3 Tahap Siklus Kerja",
                    "payload": {
                        "steps": ["Tahap 1: Inisiasi", "Tahap 2: Reaksi Utama", "Tahap 3: Output Daya"]
                    }
                }
            ]
        },
        "scenes": [
            {
                "id": "scene_01_hook",
                "timeSec": 0.0,
                "durationSec": 4.0,
                "rhythmTag": "AKSI",
                "narration": f"Pernahkah kamu penasaran bagaimana {topic} sebenarnya bekerja di dalamnya?",
                "highlights": ["bekerja di dalamnya"],
                "rigState": {
                    "explodeFactor": 0.0,
                    "xrayClip": 0.0,
                    "cameraPose": "iso-wide",
                    "activeCallouts": [],
                    "sfxCue": "electric_hum"
                }
            },
            {
                "id": "scene_02_xray",
                "timeSec": 4.0,
                "durationSec": 5.0,
                "rhythmTag": "AKSI",
                "narration": "Jika kita belah casing luarnya, ada komponen utama yang bekerja dalam presisi tinggi.",
                "highlights": ["belah casing", "presisi tinggi"],
                "rigState": {
                    "explodeFactor": 0.2,
                    "xrayClip": 0.8,
                    "cameraPose": "iso-wide",
                    "activeCallouts": ["casing_outer"],
                    "sfxCue": "whoosh_xray"
                }
            },
            {
                "id": "scene_03_explode",
                "timeSec": 9.0,
                "durationSec": 6.0,
                "rhythmTag": "FOKUS",
                "narration": "Saat kita bongkar seluruh rakitannya, terlihat bagaimana tiap bagian saling terhubung.",
                "highlights": ["bongkar seluruh rakitan"],
                "rigState": {
                    "explodeFactor": 1.0,
                    "xrayClip": 0.0,
                    "cameraPose": "iso-tight",
                    "activeCallouts": ["core_unit", "control_module"],
                    "sfxCue": "servo_explode"
                }
            }
        ]
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Episode baru berhasil dibuat di: {out_file}")
    print(f"     Langkah selanjutnya:")
    print(f"     1. Sesuaikan narasi atau part 3D jika diperlukan.")
    print(f"     2. Generate audio:")
    print(f"        python scripts/generate_voice_and_sfx.py --storyboard {out_file} --output-dir ./public")
    print(f"     3. Render video:")
    print(f"        npx remotion render ExplainerMain out/{slug}.mp4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new episode scaffold")
    parser.add_argument("--topic", required=True, help="1-sentence topic or question")
    parser.add_argument("--duration", default="60s", choices=["60s", "90s", "120s"])
    parser.add_argument("--style", default="taken-apart-blueprint")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"])

    args = parser.parse_args()
    create_scaffold(args.topic, args.duration, args.style, args.aspect_ratio)

