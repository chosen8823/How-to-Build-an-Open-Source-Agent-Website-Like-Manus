# Sophia Procedural Field

The governing architecture is defined in
[`docs/DUDENTY_CANON_V0_1.md`](../../docs/DUDENTY_CANON_V0_1.md) with a
machine-readable companion at
[`docs/dudenty_canon_v0_1.json`](../../docs/dudenty_canon_v0_1.json). Its
origin and exact artefact identities are joined to the OPTE world-memory
cartridge by
[`docs/dudenty_canon_v0_1.seal.json`](../../docs/dudenty_canon_v0_1.seal.json).

This browser aperture renders one deterministic procedural world through two
simultaneous projections:

- an 8-bit tile field;
- a low-poly isometric field; and
- a weave mode that keeps both visible and phase-aligned.

The renderers never own or independently simulate the world. `world-state.js`
is the canonical state surface. Both projections carry the same world
fingerprint and preserve every source-cell identifier.

## Run

From the repository root:

```powershell
python -m http.server 4173 --directory frontend
```

Then open `http://localhost:4173/procedural-world/`.

Run the dependency-free tests with:

```powershell
node --test frontend/procedural-world/tests/*.test.mjs
```

## Asset policy

The first vertical slice generates its own colour field and geometry and does
not require downloaded binaries. `assets/cc0-sources.json` records three
verified CC0 source families that can later hydrate either projection without
changing canonical world state. This keeps the runtime runnable on a constrained
drive and prevents an art pack from becoming the authority over state.
