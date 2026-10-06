#!/usr/bin/env node

"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const { chromium } = require(
  process.env.PLAYWRIGHT_CORE_PATH || "playwright-core",
);

const pages = [
  "/index.html",
  "/chapters/01-introduction.html",
  "/chapters/02-thermal-equilibrium.html",
  "/chapters/03-debye-shielding.html",
  "/chapters/04-plasma-oscillations.html",
  "/chapters/05-single-particle-motion.html",
  "/chapters/06-kinetic-theory.html",
  "/chapters/07-moments.html",
  "/chapters/08-multiple-fluids.html",
  "/chapters/09-mhd.html",
  "/chapters/10-collisions-conductivity.html",
  "/chapters/11-diffusion.html",
  "/chapters/12-introduction-waves.html",
  "/chapters/13-cold-magnetized-waves.html",
  "/chapters/14-finite-temperature-waves.html",
  "/chapters/15-hot-plasma-waves.html",
  "/chapters/16-sheaths-probes.html",
  "/appendices/mathematical-toolkit.html",
];

const viewports = [
  { name: "mobile", width: 390, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "wide", width: 1440, height: 1200 },
];

const screenshotTargets = new Map([
  ["/chapters/01-introduction.html", "main figure:has(.model-figure-diagram)"],
  ["/chapters/02-thermal-equilibrium.html", "main figure:has(img), main figure:has(svg)"],
  ["/chapters/03-debye-shielding.html", "main figure:has(svg), main figure:has(img[src^='data:image/svg+xml']), main figure:has(img[src$='.svg'])"],
  ["/chapters/04-plasma-oscillations.html", "main video, main iframe.animation-embed"],
  ["/chapters/07-moments.html", 'main math[display="block"]'],
  [
    "/chapters/13-cold-magnetized-waves.html",
    'main > div[id^="frame-wrapper-"]',
  ],
  ["/chapters/16-sheaths-probes.html", "main video, main iframe.animation-embed"],
  [
    "/appendices/mathematical-toolkit.html",
    'main > div[id^="frame-wrapper-"]',
  ],
]);

const baseUrl = new URL(process.env.SITE_BASE_URL || "http://127.0.0.1/");
const artifactDir =
  process.env.SITE_AUDIT_ARTIFACT_DIR ||
  path.join(os.tmpdir(), "plasma-site-audit");
const failures = [];
let screenshotCount = 0;

fs.rmSync(artifactDir, { recursive: true, force: true });
fs.mkdirSync(artifactDir, { recursive: true });

function recordFailure(message) {
  failures.push(message);
}

function screenshotName(pagePath, viewportName) {
  const pageName = pagePath
    .replace(/^\//, "")
    .replace(/\.html$/, "")
    .replaceAll("/", "-");
  return `${pageName}-${viewportName}.png`;
}

function sameOrigin(url) {
  try {
    return new URL(url).origin === baseUrl.origin;
  } catch {
    return false;
  }
}

async function auditPage(page, pagePath, viewport) {
  const pageLabel = `${viewport.name} ${pagePath}`;
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  const badResponses = [];

  page.on("console", (message) => {
    if (
      message.type() === "error" &&
      // A bare 404 console line carries no URL; the favicon probe produces it
      // with server-specific wording. Real same-origin 404s are still caught by
      // the response handler below.
      !/^Failed to load resource: the server responded with a status of 404 \((File not found|Not Found)\)$/.test(
        message.text(),
      )
    ) {
      consoleErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    pageErrors.push(error.message);
  });
  page.on("requestfailed", (request) => {
    // Chromium cancels media requests (net::ERR_ABORTED) when it switches to
    // range requests or leaves the page; missing media still fails through the
    // response handler.
    const abortedMedia =
      (request.resourceType() === "media" || request.url().endsWith(".mp4")) &&
      request.failure()?.errorText === "net::ERR_ABORTED";
    if (sameOrigin(request.url()) && !request.url().endsWith("/favicon.ico") && !abortedMedia) {
      failedRequests.push(`${request.url()}: ${request.failure()?.errorText}`);
    }
  });
  page.on("response", (response) => {
    if (
      sameOrigin(response.url()) &&
      response.status() >= 400 &&
      !response.url().endsWith("/favicon.ico")
    ) {
      badResponses.push(`${response.status()} ${response.url()}`);
    }
  });

  try {
    const response = await page.goto(new URL(pagePath, baseUrl).href, {
      timeout: 30_000,
      waitUntil: "load",
    });

    if (!response || !response.ok()) {
      recordFailure(`${pageLabel}: page request failed`);
      return;
    }

    await page.evaluate(() =>
      document.fonts ? document.fonts.ready : Promise.resolve(),
    );
    await page.waitForTimeout(100);

    if (pagePath === "/chapters/02-thermal-equilibrium.html") {
      const sections = await page.locator("main h2").allTextContents();
      if (sections.length !== 5 || !sections.some((text) => /Saha equation/.test(text))) {
        recordFailure(`${pageLabel}: thermal chapter lacks its five teaching sections`);
      }
      const checks = await page.locator(".knowledge-check > ol > li").count();
      if (checks !== 20) {
        recordFailure(`${pageLabel}: thermal chapter must expose twenty knowledge-check questions`);
      }
      const content = await page.locator("main").innerText();
      if (!/3226/.test(content) || !/26230/.test(content)) {
        recordFailure(`${pageLabel}: computed half-ionization table is missing`);
      }
    }

    if (pagePath === "/chapters/01-introduction.html") {
      const diagramCounts = await page.evaluate(() => {
        const visibleDiagrams = () => [...document.querySelectorAll(".model-figure svg")]
          .filter((svg) => svg.getBoundingClientRect().width > 0).length;
        const withStylesheet = visibleDiagrams();
        const externalSheets = [...document.styleSheets]
          .filter((sheet) => sheet.href)
          .map((sheet) => [sheet, sheet.disabled]);
        try {
          // The single diagram must remain visible without external CSS.
          for (const [sheet] of externalSheets) sheet.disabled = true;
          return {
            total: document.querySelectorAll(".model-figure svg").length,
            withStylesheet,
            withoutStylesheet: visibleDiagrams(),
          };
        } finally {
          for (const [sheet, disabled] of externalSheets) sheet.disabled = disabled;
        }
      });
      for (const [condition, count] of Object.entries(diagramCounts)) {
        if (count !== 1) {
          recordFailure(`${pageLabel}: expected one model diagram ${condition}, found ${count}`);
        }
      }
    }

    // The reading order is observable behavior: headings and navigation must
    // agree with the sixteen-chapter course sequence, including thermal equilibrium.
    const chapterPages = pages.filter((path) => path.startsWith("/chapters/"));
    const chapterIndex = chapterPages.indexOf(pagePath);
    if (chapterIndex >= 0) {
      const heading = await page.locator("main h1").evaluate((element) => {
        const item = element.querySelector("ol > li");
        // List markers are rendered, but excluded from innerText by browsers.
        const number = item
          ? Number(item.getAttribute("value") || item.parentElement.getAttribute("start") || 1)
          : Number(element.innerText.match(/^(\d+)\./)?.[1]);
        return { number, title: element.innerText };
      });
      if (heading.number !== chapterIndex + 1) {
        recordFailure(`${pageLabel}: incorrect chapter number in ${heading.title}`);
      }
      const navigation = await page.locator('.chapter-nav a[href$=".html"]').evaluateAll(
        (links) => links.map((link) => new URL(link.href).pathname),
      );
      const expected = [
        ...(chapterIndex > 0 ? [chapterPages[chapterIndex - 1]] : []),
        chapterPages[chapterIndex + 1] || "/appendices/mathematical-toolkit.html",
      ];
      if (JSON.stringify(navigation) !== JSON.stringify(expected)) {
        recordFailure(`${pageLabel}: chapter navigation does not follow reading order`);
      }
      if (chapterIndex < 4) {
        const deck = await page.locator('.chapter-nav a[href*="../present/"]').evaluateAll(
          (links) => links.map((link) => new URL(link.href).pathname),
        );
        const expectedDeck = pagePath.replace("/chapters/", "/present/").replace(/\.html$/, "/");
        if (JSON.stringify(deck) !== JSON.stringify([expectedDeck])) {
          recordFailure(`${pageLabel}: lecture deck link does not match its chapter`);
        }
      }
    }
    if (pagePath === "/index.html") {
      const contents = await page.locator("#contents a").evaluateAll(
        (links) => links.map((link) => new URL(link.href).pathname)
          .filter((path) => path.startsWith("/chapters/")),
      );
      if (JSON.stringify(contents) !== JSON.stringify(chapterPages)) {
        recordFailure(`${pageLabel}: contents omit or misorder a chapter`);
      }
    }
    if (pagePath === "/chapters/01-introduction.html") {
      const movedSections = page.getByRole("heading", {
        name: /^(Debye shielding|Electron plasma oscillations)$/,
      });
      if (await movedSections.count()) {
        recordFailure(`${pageLabel}: dedicated topics remain sections of the introduction`);
      }
    }

    const result = await page.evaluate(() => {
      const documentElement = document.documentElement;
      const body = document.body;
      const images = [...document.images].filter(
        (image) => !image.alt.trim(),
      );
      const details = [...document.querySelectorAll("details")];
      const videos = [...document.querySelectorAll("video")];
      const invalidVideos = videos.filter((video) => {
        const hasSource =
          video.hasAttribute("src") || Boolean(video.querySelector("source[src]"));
        const hasFallback = video.textContent.trim().length > 0;
        const hasCaption = Boolean(
          video.closest("figure")?.querySelector("figcaption"),
        );
        const hasAlternativeDescription = Boolean(
          video.getAttribute("aria-label")?.trim(),
        );
        const customControls = video.closest(".animation-player")?.querySelector(".animation-controls");
        const hasControls = video.hasAttribute("controls") || (
          customControls && !customControls.hidden &&
          video.getAttribute("role") === "button" && video.tabIndex === 0 &&
          [".animation-seek[aria-label]", ".animation-fullscreen[aria-label]"].every((selector) => customControls.querySelector(selector))
        );
        return (
          !hasControls ||
          !hasSource ||
          !hasFallback ||
          !hasCaption ||
          !hasAlternativeDescription
        );
      });

      const invalidEmbeds = [...document.querySelectorAll("iframe.animation-embed")].filter((frame) => {
        const figure = frame.closest("figure");
        return !frame.title.trim() || !/^https:\/\/www\.youtube-nocookie\.com\/embed\/[A-Za-z0-9_-]{11}$/.test(frame.src) ||
          !figure?.querySelector("figcaption") || !figure?.querySelector('a[href^="https://youtu.be/"], a[href^="https://www.youtube.com/watch?"]');
      });
      invalidVideos.push(...invalidEmbeds);

      const readingColumn = document.querySelector(
        ".site-main > h2, .site-main > h1",
      );
      const readingRect = readingColumn?.getBoundingClientRect();
      const expandedDisclosureIssues = [];
      let expandedDocumentOverflow = false;
      for (const [index, detail] of details.entries()) {
        const originalOpen = detail.open;
        detail.open = true;
        const detailRect = detail.getBoundingClientRect();
        const directChildren = [...detail.children].filter(
          (child) => child.tagName !== "SUMMARY",
        );
        const overwideChild = directChildren.find((child) => {
          const childRect = child.getBoundingClientRect();
          return (
            childRect.left < detailRect.left - 2 ||
            childRect.right > detailRect.right + 2
          );
        });

        if (
          detail.classList.contains("disclosure") &&
          readingRect &&
          (detailRect.left < readingRect.left - 2 ||
            detailRect.right > readingRect.right + 2)
        ) {
          expandedDisclosureIssues.push(
            `details ${index} is outside the reading column`,
          );
        }
        if (overwideChild) {
          expandedDisclosureIssues.push(
            `details ${index} has an overwide child`,
          );
        }
        if (
          documentElement.scrollWidth >
          documentElement.clientWidth + 1
        ) {
          expandedDocumentOverflow = true;
        }

        detail.open = originalOpen;
      }

      return {
        documentWidth: documentElement.scrollWidth,
        documentClientWidth: documentElement.clientWidth,
        bodyWidth: body?.scrollWidth ?? 0,
        bodyClientWidth: body?.clientWidth ?? 0,
        openDetails: details.filter((detail) => detail.open).length,
        missingImageAlt: images.length,
        invalidVideos: invalidVideos.length,
        expandedDisclosureIssues,
        expandedDocumentOverflow,
      };
    });

    if (result.documentWidth > result.documentClientWidth + 1) {
      recordFailure(
        `${pageLabel}: document overflow ${result.documentWidth}px > ${result.documentClientWidth}px`,
      );
    }
    if (result.bodyWidth > result.bodyClientWidth + 1) {
      recordFailure(
        `${pageLabel}: body overflow ${result.bodyWidth}px > ${result.bodyClientWidth}px`,
      );
    }
    if (result.openDetails !== 0) {
      recordFailure(`${pageLabel}: ${result.openDetails} details open by default`);
    }
    if (result.missingImageAlt !== 0) {
      recordFailure(`${pageLabel}: ${result.missingImageAlt} images lack alt text`);
    }
    if (result.invalidVideos !== 0) {
      recordFailure(
        `${pageLabel}: ${result.invalidVideos} animations lack controls, source, fallback, or caption`,
      );
    }
    for (const issue of result.expandedDisclosureIssues) {
      recordFailure(`${pageLabel}: ${issue}`);
    }
    if (result.expandedDocumentOverflow) {
      recordFailure(`${pageLabel}: expanded details cause document overflow`);
    }
    for (const message of consoleErrors) {
      recordFailure(`${pageLabel}: browser console error: ${message}`);
    }
    for (const message of pageErrors) {
      recordFailure(`${pageLabel}: page error: ${message}`);
    }
    for (const message of failedRequests) {
      recordFailure(`${pageLabel}: failed request: ${message}`);
    }
    for (const message of badResponses) {
      recordFailure(`${pageLabel}: bad response: ${message}`);
    }

    // Opt-in evidence for visual debugging: capture every figure, and seek
    // real served videos rather than accepting their posters as playback.
    if (process.env.SITE_AUDIT_FIGURES === "1" && viewport.name === "wide") {
      const figures = page.locator("main figure");
      for (let index = 0; index < await figures.count(); index += 1) {
        const figure = figures.nth(index);
        if (!await figure.isVisible()) continue;
        const stem = screenshotName(pagePath, `figure-${index}`).replace(/\.png$/, "");
        await figure.screenshot({ path: path.join(artifactDir, `${stem}.png`) });
        screenshotCount += 1;
        const video = figure.locator("video");
        if (await video.count() && sameOrigin(await video.getAttribute("src"))) {
          // The simple preview server does not implement byte ranges.
          // Decode its complete response as a blob for deterministic seeking;
          // this verifies served media, not HTTP range-request support.
          await video.evaluate(async (element) => {
            const response = await fetch(element.currentSrc || element.src);
            if (!response.ok) throw new Error(`video fetch failed: ${response.status}`);
            element.src = URL.createObjectURL(await response.blob());
            element.load();
          });
          for (const fraction of [0.25, 0.75]) {
            await video.scrollIntoViewIfNeeded();
            await video.evaluate(async (element, fraction) => {
              element.muted = true;
              await element.play();
              element.pause();
              await new Promise((resolve, reject) => {
                const timer = setTimeout(() => reject(new Error("video seek timed out")), 15000);
                element.addEventListener("seeked", () => { clearTimeout(timer); resolve(); }, { once: true });
                const seek = () => { element.currentTime = fraction * element.duration; };
                if (element.readyState >= 1) seek();
                else {
                  element.addEventListener("loadedmetadata", seek, { once: true });
                  element.load();
                }
              });
              if (Math.abs(element.currentTime - fraction * element.duration) > 0.15) {
                throw new Error(`video did not reach requested frame: ${element.currentTime}/${element.duration}`);
              }
            }, fraction);
            await page.waitForTimeout(150);
            await video.screenshot({ path: path.join(artifactDir, `${stem}-video-${fraction}.png`) });
            screenshotCount += 1;
          }
        }
      }
    }

    const targetSelector = screenshotTargets.get(pagePath);
    if (targetSelector) {
      const target = page.locator(targetSelector).first();
      if ((await target.count()) === 0) {
        recordFailure(`${pageLabel}: screenshot target is missing: ${targetSelector}`);
      } else {
        await target.scrollIntoViewIfNeeded();
        await page.waitForTimeout(50);
        await page.screenshot({
          animations: "disabled",
          path: path.join(artifactDir, screenshotName(pagePath, viewport.name)),
        });
        screenshotCount += 1;
      }
    }
  } catch (error) {
    recordFailure(`${pageLabel}: ${error.stack || error.message}`);
  }
}

async function main() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || undefined,
    args: [
      "--disable-dev-shm-usage",
      "--disable-gpu",
      "--no-sandbox",
    ],
  });

  try {
    for (const viewport of viewports) {
      const context = await browser.newContext({
        deviceScaleFactor: 1,
        reducedMotion: "reduce",
        viewport: { width: viewport.width, height: viewport.height },
      });
      if (process.env.SITE_MEDIA_FIXTURE_PATH) {
        await context.route(/^https:\/\/cloud\.tugraz\.at\/.*\/animations\/[^?]+\.mp4(?:\?|$)/,
          (route) => route.fulfill({ path: process.env.SITE_MEDIA_FIXTURE_PATH, contentType: "video/mp4" }));
      }

      for (const pagePath of pages) {
        const page = await context.newPage();
        await auditPage(page, pagePath, viewport);
        await page.close();
      }

      await context.close();
    }
  } finally {
    await browser.close();
  }

  const summary = {
    externalMediaTransportFixture: Boolean(process.env.SITE_MEDIA_FIXTURE_PATH),
    pages: pages.length,
    viewports: viewports.map(({ name, width, height }) => ({ name, width, height })),
    checks: pages.length * viewports.length,
    screenshots: screenshotCount,
    failures,
  };
  fs.writeFileSync(
    path.join(artifactDir, "summary.json"),
    `${JSON.stringify(summary, null, 2)}\n`,
  );

  if (failures.length > 0) {
    console.error(JSON.stringify(summary, null, 2));
    process.exitCode = 1;
    return;
  }

  console.log(
    `site integration passed: ${summary.checks} page/viewport checks, ${summary.screenshots} screenshots`,
  );
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exitCode = 1;
});
