const WORLD_VERSION = "procedural-field-v1";
const BIOMES = Object.freeze(["deep-water", "water", "sand", "meadow", "forest", "stone", "snow"]);
const DIRECTIONS = Object.freeze([
  [0, -1],
  [1, 0],
  [0, 1],
  [-1, 0],
  [0, 0],
]);

function clamp(value, minimum, maximum) {
  return Math.max(minimum, Math.min(maximum, value));
}

function utf8Bytes(value) {
  return new TextEncoder().encode(String(value));
}

export function hash32(value) {
  let hash = 0x811c9dc5;
  for (const byte of utf8Bytes(value)) {
    hash ^= byte;
    hash = Math.imul(hash, 0x01000193);
  }
  return hash >>> 0;
}

function canonicalise(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalise);
  }
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalise(value[key])]),
    );
  }
  return value;
}

function deepFreeze(value) {
  if (value !== null && typeof value === "object" && !Object.isFrozen(value)) {
    Object.freeze(value);
    for (const child of Object.values(value)) {
      deepFreeze(child);
    }
  }
  return value;
}

function latticeField(seed, x, y, channel) {
  const scales = [16, 8, 4, 2];
  const weights = [8, 4, 2, 1];
  let weighted = 0;
  let totalWeight = 0;

  for (let index = 0; index < scales.length; index += 1) {
    const scale = scales[index];
    const weight = weights[index];
    const latticeX = Math.floor(x / scale);
    const latticeY = Math.floor(y / scale);
    weighted += (hash32(`${seed}:${channel}:${latticeX}:${latticeY}`) & 255) * weight;
    totalWeight += weight;
  }

  return Math.floor(weighted / totalWeight);
}

function biomeFor(elevation, moisture) {
  if (elevation < 58) return "deep-water";
  if (elevation < 88) return "water";
  if (elevation < 104) return "sand";
  if (elevation > 218) return "snow";
  if (elevation > 184) return "stone";
  if (moisture > 138) return "forest";
  return "meadow";
}

function tileAt(seed, x, y, width, height) {
  const rawElevation = latticeField(seed, x, y, "elevation");
  const moisture = latticeField(seed, x, y, "moisture");
  const edgeDistance = Math.min(x, y, width - 1 - x, height - 1 - y);
  const edgeLift = clamp(edgeDistance * 15, 0, 90);
  const elevation = clamp(rawElevation + edgeLift - 64, 0, 255);
  const biome = biomeFor(elevation, moisture);

  return {
    biome,
    elevation,
    moisture,
    sourceCell: `${x}:${y}`,
    x,
    y,
  };
}

function createEntities(seed, tiles, width, height) {
  const entities = [];
  for (const tile of tiles) {
    if (tile.biome === "deep-water" || tile.biome === "water") continue;
    const resonance = hash32(`${seed}:entity:${tile.x}:${tile.y}`);
    if (resonance % 137 !== 0) continue;
    const kinds = ["wanderer", "seed", "beacon", "mycelium"];
    entities.push({
      facing: resonance % 4,
      id: `entity:${tile.x}:${tile.y}:${resonance.toString(16)}`,
      kind: kinds[(resonance >>> 8) % kinds.length],
      phase: (resonance >>> 16) % 12,
      x: tile.x,
      y: tile.y,
    });
  }

  if (entities.length === 0) {
    const fallback = tiles.find((tile) => !tile.biome.includes("water")) ?? tiles[0];
    entities.push({
      facing: 0,
      id: `entity:${fallback.x}:${fallback.y}:origin`,
      kind: "beacon",
      phase: 0,
      x: fallback.x,
      y: fallback.y,
    });
  }

  return entities;
}

export function createWorld({ seed = "sophia-field", width = 32, height = 24 } = {}) {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 4 || height < 4) {
    throw new RangeError("World dimensions must be integers of at least four cells.");
  }

  const stableSeed = String(seed).trim() || "sophia-field";
  const tiles = [];
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      tiles.push(tileAt(stableSeed, x, y, width, height));
    }
  }

  return deepFreeze({
    entities: createEntities(stableSeed, tiles, width, height),
    height,
    seed: stableSeed,
    tick: 0,
    tiles,
    version: WORLD_VERSION,
    width,
  });
}

function tileLookup(world) {
  return new Map(world.tiles.map((tile) => [tile.sourceCell, tile]));
}

export function advanceWorld(world) {
  const validation = validateWorld(world);
  if (!validation.ok) {
    throw new TypeError(`Cannot advance invalid world: ${validation.errors.join("; ")}`);
  }

  const nextTick = world.tick + 1;
  const tilesByCell = tileLookup(world);
  const entities = world.entities.map((entity) => {
    const pulse = hash32(`${world.seed}:pulse:${nextTick}:${entity.id}`);
    const [deltaX, deltaY] = DIRECTIONS[pulse % DIRECTIONS.length];
    const nextX = clamp(entity.x + deltaX, 0, world.width - 1);
    const nextY = clamp(entity.y + deltaY, 0, world.height - 1);
    const destination = tilesByCell.get(`${nextX}:${nextY}`);
    const canMove = destination && !destination.biome.includes("water");

    return {
      ...entity,
      facing: pulse % 4,
      phase: (entity.phase + 1) % 12,
      x: canMove ? nextX : entity.x,
      y: canMove ? nextY : entity.y,
    };
  });

  return deepFreeze({ ...world, entities, tick: nextTick });
}

export function worldFingerprint(world) {
  const canonical = JSON.stringify(canonicalise(world));
  return `fnv1a32:${hash32(canonical).toString(16).padStart(8, "0")}`;
}

export function validateWorld(world) {
  const errors = [];
  if (!world || typeof world !== "object") return { ok: false, errors: ["world must be an object"] };
  if (world.version !== WORLD_VERSION) errors.push("unsupported world version");
  if (!Number.isInteger(world.width) || !Number.isInteger(world.height)) errors.push("dimensions must be integers");
  if (!Number.isInteger(world.tick) || world.tick < 0) errors.push("tick must be a non-negative integer");
  if (!Array.isArray(world.tiles) || world.tiles.length !== world.width * world.height) errors.push("tile cardinality mismatch");
  if (!Array.isArray(world.entities)) errors.push("entities must be a list");

  for (const tile of world.tiles ?? []) {
    if (!BIOMES.includes(tile.biome)) errors.push(`unknown biome at ${tile.sourceCell}`);
    for (const field of ["x", "y", "elevation", "moisture"]) {
      if (!Number.isInteger(tile[field])) errors.push(`${field} must be integer at ${tile.sourceCell}`);
    }
  }

  return { ok: errors.length === 0, errors };
}
