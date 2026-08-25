import { advanceWorld, createWorld, worldFingerprint } from "./world-state.js";
import { projectPixel, projectPoly } from "./projections.js";
import { PixelRenderer, PolyRenderer } from "./renderers.js";

const elements = {
  entityCount: document.querySelector("[data-entity-count]"),
  exportButton: document.querySelector("[data-export]"),
  fingerprint: document.querySelector("[data-fingerprint]"),
  focus: document.querySelector("[data-focus]"),
  modeButtons: [...document.querySelectorAll("[data-mode]")],
  pixelCanvas: document.querySelector("#pixel-field"),
  pixelPanel: document.querySelector("[data-panel='pixel']"),
  playButton: document.querySelector("[data-play]"),
  polyCanvas: document.querySelector("#poly-field"),
  polyPanel: document.querySelector("[data-panel='poly']"),
  regenerateButton: document.querySelector("[data-regenerate]"),
  seed: document.querySelector("#world-seed"),
  stepButton: document.querySelector("[data-step]"),
  tick: document.querySelector("[data-tick]"),
  worldGrid: document.querySelector(".world-grid"),
};

const pixelRenderer = new PixelRenderer(elements.pixelCanvas);
const polyRenderer = new PolyRenderer(elements.polyCanvas);
let world = createWorld({ seed: elements.seed.value });
let focusCell = null;
let mode = "weave";
let timer = null;

function render() {
  const pixel = projectPixel(world);
  const poly = projectPoly(world);
  pixelRenderer.render(pixel, focusCell);
  polyRenderer.render(poly, focusCell);
  elements.tick.textContent = String(world.tick);
  elements.entityCount.textContent = String(world.entities.length);
  elements.fingerprint.textContent = worldFingerprint(world);
  elements.focus.textContent = focusCell ?? "none";
}

function setMode(nextMode) {
  mode = nextMode;
  elements.worldGrid.dataset.mode = mode;
  elements.pixelPanel.hidden = mode === "poly";
  elements.polyPanel.hidden = mode === "pixel";
  for (const button of elements.modeButtons) {
    button.setAttribute("aria-pressed", String(button.dataset.mode === mode));
  }
  requestAnimationFrame(render);
}

function stop() {
  if (timer !== null) window.clearInterval(timer);
  timer = null;
  elements.playButton.textContent = "Play heartbeat";
  elements.playButton.setAttribute("aria-pressed", "false");
}

function togglePlay() {
  if (timer !== null) {
    stop();
    return;
  }
  timer = window.setInterval(() => {
    world = advanceWorld(world);
    render();
  }, 680);
  elements.playButton.textContent = "Pause heartbeat";
  elements.playButton.setAttribute("aria-pressed", "true");
}

function regenerate() {
  stop();
  world = createWorld({ seed: elements.seed.value, width: 32, height: 24 });
  focusCell = null;
  render();
}

function exportState() {
  const payload = JSON.stringify(world, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${world.seed.replace(/[^a-z0-9_-]+/gi, "-")}-tick-${world.tick}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}

for (const button of elements.modeButtons) button.addEventListener("click", () => setMode(button.dataset.mode));
elements.regenerateButton.addEventListener("click", regenerate);
elements.stepButton.addEventListener("click", () => {
  world = advanceWorld(world);
  render();
});
elements.playButton.addEventListener("click", togglePlay);
elements.exportButton.addEventListener("click", exportState);
elements.seed.addEventListener("keydown", (event) => {
  if (event.key === "Enter") regenerate();
});
elements.pixelCanvas.addEventListener("click", (event) => {
  focusCell = pixelRenderer.pick(event);
  render();
});
elements.polyCanvas.addEventListener("click", (event) => {
  focusCell = polyRenderer.pick(event);
  render();
});
window.addEventListener("resize", render);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) stop();
});

setMode("weave");
