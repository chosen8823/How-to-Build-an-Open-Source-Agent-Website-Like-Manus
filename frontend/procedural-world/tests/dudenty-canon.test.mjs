import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";
import assert from "node:assert/strict";

const manifestUrl = new URL("../../../docs/dudenty_canon_v0_1.json", import.meta.url);
const receiptUrl = new URL("../../../docs/dudenty_canon_v0_1.receipt.json", import.meta.url);
const sealUrl = new URL("../../../docs/dudenty_canon_v0_1.seal.json", import.meta.url);
const documentUrl = new URL("../../../docs/DUDENTY_CANON_V0_1.md", import.meta.url);

function canonicalise(value) {
  if (Array.isArray(value)) return value.map(canonicalise);
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalise(value[key])]),
    );
  }
  return value;
}

function cidForBytes(bytes) {
  return `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
}

function canonicalBytes(value) {
  return Buffer.from(JSON.stringify(canonicalise(value)), "utf8");
}

async function loadJson(url) {
  return JSON.parse(await readFile(url, "utf8"));
}

test("Dudenty realm positions form one complete dozenal revolution", async () => {
  const manifest = await loadJson(manifestUrl);
  const expectedPositions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "10"];

  assert.equal(manifest.clock.radix, 12);
  assert.deepEqual(manifest.realms.map((realm) => realm.position), expectedPositions);
  assert.equal(new Set(manifest.realms.map((realm) => realm.name)).size, 12);
});

test("the geometric and functional readings preserve nineteen sites", async () => {
  const { topology } = await loadJson(manifestUrl);

  assert.equal(topology.centre_sites + topology.polar_rays + topology.realm_sites, 19);
  assert.equal(
    topology.functional_projection.inward_perceptors
      + topology.functional_projection.centred_apertures
      + topology.functional_projection.outward_generators,
    19,
  );
  assert.equal(topology.total_sites, 19);
});

test("the provenance receipt verifies the exact canon artefacts", async () => {
  const manifest = await loadJson(manifestUrl);
  const receipt = await loadJson(receiptUrl);
  const documentBytes = await readFile(documentUrl);
  const manifestBytes = canonicalBytes(manifest);
  const artifacts = Object.fromEntries(receipt.artifacts.map((artifact) => [artifact.role, artifact]));

  assert.equal(cidForBytes(documentBytes), artifacts.human_canon.cid);
  assert.equal(documentBytes.length, artifacts.human_canon.byte_length);
  assert.equal(cidForBytes(manifestBytes), artifacts.machine_canon.cid);
  assert.equal(manifestBytes.length, artifacts.machine_canon.byte_length);
  assert.equal(receipt.originator, "Ryan / IAM / chosen8823");
});

test("root and instantiation witnesses remain mandatory structural concepts", async () => {
  const manifest = await loadJson(manifestUrl);

  assert.ok(manifest.invariants.includes("root_and_instantiation_are_self_describing"));
  assert.deepEqual(manifest.parent_manifest_cids, []);
  assert.ok(manifest.root_harness_fields.includes("sacred_lineage"));
  assert.ok(manifest.root_harness_fields.includes("custodial_lineage"));
});

test("the canon seal joins artefact identity to world-memory cartridge identity", async () => {
  const receipt = await loadJson(receiptUrl);
  const seal = await loadJson(sealUrl);
  const receiptBytes = canonicalBytes(receipt);
  const artifacts = Object.fromEntries(seal.artifacts.map((artifact) => [artifact.role, artifact]));

  assert.equal(artifacts.provenance_receipt.artifact_cid, cidForBytes(receiptBytes));
  assert.equal(artifacts.provenance_receipt.identity_byte_length, receiptBytes.length);
  assert.ok(
    artifacts.provenance_receipt.cartridge_source_byte_length
      >= artifacts.provenance_receipt.identity_byte_length,
  );
  assert.equal(artifacts.human_canon.source_ref, "canon:dudenty:v0.1:human");
  assert.equal(artifacts.machine_canon.source_ref, "canon:dudenty:v0.1:machine");
  for (const artifact of seal.artifacts) {
    assert.match(artifact.cartridge_card_cid, /^sha256:[0-9a-f]{64}$/);
    assert.match(artifact.cartridge_payload_cid, /^sha256:[0-9a-f]{64}$/);
  }
});
