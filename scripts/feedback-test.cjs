#!/usr/bin/env node
"use strict";
const assert = require("node:assert/strict");
const { chromium } = require(process.env.PLAYWRIGHT_CORE_PATH || "playwright-core");
const base = process.env.SITE_BASE_URL || "http://127.0.0.1:8139/";

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_EXECUTABLE_PATH || "/usr/bin/chromium",
    headless: true,
  });
  try {
    for (const width of [390, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 900 } });
      const reports = [];
      // Test the actual click without posting an issue or requiring a login.
      // GitHub's documented query fields provide the external behavior oracle.
      await context.route("https://github.com/**/issues/new?**", async route => {
        reports.push(new URL(route.request().url()));
        await route.fulfill({ contentType: "text/html", body: "<h1>Review issue</h1>" });
      });
      const page = await context.newPage();
      await page.goto(new URL("chapters/02-debye-shielding.html?private=do-not-share", base).href);
      const section = page.getByRole("heading", { name: /Finite charge distribution/ });
      await section.evaluate(h => h.scrollIntoView({ block: "start" }));
      const sectionID = await section.getAttribute("id");
      assert.ok(sectionID, "Unlabelled sections need working feedback anchors");
      const button = page.getByRole("link", { name: /Report a problem/ });
      assert.equal(await button.count(), 1);
      assert.ok(await button.isVisible());
      const popupPromise = context.waitForEvent("page");
      await button.click();
      const popup = await popupPromise;
      await popup.waitForLoadState();
      assert.equal(reports.length, 1);
      assert.equal(reports[0].pathname, "/krystophny/plasma-skript/issues/new");
      assert.match(reports[0].searchParams.get("title"), /Finite charge distribution/);
      const body = reports[0].searchParams.get("body");
      assert.ok(body.includes(`https://krystophny.github.io/plasma-skript/chapters/02-debye-shielding.html#${sectionID}`));
      assert.ok(!body.includes("do-not-share"), "Private queries must not enter reports");
      assert.ok(!body.includes("127.0.0.1"), "Reports must use the public reading URL");
      assert.match(body, /Problem or suggestion/);
      await popup.close();

      // Newly generated section fragments must work when opened directly.
      await page.goto(new URL(`chapters/02-debye-shielding.html#${sectionID}`, base).href);
      await page.waitForFunction(id => Math.abs(document.getElementById(id).getBoundingClientRect().top) < 10, sectionID);
      await page.screenshot({ path: `/tmp/plasma-feedback-${width}.png` });

      // A selected passage chooses its own section, even outside the viewport.
      await page.getByRole("heading", { name: /Plasma parameter/ }).scrollIntoViewIfNeeded();
      await page.evaluate(() => {
        const h = document.querySelector("#intro-debye-shielding");
        const range = document.createRange(); range.selectNodeContents(h);
        const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      });
      const selectedPopupPromise = context.waitForEvent("page");
      await button.click();
      const selectedPopup = await selectedPopupPromise;
      await selectedPopup.waitForLoadState();
      const selectedURL = reports.at(-1);
      assert.match(selectedURL.searchParams.get("body"), /Selected passage/);
      assert.ok(selectedURL.searchParams.get("body").includes("#intro-debye-shielding"));
      assert.ok(selectedURL.href.length < 8000);
      await selectedPopup.close();
      await context.close();
      console.log(`Feedback click, anchors and selection verified at ${width}px`);
    }
    const context = await browser.newContext({ javaScriptEnabled: false });
    const page = await context.newPage();
    await page.goto(new URL("index.html", base).href);
    const fallback = new URL(await page.getByRole("link", { name: /Report a problem/ }).getAttribute("href"));
    assert.match(fallback.searchParams.get("body"), /https:\/\/krystophny.github.io\/plasma-skript\/index.html/);
    await context.close();
    console.log("No-JavaScript feedback fallback verified");
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
