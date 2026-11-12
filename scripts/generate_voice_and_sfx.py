#!/usr/bin/env python3
"""
generate_voice_and_sfx.py
Remotion Explainer Architect Pro - Audio & SFX Generation Engine

Generates:
1. Procedural SFX (.wav) with zero third-party dependencies (pure standard library: wave, math, struct).
2. Voiceover audio (.mp3) using edge-tts (Indonesian neural voices: id-ID-ArdiNeural / id-ID-GadisNeural).
3. Frame-accurate timeline.json mapped to Remotion frames (e.g. 30 fps) with word boundaries.

Usage:
  python generate_voice_and_sfx.py --storyboard storyboard.json --output-dir ./public/audio --fps 30
"""

import os
import sys
import math
import wave
import struct
import json
import argparse
import asyncio
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# 1. Procedural WAV SFX Synthesizer (Zero Dependencies)
# ---------------------------------------------------------------------------

SAMPLE_RATE = 44100

def _write_wav(filename: str, samples: List[float]):
    """Writes a list of normalized floats (-1.0 to 1.0) to a 16-bit mono WAV file."""
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)      # mono
        wf.setsampwidth(2)      # 16-bit
        wf.setframerate(SAMPLE_RATE)
        
        packed_data = bytearray()
        for s in samples:
            # Clamp to [-1.0, 1.0]
            val = max(-1.0, min(1.0, s))
            int_val = int(val * 32767)
            packed_data.extend(struct.pack('<h', int_val))
        wf.writeframes(packed_data)

def synth_ui_pop(filename: str):
    """Crisp UI pop / plink sound (~0.12s)"""
    duration = 0.12
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    f_start, f_end = 880.0, 1760.0  # pitch bends upward
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = i / total_samples
        # Exponential frequency sweep
        freq = f_start + (f_end - f_start) * (progress ** 0.5)
        # Fast exponential decay envelope
        env = math.exp(-35.0 * t)
        val = math.sin(2.0 * math.pi * freq * t) * env
        samples.append(val * 0.8)
    
    _write_wav(filename, samples)

def synth_servo_explode(filename: str):
    """Mechanical servo / precision actuator whirr for 3D explode (~0.35s)"""
    duration = 0.35
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    phase = 0.0
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = i / total_samples
        
        # Servo motor stepped frequencies (chirp + buzz)
        freq = 320.0 + 480.0 * math.sin(progress * math.pi)
        phase += 2.0 * math.pi * freq / SAMPLE_RATE
        
        # Square-ish harmonics for robotic mechanical feel
        fundamental = math.sin(phase)
        h3 = 0.3 * math.sin(3.0 * phase)
        h5 = 0.15 * math.sin(5.0 * phase)
        raw = fundamental + h3 + h5
        
        # Trapezoidal envelope
        attack = min(1.0, i / (0.04 * SAMPLE_RATE))
        decay = max(0.0, (total_samples - i) / (0.1 * SAMPLE_RATE))
        env = attack * min(1.0, decay)
        
        samples.append(raw * env * 0.5)
        
    _write_wav(filename, samples)

def synth_whoosh_xray(filename: str):
    """Smooth air whoosh / cutaway slice sound (~0.4s)"""
    import random
    duration = 0.4
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    # Simple resonant low-pass filtered noise
    prev_out = 0.0
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        progress = i / total_samples
        
        white_noise = (random.random() * 2.0 - 1.0)
        
        # Filter cutoff sweeps up then down
        cutoff = 0.05 + 0.35 * math.sin(progress * math.pi)
        out = prev_out + cutoff * (white_noise - prev_out)
        prev_out = out
        
        env = math.sin(progress * math.pi) ** 1.5
        samples.append(out * env * 0.9)
        
    _write_wav(filename, samples)

def synth_electric_hum(filename: str):
    """Deep electrical energy / current hum (~0.5s)"""
    duration = 0.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # 60Hz fundamental + 120Hz & 180Hz buzz
        v1 = math.sin(2.0 * math.pi * 60.0 * t)
        v2 = 0.45 * math.sin(2.0 * math.pi * 120.0 * t)
        v3 = 0.25 * math.sin(2.0 * math.pi * 180.0 * t)
        raw = v1 + v2 + v3
        
        env = math.sin((i / total_samples) * math.pi)
        samples.append(raw * env * 0.6)
        
    _write_wav(filename, samples)

def synth_verdict_stamp(filename: str):
    """Low-end mechanical impact thud for verdict stamps (~0.25s)"""
    duration = 0.25
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # Pitch drops quickly from 180Hz down to 45Hz
        freq = 45.0 + 135.0 * math.exp(-30.0 * t)
        env = math.exp(-18.0 * t)
        val = math.sin(2.0 * math.pi * freq * t) * env
        samples.append(val * 0.95)
        
    _write_wav(filename, samples)

def generate_all_sfx(sfx_dir: str) -> Dict[str, str]:
    """Generates all standard SFX library files."""
    os.makedirs(sfx_dir, exist_ok=True)
    registry = {
        "ui_pop": os.path.join(sfx_dir, "ui_pop.wav"),
        "servo_explode": os.path.join(sfx_dir, "servo_explode.wav"),
        "whoosh_xray": os.path.join(sfx_dir, "whoosh_xray.wav"),
        "electric_hum": os.path.join(sfx_dir, "electric_hum.wav"),
        "verdict_stamp": os.path.join(sfx_dir, "verdict_stamp.wav"),
    }
    
    print("[SFX] Generating procedural WAV assets...")
    synth_ui_pop(registry["ui_pop"])
    synth_servo_explode(registry["servo_explode"])
    synth_whoosh_xray(registry["whoosh_xray"])
    synth_electric_hum(registry["electric_hum"])
    synth_verdict_stamp(registry["verdict_stamp"])
    print(f"[SFX] 5 procedural SFX files successfully created in {sfx_dir}")
    return registry

# ---------------------------------------------------------------------------
# 2. Voiceover & Word Boundary Generation (edge-tts + Fallback)
# ---------------------------------------------------------------------------

async def synthesize_scene_tts(text: str, voice: str, output_mp3: str) -> List[Dict[str, Any]]:
    """Synthesize voice for a single scene and capture word boundary events."""
    import edge_tts
    
    communicate = edge_tts.Communicate(text, voice)
    word_boundaries = []
    
    with open(output_mp3, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                word_boundaries.append({
                    "text": chunk["text"],
                    "offsetSec": chunk["offset"] / 10_000_000.0,
                    "durationSec": chunk["duration"] / 10_000_000.0,
                })
                
    return word_boundaries

def mock_scene_word_boundaries(text: str, wpm: int = 150) -> List[Dict[str, Any]]:
    """Deterministic fallback word timing generator when edge-tts is offline."""
    words = text.split()
    sec_per_word = 60.0 / wpm
    boundaries = []
    current_time = 0.0
    
    for w in words:
        dur = sec_per_word * (0.8 + 0.4 * (len(w) / 6.0))
        boundaries.append({
            "text": w,
            "offsetSec": round(current_time, 3),
            "durationSec": round(dur, 3),
        })
        current_time += dur
    return boundaries

# ---------------------------------------------------------------------------
# 3. Timeline & Storyboard Compiler
# ---------------------------------------------------------------------------

def compile_timeline(storyboard_path: str, output_dir: str, fps: int = 30, voice: str = "id-ID-ArdiNeural", breath_pause_sec: float = 0.25):
    """
    Compiles a complete audio & timeline bundle for Remotion.
    Synthesizes per-scene audio to prevent audio drift across Remotion <Series.Sequence> cuts,
    as well as a consolidated voiceover.mp3.
    """
    with open(storyboard_path, 'r', encoding='utf-8') as f:
        sb_data = json.load(f)
        
    metadata = sb_data.get("metadata", {})
    # Prioritize CLI arguments if explicitly changed, otherwise prefer storyboard metadata
    actual_fps = metadata.get("fps", fps) if fps == 30 else fps
    actual_voice = metadata.get("voice", voice) if voice == "id-ID-ArdiNeural" else voice
    aspect_ratio = metadata.get("aspectRatio", sb_data.get("aspectRatio", "16:9"))

    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    # 1. Synthesize Procedural SFX
    generate_all_sfx(audio_dir)
    
    # 2. Check edge_tts availability
    has_edge_tts = False
    try:
        import edge_tts
        has_edge_tts = True
    except ImportError:
        print("[VO-Notice] 'edge-tts' not installed. Running in deterministic mock timing mode.")
        print("            To install: pip install edge-tts")
    
    # 3. Process scenes & audio synthesis
    scenes = sb_data.get("scenes", [])
    all_word_boundaries: List[Dict[str, Any]] = []
    combined_audio_bytes = bytearray()
    current_global_time = 0.0

    print(f"[VO] Compiling audio for {len(scenes)} scenes (voice: {actual_voice}, fps: {actual_fps})...")

    for idx, scene in enumerate(scenes):
        scene_id = scene.get("id", f"scene_{idx:02d}")
        narration = scene.get("narration", "").strip()
        scene_mp3_name = f"{scene_id}.mp3"
        scene_mp3_path = os.path.join(audio_dir, scene_mp3_name)
        
        scene_wb = []
        if has_edge_tts and narration:
            try:
                scene_wb = asyncio.run(synthesize_scene_tts(narration, actual_voice, scene_mp3_path))
                with open(scene_mp3_path, "rb") as f_scene:
                    combined_audio_bytes.extend(f_scene.read())
            except Exception as err:
                print(f"[VO-Warn] Failed synthesizing {scene_id} via edge-tts: {err}. Using fallback.")
                scene_wb = mock_scene_word_boundaries(narration)
                if not os.path.exists(scene_mp3_path):
                    with open(scene_mp3_path, "wb") as f_dummy:
                        f_dummy.write(b"")
        else:
            scene_wb = mock_scene_word_boundaries(narration) if narration else []
            if not os.path.exists(scene_mp3_path):
                with open(scene_mp3_path, "wb") as f_dummy:
                    f_dummy.write(b"")

        # Determine spoken duration
        if scene_wb:
            spoken_duration = scene_wb[-1]["offsetSec"] + scene_wb[-1]["durationSec"]
        else:
            spoken_duration = scene.get("durationSec", 3.0)

        # Add slight natural breathing pause at the end of each scene
        scene_duration = round(spoken_duration + breath_pause_sec, 2)
        scene_duration_frames = int(math.ceil(scene_duration * actual_fps))

        # Update scene in timeline with frame-accurate values
        scene["timeSec"] = round(current_global_time, 2)
        scene["durationSec"] = scene_duration
        scene["durationInFrames"] = scene_duration_frames
        scene["startFrame"] = int(round(current_global_time * actual_fps))
        scene["endFrame"] = scene["startFrame"] + scene_duration_frames
        scene["audioFile"] = f"audio/{scene_mp3_name}"

        # Shift word boundaries to global timeline and annotate frames
        for wb in scene_wb:
            global_offset = round(current_global_time + wb["offsetSec"], 3)
            wb_entry = {
                "text": wb["text"],
                "sceneId": scene_id,
                "localOffsetSec": wb["offsetSec"],
                "offsetSec": global_offset,
                "durationSec": wb["durationSec"],
                "startFrame": int(round(global_offset * actual_fps)),
                "endFrame": int(round((global_offset + wb["durationSec"]) * actual_fps)),
            }
            all_word_boundaries.append(wb_entry)

        current_global_time += scene_duration

    # 4. Save combined voiceover.mp3
    master_mp3_path = os.path.join(audio_dir, "voiceover.mp3")
    with open(master_mp3_path, "wb") as f_master:
        f_master.write(combined_audio_bytes)

    # 5. Output timeline.json
    timeline = {
        "metadata": {
            "fps": actual_fps,
            "totalDurationSec": round(current_global_time, 2),
            "totalFrames": int(math.ceil(current_global_time * actual_fps)),
            "voice": actual_voice,
            "aspectRatio": aspect_ratio,
            "sceneCount": len(scenes)
        },
        "wordBoundaries": all_word_boundaries,
        "scenes": scenes
    }
    
    timeline_path = os.path.join(output_dir, "timeline.json")
    with open(timeline_path, 'w', encoding='utf-8') as f_out:
        json.dump(timeline, f_out, indent=2, ensure_ascii=False)
        
    print(f"[OK] Timeline compiled successfully ({len(scenes)} scenes, {round(current_global_time, 2)}s, {int(math.ceil(current_global_time * actual_fps))} frames).")
    print(f"     Artifacts saved to {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Remotion Explainer Audio & SFX Generator")
    parser.add_argument("--storyboard", required=True, help="Path to storyboard JSON file")
    parser.add_argument("--output-dir", default="./public", help="Output directory for audio and timeline.json")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for Remotion mapping")
    parser.add_argument("--voice", default="id-ID-ArdiNeural", help="Voice model (default: id-ID-ArdiNeural)")
    
    args = parser.parse_args()
    compile_timeline(args.storyboard, args.output_dir, args.fps, args.voice)

if __name__ == "__main__":
    main()

