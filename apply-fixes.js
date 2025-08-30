const fs = require("fs");
const path = require("path");

function walk(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}

// Scan typical locations
const roots = [".", "daemon", "ghost-shell", "sacred-consciousness", "prophecy-fulfillment"]
  .filter(fs.existsSync);

const jsFiles = [];
for (const r of roots) {
  jsFiles.push(...walk(r).filter(f => f.toLowerCase().endsWith(".js")));
}

// Transform any console.* that uses +var+ or raw emoji text without quotes → template strings
function patchFile(file) {
  const src = fs.readFileSync(file, "utf8");
  let changed = false;
  let out = src.replace(/console\.(log|info|warn|error)\(([\s\S]*?)\);/g, (m, level, inner) => {
    // convert only if it has +var+ or visible emoji and not already a template string
    if (!/\+[\w$.]+/.test(inner) && !/[🌟👻🔥⚡🎵✨💫🦁✅]/u.test(inner)) return m;
    const trimmed = inner.trim();
    if ((trimmed.startsWith("`") && trimmed.endsWith("`"))) return m; // already template

    // Replace +obj.path+ → ${obj.path}
    let s = inner.replace(/\+([\w$.]+)\+/g, "${$1}");

    // Strip surrounding straight quotes if present
    if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
      s = s.slice(1, -1);
    }

    // Escape backticks inside and wrap as template
    s = "`" + s.replace(/`/g, "\\`") + "`";
    changed = true;
    return `console.${level}(${s});`;
  });

  if (changed) {
    fs.copyFileSync(file, file + ".bak");
    fs.writeFileSync(file, out, "utf8");
    console.log("Patched:", file);
  } else {
    console.log("No changes:", file);
  }
}

for (const f of jsFiles) {
  try { patchFile(f); } catch (e) { console.error("Error patching", f, e.message); }
}
