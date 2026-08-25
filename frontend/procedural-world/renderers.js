function canvasPoint(canvas, event) {
  const bounds = canvas.getBoundingClientRect();
  return {
    x: ((event.clientX - bounds.left) / bounds.width) * canvas.width,
    y: ((event.clientY - bounds.top) / bounds.height) * canvas.height,
  };
}

function resizeCanvas(canvas) {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = Math.max(320, Math.floor(canvas.clientWidth * ratio));
  const height = Math.max(260, Math.floor(canvas.clientHeight * ratio));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
}

export class PixelRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.context = canvas.getContext("2d", { alpha: false });
    this.layout = null;
  }

  render(projection, focusCell = null) {
    resizeCanvas(this.canvas);
    const { context, canvas } = this;
    const cellSize = Math.max(4, Math.floor(Math.min(canvas.width / projection.width, canvas.height / projection.height)));
    const fieldWidth = cellSize * projection.width;
    const fieldHeight = cellSize * projection.height;
    const offsetX = Math.floor((canvas.width - fieldWidth) / 2);
    const offsetY = Math.floor((canvas.height - fieldHeight) / 2);
    this.layout = { cellSize, offsetX, offsetY, projection };

    context.imageSmoothingEnabled = false;
    context.fillStyle = "#071018";
    context.fillRect(0, 0, canvas.width, canvas.height);

    for (const cell of projection.cells) {
      context.fillStyle = cell.colour;
      context.fillRect(offsetX + cell.x * cellSize, offsetY + cell.y * cellSize, cellSize + 1, cellSize + 1);
      if (cell.elevation > 205) {
        context.fillStyle = "rgba(255,255,255,0.18)";
        context.fillRect(offsetX + cell.x * cellSize, offsetY + cell.y * cellSize, cellSize, Math.max(1, Math.floor(cellSize / 4)));
      }
    }

    for (const entity of projection.entities) {
      const x = offsetX + entity.x * cellSize + Math.floor(cellSize / 2);
      const y = offsetY + entity.y * cellSize + Math.floor(cellSize / 2);
      const radius = Math.max(2, Math.floor(cellSize / 3));
      context.fillStyle = entity.colour;
      context.fillRect(x - radius, y - radius, radius * 2, radius * 2);
      context.fillStyle = "#071018";
      context.fillRect(x, y - radius, Math.max(1, Math.floor(radius / 2)), radius);
    }

    if (focusCell) {
      const [x, y] = focusCell.split(":").map(Number);
      context.strokeStyle = "#ffffff";
      context.lineWidth = Math.max(2, Math.floor(cellSize / 5));
      context.strokeRect(offsetX + x * cellSize + 1, offsetY + y * cellSize + 1, cellSize - 2, cellSize - 2);
    }
  }

  pick(event) {
    if (!this.layout) return null;
    const point = canvasPoint(this.canvas, event);
    const { cellSize, offsetX, offsetY, projection } = this.layout;
    const x = Math.floor((point.x - offsetX) / cellSize);
    const y = Math.floor((point.y - offsetY) / cellSize);
    if (x < 0 || y < 0 || x >= projection.width || y >= projection.height) return null;
    return `${x}:${y}`;
  }
}

function polygon(context, points, fill, stroke = null) {
  context.beginPath();
  context.moveTo(points[0].x, points[0].y);
  for (const point of points.slice(1)) context.lineTo(point.x, point.y);
  context.closePath();
  context.fillStyle = fill;
  context.fill();
  if (stroke) {
    context.strokeStyle = stroke;
    context.stroke();
  }
}

export class PolyRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.context = canvas.getContext("2d", { alpha: false });
    this.layout = null;
  }

  render(projection, focusCell = null) {
    resizeCanvas(this.canvas);
    const { canvas, context } = this;
    const tileWidth = Math.max(10, Math.floor(canvas.width / (projection.width + projection.height + 2)) * 2);
    const tileHeight = Math.max(5, Math.floor(tileWidth / 2));
    const originX = Math.floor(canvas.width / 2);
    const originY = Math.max(36, Math.floor((canvas.height - (projection.width + projection.height) * tileHeight / 2) / 2));
    const heightScale = Math.max(2, Math.floor(tileHeight / 3));
    this.layout = { heightScale, originX, originY, projection, tileHeight, tileWidth };

    const gradient = context.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, "#10152a");
    gradient.addColorStop(1, "#05070d");
    context.fillStyle = gradient;
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.lineWidth = 1;

    const sortedCells = [...projection.cells].sort((left, right) => (left.x + left.y) - (right.x + right.y) || left.y - right.y);
    for (const cell of sortedCells) {
      const centreX = originX + (cell.x - cell.y) * tileWidth / 2;
      const groundY = originY + (cell.x + cell.y) * tileHeight / 2;
      const lift = Math.floor(cell.elevation / 32) * heightScale;
      const topY = groundY - lift;
      const top = [
        { x: centreX, y: topY },
        { x: centreX + tileWidth / 2, y: topY + tileHeight / 2 },
        { x: centreX, y: topY + tileHeight },
        { x: centreX - tileWidth / 2, y: topY + tileHeight / 2 },
      ];
      const bottomY = groundY + tileHeight;
      polygon(context, [top[1], top[2], { x: centreX, y: bottomY }, { x: centreX + tileWidth / 2, y: bottomY - tileHeight / 2 }], cell.sideColour);
      polygon(context, [top[2], top[3], { x: centreX - tileWidth / 2, y: bottomY - tileHeight / 2 }, { x: centreX, y: bottomY }], cell.sideColour);
      polygon(context, top, cell.topColour, cell.sourceCell === focusCell ? "#ffffff" : "rgba(5,10,18,0.28)");
    }

    for (const entity of projection.entities) {
      const source = projection.cells[entity.y * projection.width + entity.x];
      const centreX = originX + (entity.x - entity.y) * tileWidth / 2;
      const groundY = originY + (entity.x + entity.y) * tileHeight / 2;
      const lift = Math.floor(source.elevation / 32) * heightScale;
      const radius = Math.max(3, Math.floor(tileHeight / 3));
      context.beginPath();
      context.arc(centreX, groundY - lift + tileHeight / 2 - radius, radius, 0, Math.PI * 2);
      context.fillStyle = entity.colour;
      context.fill();
    }
  }

  pick(event) {
    if (!this.layout) return null;
    const point = canvasPoint(this.canvas, event);
    const { originX, originY, projection, tileHeight, tileWidth } = this.layout;
    const relativeX = point.x - originX;
    const relativeY = point.y - originY;
    const x = Math.floor(relativeY / tileHeight + relativeX / tileWidth);
    const y = Math.floor(relativeY / tileHeight - relativeX / tileWidth);
    if (x < 0 || y < 0 || x >= projection.width || y >= projection.height) return null;
    return `${x}:${y}`;
  }
}
