# Three.js Exploded Anatomy & Style Presets Reference (`@remotion/three`)

Use these reusable patterns when generating interactive 3D previews or `@remotion/three` production files for `remotion-explainer-architect-pro`.

## 1. Theme & Shader Preset Tokens (`theme.config.ts`)

```typescript
export type StylePresetId =
  | 'taken-apart-blueprint'
  | 'joni-bongkar-cutaway'
  | 'zackd-cgi'
  | 'dan-koe-glow'
  | 'comic-vector';

export interface ThemePreset {
  id: StylePresetId;
  name: string;
  bgHex: string;
  gridColor: string;
  inkOutlineHex: string;
  cameraType: 'orthographic' | 'perspective';
  toonShading: boolean;
  wireframeGlow: boolean;
  hudStyle: 'taken-apart-fig' | 'editorial-pill' | 'minimal-cyber';
  accentPrimary: string;
  accentWarn: string;
}

export const THEME_PRESETS: Record<StylePresetId, ThemePreset> = {
  'taken-apart-blueprint': {
    id: 'taken-apart-blueprint',
    name: 'Taken Apart · 3D Isometric Blueprint',
    bgHex: '#F2EFE9',
    gridColor: '#DFDBD2',
    inkOutlineHex: '#1E2022',
    cameraType: 'orthographic',
    toonShading: true,
    wireframeGlow: false,
    hudStyle: 'taken-apart-fig',
    accentPrimary: '#1E8E5A',
    accentWarn: '#E87A24',
  },
  'joni-bongkar-cutaway': {
    id: 'joni-bongkar-cutaway',
    name: 'Joni Bongkar · Editorial Cutaway + UI',
    bgHex: '#F5F2EB',
    gridColor: '#E5E0D5',
    inkOutlineHex: '#18181B',
    cameraType: 'orthographic',
    toonShading: true,
    wireframeGlow: false,
    hudStyle: 'editorial-pill',
    accentPrimary: '#1E8E5A',
    accentWarn: '#E87A24',
  },
  'zackd-cgi': {
    id: 'zackd-cgi',
    name: 'ZackD Films · Macro CGI Studio',
    bgHex: '#141820',
    gridColor: '#1E2631',
    inkOutlineHex: '#000000',
    cameraType: 'perspective',
    toonShading: false,
    wireframeGlow: false,
    hudStyle: 'editorial-pill',
    accentPrimary: '#22C55E',
    accentWarn: '#F97316',
  },
  'dan-koe-glow': {
    id: 'dan-koe-glow',
    name: 'Dan Koe / Glow Sketch · High-Contrast Wireframe',
    bgHex: '#07080C',
    gridColor: '#131622',
    inkOutlineHex: '#38BDF8',
    cameraType: 'orthographic',
    toonShading: false,
    wireframeGlow: true,
    hudStyle: 'minimal-cyber',
    accentPrimary: '#38BDF8',
    accentWarn: '#F43F5E',
  },
  'comic-vector': {
    id: 'comic-vector',
    name: 'Comic / Flat Vector · Bold Pop Ink',
    bgHex: '#FFFDF7',
    gridColor: '#E8E3D5',
    inkOutlineHex: '#09090B',
    cameraType: 'orthographic',
    toonShading: true,
    wireframeGlow: false,
    hudStyle: 'editorial-pill',
    accentPrimary: '#16A34A',
    accentWarn: '#EA580C',
  },
};
```

## 2. Declarative 3D Part & Explode Rig Schema

Every 3D object in the library is defined as an array of `PartSpec` items so any machine, battery, or device can be assembled, exploded (`explodeFactor: 0 -> 1`), or sliced (`xrayClip: 0 -> 1`) automatically:

```typescript
export interface PartSpec {
  id: string;
  label: string;
  assemblyGroup: string;
  geometry: 'box' | 'cylinder' | 'torus' | 'sphere' | 'tube';
  args: number[];
  basePos: [number, number, number];
  baseRot?: [number, number, number];
  explodeOffset: [number, number, number]; // Direction & distance when explodeFactor = 1
  materialKey: 'shell' | 'structural' | 'core_component' | 'control_bms' | 'medium_fluid' | 'hazard_heat' | 'energy_current';
  isOuterShell?: boolean; // Fades or clips away when xrayClip > 0
}
```
