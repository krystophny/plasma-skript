"use strict";

(() => {
  const link = document.querySelector('[data-script-feedback="true"]');
  const main = document.querySelector("main");
  if (!link || !main) return;

  // Some Typst section headings lack IDs. Give them deterministic anchors so
  // a report can link back to the exact section instead of the whole chapter.
  const headings = [...main.querySelectorAll("h2")];
  for (const heading of headings) {
    if (heading.id) continue;
    const stem = "section-" + heading.textContent.trim().normalize("NFKD")
      .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    let id = stem;
    for (let suffix = 2; document.getElementById(id); suffix++) id = `${stem}-${suffix}`;
    heading.id = id;
  }

  function currentSection() {
    const selection = window.getSelection();
    if (selection && !selection.isCollapsed && main.contains(selection.anchorNode)) {
      const node = selection.anchorNode.nodeType === Node.ELEMENT_NODE
        ? selection.anchorNode : selection.anchorNode.parentElement;
      return headings.filter(h => h === node ||
        Boolean(h.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING)).at(-1)
        || null;
    }
    const readingLine = window.innerHeight * 0.3;
    return headings.filter(h => h.getBoundingClientRect().top <= readingLine).at(-1) || null;
  }

  function update() {
    const section = currentSection();
    const chapter = (main.querySelector("h1")?.textContent || document.title).trim();
    const sectionTitle = section?.textContent.trim();
    const page = new URL(link.dataset.pageUrl);
    if (section) page.hash = section.id;
    const location = sectionTitle ? `${chapter} — ${sectionTitle}` : chapter;
    let body = `### Location\n${location}\n${page.href}\n`;
    const selection = window.getSelection();
    if (selection && main.contains(selection.anchorNode) && !selection.isCollapsed) {
      const selected = selection.toString().trim().slice(0, 500);
      if (selected) body += `\n### Selected passage\n${selected}\n`;
    }
    body += "\n### Problem or suggestion\nPlease describe the issue here.\n";
    const issue = new URL(link.dataset.repoUrl + "/issues/new");
    issue.searchParams.set("title", `Script feedback: ${location}`.slice(0, 200));
    issue.searchParams.set("body", body);
    link.href = issue.href;
  }

  // Native links retain keyboard/middle-click behavior and need no popup API.
  for (const event of ["pointerdown", "focus", "click", "contextmenu"]) {
    link.addEventListener(event, update);
  }
  update();

  // Generated heading anchors must also resolve when following an old report.
  if (window.location.hash) {
    try {
      const target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
      if (target?.id.startsWith("section-")) target.scrollIntoView();
    } catch (_) { /* A malformed fragment must not break the reading page. */ }
  }
})();
