/* Presentation mode for the lecture decks.
 *
 * Reads ./manifest.json (written by scripts/build-present.py):
 *   { stem, chapter, title, course, author, aspect, pdf,
 *     pages: [{ src, kind: "static"|"animation", background: "light"|"dark",
 *               video?, poster?, loop? }] }
 * One page fills the viewport. Touch: swipe or tap the left/right part of
 * the page; tap the middle of an animation to play or pause it. Apple
 * Pencil never navigates: it shows a laser dot. Keys: arrows, PageUp/Down,
 * Space, Home/End, G overview, F full screen, L mouse laser, B/W blank,
 * R restart animation, ? help.
 */
"use strict";

(() => {
  const root = document.documentElement;
  const stage = document.querySelector(".stage");
  const frame = document.querySelector(".frame");
  const laser = document.querySelector(".laser");
  const where = document.querySelector(".where");
  const progress = document.querySelector(".progress");
  const overview = document.querySelector(".overview ol");
  const statusBox = document.querySelector(".status");
  const live = document.querySelector("[aria-live]");

  let deck = null;
  let pages = [];
  let index = 0;
  let mouseLaser = false;
  let hudTimer = 0;
  let statusTimer = 0;
  let wakeLock = null;

  const clamp = (i) => Math.max(0, Math.min(pages.length - 1, i));
  const currentPage = () => pages[index];

  function status(text, ms = 1600) {
    statusBox.textContent = text;
    statusBox.classList.add("show");
    clearTimeout(statusTimer);
    statusTimer = setTimeout(() => statusBox.classList.remove("show"), ms);
  }

  function showHud(ms = 1800) {
    root.classList.add("hud-on");
    clearTimeout(hudTimer);
    hudTimer = setTimeout(() => {
      if (!root.classList.contains("overview-on")) root.classList.remove("hud-on");
    }, ms);
  }

  /* ------------------------------------------------------------ pages */

  function buildPage(spec, i) {
    const el = document.createElement("section");
    el.className = "page " + spec.kind;
    el.setAttribute("aria-roledescription", "slide");
    el.setAttribute("aria-label", `Page ${i + 1} of ${deck.pages.length}`);
    const img = document.createElement("img");
    img.alt = spec.alt || "";
    img.decoding = "async";
    img.draggable = false;
    img.dataset.src = spec.kind === "animation" ? (spec.poster || spec.src) : spec.src;
    if (spec.kind === "animation") {
      img.className = "poster";
      const video = document.createElement("video");
      video.muted = true;
      video.defaultMuted = true;
      video.playsInline = true;
      video.setAttribute("playsinline", "");
      video.setAttribute("webkit-playsinline", "");
      video.loop = spec.loop !== false;
      video.preload = "none";
      video.disablePictureInPicture = true;
      video.dataset.src = spec.video;
      video.addEventListener("playing", () => el.classList.add("started"));
      video.addEventListener("ended", () => flash(el, "replay"));
      el.append(video, img);
      const f = document.createElement("div");
      f.className = "flash";
      el.append(f);
    } else {
      el.append(img);
    }
    return { spec, el, img, video: el.querySelector("video") };
  }

  // Load the image (and, for animations, the video) of page i.
  function warm(i, withVideo) {
    const p = pages[i];
    if (!p) return;
    if (!p.img.src) p.img.src = p.img.dataset.src;
    if (p.video && withVideo && !p.video.src) {
      p.video.src = p.video.dataset.src;
      p.video.preload = "auto";
      p.video.load();
    }
  }

  function resetVideo(p) {
    if (!p || !p.video) return;
    p.video.pause();
    if (p.video.currentTime > 0) p.video.currentTime = 0;
    p.el.classList.remove("started");
  }

  function go(i, { replace = false } = {}) {
    i = clamp(i);
    const old = pages[index];
    if (old && i !== index) {
      old.el.classList.remove("current");
      resetVideo(old);
    }
    index = i;
    const p = pages[index];
    warm(index, true);
    p.el.classList.add("current");
    root.dataset.bg = p.spec.background || (p.spec.kind === "animation" ? "dark" : "light");
    delete root.dataset.blank;
    // Neighbours: images two ahead and one behind, the next video one ahead.
    warm(index + 1, true);
    warm(index + 2, false);
    warm(index - 1, false);
    const n = pages.length;
    where.innerHTML = `<b>${index + 1}</b> / ${n}`;
    progress.style.width = `${(100 * (index + 1)) / n}%`;
    live.textContent = `Page ${index + 1} of ${n}`;
    for (const a of overview.querySelectorAll("a")) {
      if (Number(a.dataset.i) === index) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    }
    const hash = `#${index + 1}`;
    if (location.hash !== hash) history[replace ? "replaceState" : "pushState"](null, "", hash);
  }

  const next = () => go(index + 1);
  const prev = () => go(index - 1);

  /* ------------------------------------------------------- animations */

  const icons = {
    play: '<svg viewBox="0 0 24 24"><path d="M9 7l9 5-9 5z"/></svg>',
    pause: '<svg viewBox="0 0 24 24"><path d="M8 7h3v10H8zM13 7h3v10h-3z"/></svg>',
    replay: '<svg viewBox="0 0 24 24"><path d="M12 6a6 6 0 1 1-6 6h2a4 4 0 1 0 4-4v3L8 7l4-4z"/></svg>',
  };

  function flash(el, kind) {
    const f = el.querySelector(".flash");
    if (!f) return;
    f.innerHTML = icons[kind];
    f.classList.remove("show");
    void f.offsetWidth;
    f.classList.add("show");
  }

  function toggleVideo() {
    const p = currentPage();
    if (!p.video) return false;
    warm(index, true);
    if (p.video.paused) {
      p.video.play().then(() => flash(p.el, "play"))
        .catch(() => status("Tap the animation once more to start it."));
    } else {
      p.video.pause();
      flash(p.el, "pause");
    }
    return true;
  }

  function restartVideo() {
    const p = currentPage();
    if (!p.video) return;
    p.video.currentTime = 0;
    p.video.play().catch(() => {});
    flash(p.el, "replay");
  }

  function seekVideo(dt) {
    const p = currentPage();
    if (!p.video || !Number.isFinite(p.video.duration)) return;
    p.video.currentTime = Math.max(0, Math.min(p.video.duration, p.video.currentTime + dt));
  }

  /* ------------------------------------------------------ interaction */

  function moveLaser(x, y) {
    laser.style.transform = `translate(${x}px, ${y}px)`;
    laser.classList.add("on");
  }
  const hideLaser = () => laser.classList.remove("on");

  // Tap zones relative to the page frame: left 30 % back, the rest forward;
  // on animations the middle 40 % toggles playback; the top band shows the HUD.
  function tap(x, y) {
    const r = frame.getBoundingClientRect();
    if (y < Math.max(56, r.top + 0.1 * r.height)) { showHud(3000); return; }
    const u = (x - r.left) / r.width;
    if (currentPage().video && u > 0.3 && u < 0.7) { toggleVideo(); return; }
    if (u < 0.3) prev(); else next();
  }

  let gesture = null;
  stage.addEventListener("pointerdown", (e) => {
    if (e.pointerType === "pen") {
      gesture = { pen: true };
      moveLaser(e.clientX, e.clientY);
      return;
    }
    if (e.pointerType === "mouse" && e.button !== 0) return;
    gesture = { x: e.clientX, y: e.clientY, t: performance.now(), id: e.pointerId };
  });
  stage.addEventListener("pointermove", (e) => {
    if (e.pointerType === "pen") {
      if (e.pressure > 0 || e.buttons) moveLaser(e.clientX, e.clientY);
      return;
    }
    if (e.pointerType === "mouse") {
      if (mouseLaser) moveLaser(e.clientX, e.clientY);
      else showHud();
      root.classList.remove("idle");
    }
  });
  const end = (e) => {
    const g = gesture;
    gesture = null;
    if (!g) return;
    if (g.pen) { setTimeout(hideLaser, 350); return; }
    if (e.type === "pointercancel" || g.id !== e.pointerId) return;
    const dx = e.clientX - g.x;
    const dy = e.clientY - g.y;
    if (Math.abs(dx) > 40 && Math.abs(dx) > 1.4 * Math.abs(dy)) {
      if (dx < 0) next(); else prev();
    } else if (Math.abs(dx) < 12 && Math.abs(dy) < 12 && performance.now() - g.t < 600) {
      if (!(e.pointerType === "mouse" && mouseLaser)) tap(e.clientX, e.clientY);
    }
  };
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);
  stage.addEventListener("pointerleave", () => { if (!mouseLaser) hideLaser(); });

  function toggleOverview(on = !root.classList.contains("overview-on")) {
    root.classList.toggle("overview-on", on);
    if (on) {
      root.classList.add("hud-on");
      clearTimeout(hudTimer);
      for (const p of pages) warm(pages.indexOf(p), false);
      overview.querySelector('[aria-current="page"]')?.scrollIntoView({ block: "center" });
    } else showHud(800);
  }

  async function toggleFullscreen() {
    const el = document.documentElement;
    const full = document.fullscreenElement || document.webkitFullscreenElement;
    try {
      if (full) await (document.exitFullscreen || document.webkitExitFullscreen).call(document);
      else await (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
    } catch {
      status("Full screen: Share → Add to Home Screen, then open from there.", 3500);
    }
  }

  function setBlank(kind) {
    if (root.dataset.blank === kind) delete root.dataset.blank;
    else root.dataset.blank = kind;
  }

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (root.classList.contains("help-on") && k !== "?") { root.classList.remove("help-on"); }
    if (root.classList.contains("overview-on")) {
      if (k === "Escape" || k === "g" || k === "G" || k === "o") { toggleOverview(false); e.preventDefault(); }
      return;
    }
    let handled = true;
    switch (k) {
      case "ArrowRight": case "ArrowDown": case "PageDown": case "Enter": next(); break;
      case "ArrowLeft": case "ArrowUp": case "PageUp": case "Backspace": prev(); break;
      case " ": if (!toggleVideo()) (e.shiftKey ? prev : next)(); break;
      case "Home": go(0); break;
      case "End": go(pages.length - 1); break;
      case "k": case "K": toggleVideo(); break;
      case "r": case "R": restartVideo(); break;
      case "j": case "J": seekVideo(-2); break;
      case "l": seekVideo(2); break;
      case "L":
        mouseLaser = !mouseLaser;
        if (!mouseLaser) hideLaser();
        status(mouseLaser ? "Laser pointer on" : "Laser pointer off");
        document.querySelector("[data-act=laser]")?.setAttribute("aria-pressed", String(mouseLaser));
        break;
      case "g": case "G": case "o": case "O": toggleOverview(true); break;
      case "f": case "F": toggleFullscreen(); break;
      case "b": case "B": case ".": setBlank("black"); break;
      case "w": case "W": case ",": setBlank("white"); break;
      case "?": root.classList.toggle("help-on"); break;
      case "Escape": delete root.dataset.blank; root.classList.remove("hud-on"); break;
      default: handled = false;
    }
    if (handled) e.preventDefault();
  });

  document.querySelector(".hud").addEventListener("click", (e) => {
    const act = e.target.closest("[data-act]")?.dataset.act;
    if (!act) return;
    e.stopPropagation();
    if (act === "prev") prev();
    else if (act === "next") next();
    else if (act === "overview") toggleOverview();
    else if (act === "fullscreen") toggleFullscreen();
    else if (act === "laser") {
      mouseLaser = !mouseLaser;
      e.target.closest("button").setAttribute("aria-pressed", String(mouseLaser));
      if (!mouseLaser) hideLaser();
    }
    else if (act === "offline") makeOffline();
    showHud(2500);
  });
  document.querySelector(".hud").addEventListener("pointerdown", (e) => e.stopPropagation());

  overview.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-i]");
    if (!a) return;
    e.preventDefault();
    go(Number(a.dataset.i));
    toggleOverview(false);
  });
  document.querySelector(".overview").addEventListener("click", (e) => {
    if (e.target.classList.contains("overview")) toggleOverview(false);
  });

  window.addEventListener("popstate", () => go(pageFromHash() ?? index, { replace: true }));

  // Idle mouse cursor disappears.
  let idleTimer = 0;
  document.addEventListener("mousemove", () => {
    root.classList.remove("idle");
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => root.classList.add("idle"), 1800);
  });

  /* ------------------------------------------------- offline, wake lock */

  async function keepAwake() {
    try {
      if ("wakeLock" in navigator && document.visibilityState === "visible") {
        wakeLock = await navigator.wakeLock.request("screen");
      }
    } catch { /* not granted: the screen may dim as usual */ }
  }
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") keepAwake();
    else resetVideo(currentPage());
  });

  function deckUrls() {
    const base = new URL("./", location.href);
    const urls = [new URL("manifest.json", base).href, location.href.split("#")[0]];
    for (const asset of ["index.html", "decks.json", "present.js", "present.css",
      "manifest.webmanifest", "icon.svg", "icon-180.png", "icon-512.png"]) {
      urls.push(new URL("../" + asset, base).href);
    }
    for (const font of ["Regular", "Bold"]) {
      urls.push(new URL(`../../fonts/STIXTwoText-${font}.otf`, base).href);
    }
    for (const p of deck.pages) {
      urls.push(new URL(p.src, base).href);
      if (p.poster) urls.push(new URL(p.poster, base).href);
      if (p.video) urls.push(new URL(p.video, base).href);
    }
    return urls;
  }

  async function makeOffline(quiet = false) {
    const reg = await navigator.serviceWorker?.ready.catch(() => null);
    if (!reg || !reg.active) { if (!quiet) status("Offline copy needs Safari or a current browser."); return; }
    const done = new Promise((resolve) => {
      const onMsg = (e) => {
        if (e.data?.type !== "cached") return;
        navigator.serviceWorker.removeEventListener("message", onMsg);
        resolve(e.data);
      };
      navigator.serviceWorker.addEventListener("message", onMsg);
    });
    reg.active.postMessage({ type: "cache", urls: deckUrls() });
    if (!quiet) status("Saving this deck for offline use …", 4000);
    const r = await done;
    if (!quiet) status(r.failed ? `Saved, ${r.failed} file(s) failed` : "Deck available offline", 2500);
  }

  /* ------------------------------------------------------------ start */

  function pageFromHash() {
    const m = /^#(\d+)$/.exec(location.hash);
    return m ? Number(m[1]) - 1 : null;
  }

  async function start() {
    const res = await fetch("manifest.json", { cache: "no-cache" });
    deck = await res.json();
    if ("serviceWorker" in navigator) {
      try {
        await navigator.serviceWorker.register("../sw.js", { scope: "../" });
        await navigator.serviceWorker.ready;
        // Keep the initial MP4 request and subsequent footer/range reads on
        // the same transport. Claiming a page during playback can interrupt
        // Chrome's demuxer when it switches from HTTP to cached responses.
        if (!navigator.serviceWorker.controller) {
          await new Promise((resolve) => navigator.serviceWorker.addEventListener(
            "controllerchange", resolve, { once: true }));
        }
      } catch { /* The online deck still works if registration is unavailable. */ }
    }
    root.style.setProperty("--aspect", String(deck.aspect || 297 / 210));
    document.title = `${deck.course} ${deck.chapter} · ${deck.title}`;
    pages = deck.pages.map(buildPage);
    frame.append(...pages.map((p) => p.el));
    overview.innerHTML = deck.pages.map((p, i) => {
      const src = p.kind === "animation" ? (p.poster || p.src) : p.src;
      const dark = (p.background || (p.kind === "animation" ? "dark" : "light")) === "dark";
      return `<li><a href="#${i + 1}" data-i="${i}"><span class="thumb${dark ? " dark" : ""}" ` +
        `style="background-image:url('${src}')"></span><span class="num">${i + 1}</span></a></li>`;
    }).join("");
    const pdf = document.querySelector("[data-act=pdf]");
    if (pdf && deck.pdf) pdf.href = deck.pdf;
    go(pageFromHash() ?? 0, { replace: true });
    keepAwake();
    if (navigator.serviceWorker?.controller) makeOffline(true).catch(() => {});
  }

  start().catch((err) => {
    status("Could not load this deck: " + err.message, 8000);
    console.error(err);
  });
})();
