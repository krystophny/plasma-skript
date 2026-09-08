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
  "/chapters/02-single-particle-motion.html",
  "/chapters/03-kinetic-theory.html",
  "/chapters/04-moments.html",
  "/chapters/05-multiple-fluids.html",
  "/chapters/06-mhd.html",
  "/chapters/07-collisions-conductivity.html",
  "/chapters/08-diffusion.html",
  "/chapters/09-introduction-waves.html",
  "/chapters/10-cold-magnetized-waves.html",
  "/chapters/11-finite-temperature-waves.html",
  "/chapters/12-hot-plasma-waves.html",
  "/chapters/13-sheaths-probes.html",
  "/appendices/mathematical-toolkit.html",
];

const viewports = [
  { name: "mobile", width: 390, height: 900 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "wide", width: 1440, height: 1200 },
];

const screenshotTargets = new Map([
  ["/chapters/01-introduction.html", "main figure:has(svg)"],
  ["/chapters/04-moments.html", 'main math[display="block"]'],
  [
    "/chapters/10-cold-magnetized-waves.html",
    'main > div[id^="frame-wrapper-"]',
  ],
  ["/chapters/13-sheaths-probes.html", "main video"],
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
      message.text() !== "Failed to load resource: the server responded with a status of 404 (File not found)"
    ) {
      consoleErrors.push(message.text());
    }
  });
  page.on("pageerror", (error) => {
    pageErrors.push(error.message);
  });
  page.on("requestfailed", (request) => {
    if (sameOrigin(request.url()) && !request.url().endsWith("/favicon.ico")) {
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
        return !video.hasAttribute("controls") || !hasSource || !hasFallback || !hasCaption;
      });

      return {
        documentWidth: documentElement.scrollWidth,
        documentClientWidth: documentElement.clientWidth,
        bodyWidth: body?.scrollWidth ?? 0,
        bodyClientWidth: body?.clientWidth ?? 0,
        openDetails: details.filter((detail) => detail.open).length,
        missingImageAlt: images.length,
        invalidVideos: invalidVideos.length,
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
