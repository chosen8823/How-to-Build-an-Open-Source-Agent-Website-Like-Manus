import test from "node:test";
import assert from "node:assert/strict";

import {
  advanceWorld,
  createWorld,
  validateWorld,
  worldFingerprint,
} from "../world-state.js";
import { projectPixel, projectPoly } from "../projections.js";

test("the same seed creates byte-equivalent world state", () => {
  const first = createWorld({ seed: "vesica-seed", width: 20, height: 14 });
  const second = createWorld({ seed: "vesica-seed", width: 20, height: 14 });

  assert.deepEqual(first, second);
  assert.equal(worldFingerprint(first), worldFingerprint(second));
});

test("a changed seed changes the generated field", () => {
  const first = createWorld({ seed: "vesica-a", width: 20, height: 14 });
  const second = createWorld({ seed: "vesica-b", width: 20, height: 14 });

  assert.notEqual(worldFingerprint(first), worldFingerprint(second));
});

test("pixel and polygon apertures preserve the same source cells", () => {
  const world = createWorld({ seed: "shared-field", width: 12, height: 10 });
  const pixel = projectPixel(world);
  const poly = projectPoly(world);

  assert.deepEqual(
    pixel.cells.map((cell) => cell.sourceCell),
    poly.cells.map((cell) => cell.sourceCell),
  );
  assert.equal(pixel.worldFingerprint, poly.worldFingerprint);
  assert.equal(pixel.entities.length, poly.entities.length);
});

test("advancing a world is deterministic and does not mutate its parent", () => {
  const parent = createWorld({ seed: "heartbeat", width: 16, height: 12 });
  const snapshot = structuredClone(parent);
  const first = advanceWorld(parent);
  const second = advanceWorld(parent);

  assert.deepEqual(parent, snapshot);
  assert.deepEqual(first, second);
  assert.equal(first.tick, parent.tick + 1);
  assert.notEqual(worldFingerprint(first), worldFingerprint(parent));
});

test("canonical world state contains finite integer values only", () => {
  const world = createWorld({ seed: "integer-field", width: 18, height: 11 });
  const result = validateWorld(world);

  assert.deepEqual(result, { ok: true, errors: [] });
  assert.doesNotThrow(() => JSON.stringify(world));
});
