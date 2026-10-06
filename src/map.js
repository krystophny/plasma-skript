// Interactive map of plasma models (map/index.html). The graph is drawn from
// the JSON that src/map.typ writes from map/plasma-models.yaml; the side panel
// shows the typeset entry of the selected model or reduction. Without
// JavaScript the page keeps the static figure and the full list of entries.
(() => {
  "use strict";
  const root = document.getElementById("model-map");
  const source = document.getElementById("map-data");
  if (!root || !source) return;
  const data = JSON.parse(source.textContent);
  const stage = document.getElementById("map-stage");
  const panel = document.getElementById("map-panel");
  const NS = "http://www.w3.org/2000/svg";
  const DX = 150, DY = 80, W = 136, H = 50, PAD = 40;

  const svgEl = (name, attrs = {}, parent = null) => {
    const el = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
    if (parent) parent.appendChild(el);
    return el;
  };
  const px = (p) => [p[0] * DX, p[1] * DY];
  const nodeOf = new Map(data.nodes.map((n) => [n.id, n]));

  // ------------------------------------------------------------ drawing
  const xs = data.nodes.map((n) => px(n.pos)[0]);
  const ys = data.nodes.map((n) => px(n.pos)[1]).concat(data.branches.map((b) => px(b.tag)[1]));
  const bounds = {
    x: Math.min(...xs) - W / 2 - PAD, y: Math.min(...ys) - H / 2 - PAD,
    w: Math.max(...xs) - Math.min(...xs) + W + 2 * PAD,
    h: Math.max(...ys) - Math.min(...ys) + H + 2 * PAD,
  };
  const svg = svgEl("svg", { class: "map-graph", role: "group",
    "aria-label": "Graph of plasma models; select a model or a reduction for details" });
  const defs = svgEl("defs", {}, svg);
  for (const kind of ["base", "dim", "hi"]) {
    const m = svgEl("marker", { id: "map-arrow-" + kind, class: "map-arrow-" + kind,
      viewBox: "0 0 10 10", refX: "9", refY: "5", markerWidth: "7", markerHeight: "7",
      orient: "auto-start-reverse" }, defs);
    svgEl("path", { d: "M0,1 L10,5 L0,9 z" }, m);
  }
  const viewport = svgEl("g", {}, svg);
  const tags = svgEl("g", { class: "map-tags", "aria-hidden": "true" }, viewport);
  const edgeLayer = svgEl("g", {}, viewport);
  const nodeLayer = svgEl("g", {}, viewport);

  for (const b of data.branches) {
    const [x, y] = px(b.tag);
    const t = svgEl("text", { x, y, class: "map-tag map-branch-" + b.id, "text-anchor": "middle" }, tags);
    t.textContent = b.name;
  }

  // Point where the segment from the box center toward (tx, ty) leaves the box.
  const exit = (cx, cy, tx, ty) => {
    const dx = tx - cx, dy = ty - cy;
    const s = Math.min(Math.abs((W / 2 + 3) / (dx || 1e-9)), Math.abs((H / 2 + 3) / (dy || 1e-9)));
    return [cx + dx * s, cy + dy * s];
  };

  const items = new Map(); // "node-id" / "edge-id" -> { el, data, kind }
  const focusable = (g, id, label) => {
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", label);
    g.dataset.target = id;
  };
  for (const e of data.edges) {
    const [ax, ay] = px(nodeOf.get(e.from).pos);
    const [bx, by] = px(nodeOf.get(e.to).pos);
    const [x1, y1] = exit(ax, ay, bx, by);
    const [x2, y2] = exit(bx, by, ax, ay);
    const d = `M${x1.toFixed(1)},${y1.toFixed(1)} L${x2.toFixed(1)},${y2.toFixed(1)}`;
    const g = svgEl("g", { class: "map-edge status-" + e.status }, edgeLayer);
    svgEl("path", { d, class: "map-edge-hit" }, g);
    svgEl("path", { d, class: "map-edge-line", "marker-end": "url(#map-arrow-base)" }, g);
    focusable(g, "edge-" + e.id, `Reduction from ${nodeOf.get(e.from).name} to ${nodeOf.get(e.to).name}`);
    items.set("edge-" + e.id, { el: g, data: e, kind: "edge" });
  }
  for (const n of data.nodes) {
    const [x, y] = px(n.pos);
    const g = svgEl("g", { class: "map-node map-branch-" + n.branch,
      transform: `translate(${x},${y})` }, nodeLayer);
    svgEl("rect", { x: -W / 2, y: -H / 2, width: W, height: H, rx: 5 }, g);
    const lines = n.label.split("\n");
    const t = svgEl("text", { "text-anchor": "middle" }, g);
    lines.forEach((line, i) => {
      const s = svgEl("tspan", { x: 0, y: (i - (lines.length - 1) / 2) * 17 + 5 }, t);
      s.textContent = line;
    });
    focusable(g, "node-" + n.id, n.name);
    items.set("node-" + n.id, { el: g, data: n, kind: "node" });
  }
  stage.replaceChildren(svg);
  root.classList.add("is-interactive");

  // ---------------------------------------------------------- pan, zoom
  let view = { ...bounds };
  const apply = () => svg.setAttribute("viewBox", `${view.x} ${view.y} ${view.w} ${view.h}`);
  const fit = () => {
    const r = stage.getBoundingClientRect();
    const aspect = r.width / Math.max(r.height, 1);
    view = { ...bounds };
    if (view.w / view.h < aspect) { const w = view.h * aspect; view.x -= (w - view.w) / 2; view.w = w; }
    else { const h = view.w / aspect; view.y -= (h - view.h) / 2; view.h = h; }
    apply();
  };
  const toView = (clientX, clientY) => {
    const r = svg.getBoundingClientRect();
    return [view.x + (clientX - r.left) / r.width * view.w, view.y + (clientY - r.top) / r.height * view.h];
  };
  const zoom = (factor, cx, cy) => {
    const w = Math.min(Math.max(view.w / factor, bounds.w / 12), bounds.w * 3);
    const f = view.w / w;
    view = { x: cx - (cx - view.x) / f, y: cy - (cy - view.y) / f, w, h: view.h / f };
    apply();
  };
  svg.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const [cx, cy] = toView(ev.clientX, ev.clientY);
    zoom(Math.exp(-ev.deltaY * 0.0015), cx, cy);
  }, { passive: false });

  const pointers = new Map();
  let moved = 0, pinch = 0;
  svg.addEventListener("pointerdown", (ev) => {
    pointers.set(ev.pointerId, [ev.clientX, ev.clientY]);
    moved = 0;
    if (pointers.size === 2) {
      const [p, q] = [...pointers.values()];
      pinch = Math.hypot(p[0] - q[0], p[1] - q[1]);
    }
  });
  svg.addEventListener("pointermove", (ev) => {
    const last = pointers.get(ev.pointerId);
    if (!last) return;
    if (pointers.size === 1) {
      const r = svg.getBoundingClientRect();
      const dx = ev.clientX - last[0], dy = ev.clientY - last[1];
      moved += Math.abs(dx) + Math.abs(dy);
      if (moved > 4 && !svg.hasPointerCapture(ev.pointerId)) svg.setPointerCapture(ev.pointerId);
      view.x -= dx / r.width * view.w;
      view.y -= dy / r.height * view.h;
      apply();
    }
    pointers.set(ev.pointerId, [ev.clientX, ev.clientY]);
    if (pointers.size === 2) {
      const [p, q] = [...pointers.values()];
      const dist = Math.hypot(p[0] - q[0], p[1] - q[1]);
      const [cx, cy] = toView((p[0] + q[0]) / 2, (p[1] + q[1]) / 2);
      if (pinch > 0) zoom(dist / pinch, cx, cy);
      pinch = dist;
      moved = 99;
    }
  });
  const release = (ev) => { pointers.delete(ev.pointerId); if (pointers.size < 2) pinch = 0; };
  svg.addEventListener("pointerup", release);
  svg.addEventListener("pointercancel", release);

  root.querySelectorAll("[data-zoom]").forEach((b) => b.addEventListener("click", () => {
    const c = [view.x + view.w / 2, view.y + view.h / 2];
    if (b.dataset.zoom === "in") zoom(1.4, ...c);
    else if (b.dataset.zoom === "out") zoom(1 / 1.4, ...c);
    else fit();
  }));

  // ------------------------------------------------------ course routes
  const routeOf = (course) => {
    const edges = new Set(data.edges.filter((e) => e.courses.includes(course)).map((e) => "edge-" + e.id));
    const nodes = new Set(data.nodes.filter((n) => n.courses.includes(course)).map((n) => "node-" + n.id));
    for (const e of data.edges) if (edges.has("edge-" + e.id)) { nodes.add("node-" + e.from); nodes.add("node-" + e.to); }
    return new Set([...edges, ...nodes]);
  };
  const setCourse = (course) => {
    const on = course ? routeOf(course) : null;
    for (const [id, item] of items) {
      item.el.classList.toggle("is-off", !!on && !on.has(id));
      item.el.classList.toggle("is-on", !!on && on.has(id));
    }
    root.querySelectorAll("[data-course]").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.course === course)));
    const url = new URL(location.href);
    if (course) url.searchParams.set("course", course); else url.searchParams.delete("course");
    history.replaceState(null, "", url);
    markers();
  };
  root.querySelectorAll("[data-course]").forEach((b) =>
    b.addEventListener("click", () => setCourse(b.dataset.course)));

  // ----------------------------------------------------------- selection
  let selected = null;
  const markers = () => {
    for (const item of items.values()) {
      if (item.kind !== "edge") continue;
      const el = item.el;
      const kind = el.classList.contains("is-selected") || el.classList.contains("is-adjacent") ? "hi"
        : el.classList.contains("is-off") ? "dim" : "base";
      el.querySelector(".map-edge-line").setAttribute("marker-end", `url(#map-arrow-${kind})`);
    }
  };
  const select = (id) => {
    const item = items.get(id);
    if (!item) return;
    const entry = document.getElementById(id);
    for (const it of items.values()) it.el.classList.remove("is-selected", "is-adjacent");
    item.el.classList.add("is-selected");
    if (item.kind === "node") {
      for (const e of data.edges) if (e.from === item.data.id || e.to === item.data.id)
        items.get("edge-" + e.id).el.classList.add("is-adjacent");
    } else {
      items.get("node-" + item.data.from).el.classList.add("is-adjacent");
      items.get("node-" + item.data.to).el.classList.add("is-adjacent");
    }
    markers();
    selected = id;
    if (entry) {
      const copy = entry.cloneNode(true);
      copy.removeAttribute("id");
      panel.replaceChildren(copy);
      panel.scrollTop = 0;
    }
    if (location.hash !== "#" + id) history.replaceState(null, "", "#" + id);
  };
  stage.addEventListener("click", (ev) => {
    if (moved > 4) return;
    const g = ev.target.closest("[data-target]");
    if (g) select(g.dataset.target);
  });
  stage.addEventListener("keydown", (ev) => {
    const g = ev.target.closest("[data-target]");
    if (g && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); select(g.dataset.target); }
  });
  // Links between entries inside the panel select instead of scrolling away.
  panel.addEventListener("click", (ev) => {
    const a = ev.target.closest("a[href^='#']");
    if (a && items.has(a.getAttribute("href").slice(1))) {
      ev.preventDefault();
      select(a.getAttribute("href").slice(1));
    }
  });
  window.addEventListener("hashchange", () => select(location.hash.slice(1)));

  // Start with the whole map when its labels stay legible; on a narrow
  // screen start at a legible scale around the selection or the top.
  const MIN_SCALE = 0.55;
  const start = () => {
    fit();
    const r = stage.getBoundingClientRect();
    if (r.width / view.w >= MIN_SCALE) return;
    const item = items.get(selected);
    let [cx, cy] = [px(nodeOf.get("maxwell-lorentz").pos)[0], null];
    if (item) {
      const ends = item.kind === "node" ? [item.data.pos] : [nodeOf.get(item.data.from).pos, nodeOf.get(item.data.to).pos];
      cx = ends.reduce((a, p) => a + px(p)[0], 0) / ends.length;
      cy = ends.reduce((a, p) => a + px(p)[1], 0) / ends.length;
    }
    const w = r.width / MIN_SCALE, h = r.height / MIN_SCALE;
    view = { x: cx - w / 2, y: cy === null ? bounds.y : cy - h / 2, w, h };
    apply();
  };
  const initial = new URL(location.href).searchParams.get("course");
  setCourse(data.courses.some((c) => c.id === initial) ? initial : "");
  if (items.has(location.hash.slice(1))) {
    select(location.hash.slice(1));
    // Show the map with the selection rather than the entry in the list.
    // The browser scrolls to the fragment after load; scroll back afterwards.
    addEventListener("load", () => setTimeout(() => root.scrollIntoView({ block: "start" }), 0));
  }
  start();
  let width = stage.clientWidth;
  new ResizeObserver(() => {
    if (stage.clientWidth !== width) { width = stage.clientWidth; start(); }
  }).observe(stage);
})();
