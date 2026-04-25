const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

async function main() {
  const htmlFile = fs.readdirSync(__dirname).find((file) => file.endsWith(".html"));
  if (!htmlFile) throw new Error("No HTML file found in test directory.");

  const browser = await chromium.launch({
    headless: true,
    executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto("file:///" + path.join(__dirname, htmlFile).replace(/\\/g, "/"));

  const result = await page.evaluate(() => {
    const badTables = [...document.querySelectorAll("table")]
      .map((table, index) => {
        const heads = table.tHead?.rows[0]?.cells.length || 0;
        const bad = [...(table.tBodies[0]?.rows || [])].filter((row) => row.cells.length !== heads).length;
        return { index, heads, bad };
      })
      .filter((item) => item.bad);

    return {
      title: document.title,
      chapters: document.querySelectorAll("article.chapter").length,
      visuals: document.querySelectorAll(".viz").length,
      badTables,
      chapter01Text: document.querySelector("#chapter-01 .chapter-body")?.textContent.slice(0, 120),
      external: [...document.querySelectorAll("script[src],link[href],img[src]")].map((el) => el.src || el.href),
      indexDisplayBefore: getComputedStyle(document.querySelector("#index")).display,
    };
  });

  await page.click("#sprintMode");
  result.sprint = await page.evaluate(() => ({
    sprint: document.body.classList.contains("sprint"),
    indexVisible: getComputedStyle(document.querySelector("#index")).display !== "none",
    supplementHidden: document.body.classList.contains("hide-supplement"),
    buttonText: document.querySelector("#sprintMode").textContent,
  }));

  await page.fill("#search", "伯努利");
  await page.waitForTimeout(180);
  result.search = await page.evaluate(() => ({
    visibleChapters: [...document.querySelectorAll("article.chapter")]
      .filter((el) => !el.classList.contains("hidden"))
      .map((el) => el.id),
    visibleFormulaRows: [...document.querySelectorAll(".formula-table tbody tr")]
      .filter((el) => !el.classList.contains("hidden")).length,
    visiblePaths: [...document.querySelectorAll(".path-card")]
      .filter((el) => !el.classList.contains("hidden")).length,
    status: document.querySelector("#resultStatus").textContent,
  }));

  await page.click('[data-filter="实验"]');
  result.filterWithSearch = await page.evaluate(() => ({
    visibleChapters: [...document.querySelectorAll("article.chapter")]
      .filter((el) => !el.classList.contains("hidden"))
      .map((el) => el.id),
    visibleCards: [...document.querySelectorAll(".chapter-card")]
      .filter((el) => !el.classList.contains("hidden"))
      .map((el) => el.dataset.target),
    active: [...document.querySelectorAll("#filters button")]
      .filter((button) => button.classList.contains("active"))
      .map((button) => button.textContent),
  }));

  await page.fill("#search", "");
  await page.waitForTimeout(180);
  result.filterOnly = await page.evaluate(() => ({
    visibleChapters: [...document.querySelectorAll("article.chapter")]
      .filter((el) => !el.classList.contains("hidden"))
      .map((el) => el.id),
    visibleCards: [...document.querySelectorAll(".chapter-card")]
      .filter((el) => !el.classList.contains("hidden"))
      .map((el) => el.dataset.target),
  }));

  await page.click(".quiz");
  result.quiz = await page.evaluate(() => ({
    text: document.querySelector(".quiz").textContent,
    expanded: document.querySelector(".quiz").getAttribute("aria-expanded"),
    answerVisible: document.querySelector(".answer").classList.contains("show"),
  }));

  await browser.close();
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
