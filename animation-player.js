/* Inline, silent playback with brief, compact controls along the bottom edge. */
"use strict";

for (const player of document.querySelectorAll(".animation-player")) {
  const video = player.querySelector("video");
  const controls = player.querySelector(".animation-controls");
  const seek = controls?.querySelector(".animation-seek");
  if (!video || !controls || !seek) continue;

  const status = player.querySelector(".animation-status");
  const fullButton = controls.querySelector(".animation-fullscreen");
  const description = video.getAttribute("aria-label") || "Animation";
  let hideTimer;
  let seeking = false;
  const message = (text) => { if (status) status.textContent = text; };
  const play = () => video.play().catch(() => message("Tap the animation to start playback."));
  const reveal = () => {
    clearTimeout(hideTimer);
    player.classList.add("animation-controls-visible");
    hideTimer = setTimeout(() => {
      if (!seeking) player.classList.remove("animation-controls-visible");
    }, 650);
  };
  const updateFullscreen = () => {
    const full = document.fullscreenElement === player || player.classList.contains("animation-full-window");
    const label = full ? "Exit full screen" : "Full screen";
    fullButton.setAttribute("aria-label", label);
    fullButton.title = label;
    const path = full ? "M9 3v6H3m18 0h-6V3M3 15h6v6m6 0v-6h6" : "M9 3H3v6m12-6h6v6M3 15v6h6m6 0h6v-6";
    fullButton.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${path}"/></svg>`;
  };
  const exitWindow = () => { player.classList.remove("animation-full-window"); updateFullscreen(); };
  const fullWindow = () => { player.classList.add("animation-full-window"); updateFullscreen(); reveal(); };
  const fullscreen = () => {
    if (player.classList.contains("animation-full-window")) { exitWindow(); return; }
    if (document.fullscreenElement === player) { document.exitFullscreen(); return; }
    // Only the explicit full-screen icon requests this, never a video tap.
    if (player.requestFullscreen) {
      player.requestFullscreen().catch(fullWindow);
    } else fullWindow();
  };
  const toggle = () => { video.paused ? play() : video.pause(); reveal(); };
  fullButton.addEventListener("click", fullscreen);
  document.addEventListener("fullscreenchange", () => { updateFullscreen(); reveal(); });
  player.addEventListener("pointermove", reveal);
  player.addEventListener("pointerenter", reveal);
  player.addEventListener("focusin", reveal);
  controls.addEventListener("pointerdown", () => { seeking = true; reveal(); });
  document.addEventListener("pointerup", () => { if (seeking) { seeking = false; reveal(); } });
  document.addEventListener("pointercancel", () => { if (seeking) { seeking = false; reveal(); } });
  video.addEventListener("click", toggle);
  const updateProgress = () => {
    if (Number.isFinite(video.duration)) {
      seek.max = String(video.duration);
      if (!seeking) seek.value = String(video.currentTime);
      seek.setAttribute("aria-valuetext", `${Math.round(video.currentTime)} of ${Math.round(video.duration)} seconds`);
    }
  };
  seek.addEventListener("input", () => { video.currentTime = Number(seek.value); reveal(); });
  video.addEventListener("loadedmetadata", updateProgress);
  video.addEventListener("timeupdate", updateProgress);
  video.addEventListener("keydown", (event) => {
    if (event.key === " " || event.key === "Enter") { event.preventDefault(); toggle(); }
    if (["ArrowLeft", "ArrowRight", "Home"].includes(event.key) && Number.isFinite(video.duration)) {
      event.preventDefault();
      video.currentTime = event.key === "Home" ? 0 : Math.max(0, Math.min(video.duration, video.currentTime + (event.key === "ArrowLeft" ? -5 : 5)));
      reveal();
    }
    if (event.key.toLowerCase() === "f") fullscreen();
    if (event.key === "Escape") exitWindow();
  });
  const updatePlayback = () => {
    video.setAttribute("aria-label", `${description}. ${video.paused ? "Play" : "Pause"} animation`);
    video.setAttribute("aria-pressed", String(!video.paused));
  };
  video.addEventListener("play", () => { updatePlayback(); message(""); });
  video.addEventListener("pause", updatePlayback);
  video.addEventListener("error", () => message("The animation could not load. Please reload the page."));
  video.muted = true;
  video.controls = false;
  video.tabIndex = 0;
  video.setAttribute("role", "button");
  video.setAttribute("aria-keyshortcuts", "Space Enter F ArrowLeft ArrowRight Home");
  controls.hidden = false;
  updatePlayback();
  updateFullscreen();
  updateProgress();
  if (document.body.classList.contains("animation-presentation") && !matchMedia("(prefers-reduced-motion: reduce)").matches) play();
}
