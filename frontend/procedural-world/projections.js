import { worldFingerprint } from "./world-state.js";

const PALETTE = Object.freeze({
  "deep-water": { pixel: "#142b5f", top: "#183a78", side: "#0c1c3f" },
  water: { pixel: "#2366a8", top: "#2c7cc3", side: "#17466f" },
  sand: { pixel: "#e2c27a", top: "#ecd58f", side: "#a78345" },
  meadow: { pixel: "#72b04a", top: "#89c65b", side: "#44752d" },
  forest: { pixel: "#28653d", top: "#347c4d", side: "#183c25" },
  stone: { pixel: "#77798f", top: "#9395a9", side: "#4a4c5d" },
  snow: { pixel: "#dce8ee", top: "#f4fbff", side: "#91a7b2" },
});

const ENTITY_COLOURS = Object.freeze({
  beacon: "#ffd166",
  mycelium: "#e27cff",
  seed: "#ff8f4c",
  wanderer: "#76f7ff",
});

function sharedProjection(world, aperture) {
  return {
    aperture,
    entities: world.entities.map((entity) => ({
      ...entity,
      colour: ENTITY_COLOURS[entity.kind] ?? "#ffffff",
      sourceCell: `${entity.x}:${entity.y}`,
    })),
    height: world.height,
    seed: world.seed,
    tick: world.tick,
    width: world.width,
    worldFingerprint: worldFingerprint(world),
  };
}

export function projectPixel(world) {
  return {
    ...sharedProjection(world, "pixel-grid-v1"),
    cells: world.tiles.map((tile) => ({
      colour: PALETTE[tile.biome].pixel,
      elevation: tile.elevation,
      sourceCell: tile.sourceCell,
      x: tile.x,
      y: tile.y,
    })),
  };
}

export function projectPoly(world) {
  return {
    ...sharedProjection(world, "low-poly-isometric-v1"),
    cells: world.tiles.map((tile) => ({
      elevation: tile.elevation,
      sideColour: PALETTE[tile.biome].side,
      sourceCell: tile.sourceCell,
      topColour: PALETTE[tile.biome].top,
      x: tile.x,
      y: tile.y,
    })),
  };
}
