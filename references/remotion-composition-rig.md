# Remotion + Three.js Composition & Production Rig

This reference defines the production boilerplate and anti-pattern rules for rendering frame-deterministic Three.js motion graphics explainers in Remotion (`@remotion/three`).

---

## 1. The 3 Golden Rules of Remotion + Three.js

### ❌ Rule 1: Never Use Delta-Based `useFrame`
In standard Three.js games/apps, `useFrame((state, delta) => mesh.rotation.y += delta)` is common.
In Remotion, **this causes corrupt and stuttering headless renders**, because Remotion renders frame-by-frame (e.g. frame 0, frame 1, frame 2) without real-time clock pacing.

**Always drive Three.js transforms deterministically from `useCurrentFrame()`:**
```tsx
// ✅ BENAR: Pure function of frame
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const RotatingCore: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Rotasi murni berbasis frame
  const rotationY = (frame / fps) * (Math.PI / 4); // 45 deg per second

  return (
    <mesh rotation={[0, rotationY, 0]}>
      <cylinderGeometry args={[1, 1, 2, 32]} />
      <meshStandardMaterial color="#3B6EE8" />
    </mesh>
  );
};
```

---

## 2. Explode Rig with Bounding Box Camera Compensation

When `explodeFactor` goes from `0.0` to `1.0`, the assembly expands outward along each part's `explodeOffset`.
To prevent parts from clipping outside the screen, the camera's orthographic zoom must automatically compensate:

```tsx
import React, { useMemo } from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import * as THREE from 'three';
import { PartSpec } from './threejs-exploded-rig';

interface ExplodedModelProps {
  parts: PartSpec[];
  targetExplodeFactor: number; // 0.0 to 1.0
  startFrame: number;
}

export const ExplodedModel: React.FC<ExplodedModelProps> = ({ parts, targetExplodeFactor, startFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring physics for natural mechanical separation
  const explodeProgress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 14, stiffness: 120, mass: 0.8 },
  }) * targetExplodeFactor;

  return (
    <group>
      {parts.map((p) => {
        const posX = p.basePos[0] + p.explodeOffset[0] * explodeProgress;
        const posY = p.basePos[1] + p.explodeOffset[1] * explodeProgress;
        const posZ = p.basePos[2] + p.explodeOffset[2] * explodeProgress;

        return (
          <mesh key={p.id} position={[posX, posY, posZ]}>
            {p.geometry === 'cylinder' && <cylinderGeometry args={p.args as any} />}
            {p.geometry === 'box' && <boxGeometry args={p.args as any} />}
            {p.geometry === 'sphere' && <sphereGeometry args={p.args as any} />}
            <meshStandardMaterial color={resolveMaterialColor(p.materialKey)} roughness={0.3} metalness={0.2} />
          </mesh>
        );
      })}
    </group>
  );
};
```

---

## 3. Dynamic Audio & Scene Synchronization (`<Series>`)

Never hardcode scene durations in seconds when using AI narration (`edge-tts`). Read `timeline.json` and let `<Series.Sequence>` dynamically size each scene block:

```tsx
import { Composition, Series, Audio, staticFile } from 'remotion';
import timelineData from '../public/timeline.json';
import { ExplainerScene } from './ExplainerScene';

export const RemotionRoot: React.FC = () => {
  const { fps, totalFrames, aspectRatio } = timelineData.metadata;
  const isVertical = aspectRatio === '9:16';
  const width = isVertical ? 1080 : 1920;
  const height = isVertical ? 1920 : 1080;

  return (
    <>
      <Composition
        id="ExplainerMain"
        component={MainSequence}
        durationInFrames={totalFrames}
        fps={fps}
        width={width}
        height={height}
      />
    </>
  );
};

export const MainSequence: React.FC = () => {
  const { fps } = timelineData.metadata;

  return (
    <div style={{ flex: 1, backgroundColor: '#F2EFE9', position: 'relative' }}>
      {/* 1. Global Voiceover Audio Track */}
      <Audio src={staticFile('audio/voiceover.mp3')} />

      {/* 2. Audio-Synchronized Scenes */}
      <Series>
        {timelineData.scenes.map((scene) => {
          const durationInFrames = Math.ceil(scene.durationSec * fps);
          return (
            <Series.Sequence key={scene.id} durationInFrames={durationInFrames}>
              <ExplainerScene scene={scene} />
            </Series.Sequence>
          );
        })}
      </Series>
    </div>
  );
};
```

---

## 4. Responsive Viewport (16:9 Landscape vs 9:16 Vertical)

| Feature | 16:9 Widescreen (YouTube) | 9:16 Vertical (Shorts / Reels / TikTok) |
|---|---|---|
| **Resolution** | `1920 x 1080` | `1080 x 1920` |
| **Camera Zoom** | Orthographic zoom `65 - 80` | Orthographic zoom `40 - 55` |
| **Explode Vector Priority** | Horizontal & Axial (`X` and `Z`) | Vertical & Depth (`Y` and `Z`) |
| **HUD Header** | Top left (`Fig 1 · ANATOMY`) | Top center + bottom safe zone margin |
| **UI Data Cards** | Right-hand side split card | Bottom overlay sheet card |
| **Subtitles** | Lower third pill badge | Middle-lower safe zone (above TikTok UI) |

---

## 5. Audio SFX Cue Triggering

When `rigState.sfxCue` is present in a keyframe scene, render a local `<Audio />` tag at frame 0 of that sequence:

```tsx
import { Audio, staticFile } from 'remotion';

export const SceneSFX: React.FC<{ sfxCue?: string | null }> = ({ sfxCue }) => {
  if (!sfxCue) return null;
  return <Audio src={staticFile(`audio/${sfxCue}.wav`)} volume={0.7} />;
};
```

