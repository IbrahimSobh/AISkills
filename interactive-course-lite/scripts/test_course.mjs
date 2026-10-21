// End-to-end check of a course file in headless Chrome.
// usage: node test_course.mjs <path/to/index.html> [--lesson-qs 3]
// Checks: no JS errors on load; sidebar built from every section; each lesson has a quiz with the expected
// number of questions; every demo button runs without errors (at high speed); the final quiz fails below
// the pass mark and passes at full marks; the certificate renders, toggles the score and downloads a PNG;
// no {{PLACEHOLDER}} text is left; the page has an embedded tab icon (scripts/favicon.py); demo captions
// don't cover the picture (desktop and 390px). Prints a report and
// exits 1 on any failure.
import { readFileSync } from "node:fs";
import { open, args, waitIdleJS, finalAnswers } from "./cdp.mjs";

const a = args(); const file = a._[0];
if (!file) { console.error("usage: node test_course.mjs <index.html> [--lesson-qs 3]"); process.exit(2); }
const src = readFileSync(file, "utf8");
const expectQs = +(a["lesson-qs"] || 3);
const fails = []; const warn = [];
const check = (ok, msg) => { console.log((ok ? "  ok   " : "  FAIL ") + msg); if (!ok) fails.push(msg); };

const leftovers = [...new Set((src.match(/\{\{[^}]{0,60}/g) || []).map(s => s.slice(0, 40)))];
check(!leftovers.length, `no {{placeholders}} left${leftovers.length ? ": " + leftovers.slice(0, 8).join(" | ") : ""}`);
check(/<link rel="icon"[^>]*href="data:image\/png;base64,/.test(src), "has an embedded tab icon (run: python -I scripts/favicon.py <index.html>)");

const p = await open(file, { width: 1280, height: 1000 });
const { ev, sleep } = p;
await sleep(500);
await ev(`DS.speed = 40; true`);

const info = await ev(`(() => {
  const secs = [...document.querySelectorAll("section[data-title]")];
  return { titles: secs.map(s => s.dataset.title), ids: secs.map(s => s.id), nav: document.querySelectorAll("#nav a").length,
    lessons: secs.filter(s => s.querySelector(".quizbox")).map(s => ({ id: s.id, qs: s.querySelectorAll(".quizbox .q").length })) };
})()`);
console.log("sections:", info.titles.join(" | "));
check(info.nav === info.titles.length, `sidebar has a link for every section (${info.nav}/${info.titles.length})`);
check(info.ids.includes("intro") && info.ids.includes("finalquiz"), "has #intro and #finalquiz sections");
for (const l of info.lessons) check(l.qs === expectQs, `lesson #${l.id} quiz has ${expectQs} questions (found ${l.qs})`);

// Smoke-test every demo button outside quizzes, the glossary filters and the final quiz.
const btnCount = await ev(`(() => { window.__btns = [...document.querySelectorAll("section button")].filter(b =>
  !b.closest(".quizbox, .quiz, #finalquiz, #certBox") ); return __btns.length; })()`);
let clicked = 0;
for (let i = 0; i < btnCount; i++) {
  const r = await ev(`(async () => { const b = __btns[${i}]; if (!b || b.disabled || !b.isConnected) return "skip"; b.scrollIntoView({ block: "center" }); b.click(); return "ok"; })()`);
  if (r === "ok") { clicked++; const idle = await ev(waitIdleJS()); if (!idle) warn.push(`demo still busy 20 s after button ${i}`); }
}
check(p.errors.length === 0, `${clicked} demo buttons clicked with no JS errors${p.errors.length ? ": " + p.errors.slice(0, 3).join(" | ") : ""}`);

// Final quiz: fail case, then pass case.
const ans = finalAnswers(src);
const finalCount = await ev(`document.querySelectorAll("#finalQuizBox .q").length`);
check(ans.length === finalCount && finalCount > 0, `final quiz has ${finalCount} questions and ${ans.length} answers parsed`);
const answerAll = wrongN => `(async () => { const A = ${JSON.stringify(ans)};
  const qs = [...document.querySelectorAll("#finalQuizBox .q")];
  qs.forEach((q, i) => { const n = q.querySelectorAll(".opts button").length; q.querySelectorAll(".opts button")[i < ${wrongN} ? (A[i] + 1) % n : A[i]].click(); });
  await new Promise(r => setTimeout(r, 200)); return document.getElementById("certBox").innerText; })()`;
const reset = `(() => { [...document.querySelectorAll("#finalQuizBox button")].find(b => b.textContent.includes("Try again")).click(); return 1; })()`;
const failText = await ev(answerAll(Math.ceil(ans.length * 0.2) + 1));
check(/Not yet/.test(failText), "final quiz below the pass mark shows 'Not yet'");
await ev(reset);
const passText = await ev(answerAll(0));
check(/Passed/.test(passText), "final quiz at full marks shows 'Passed'");
const cert = await ev(`(async () => {
  const box = document.getElementById("certBox");
  const inp = box.querySelector("input[type=text]"); inp.value = "Test Learner";
  [...box.querySelectorAll("button")].find(b => b.textContent.includes("Get my certificate")).click();
  await new Promise(r => setTimeout(r, 300));
  const c = box.querySelector(".cert"); if (!c) return { ok: false };
  const withScore = /Score:/.test(c.innerText);
  box.querySelector("input[type=checkbox]").click(); await new Promise(r => setTimeout(r, 200));
  const without = !/Score:/.test(box.querySelector(".cert").innerText);
  // capture the PNG download instead of saving it
  let bytes = 0; const orig = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () { if (this.download) { fetch(this.href).then(r => r.blob()).then(b => (bytes = b.size)); } else orig.call(this); };
  [...box.querySelectorAll("button")].find(b => b.textContent.includes("Download as image")).click();
  for (let i = 0; i < 60 && !bytes; i++) await new Promise(r => setTimeout(r, 100));
  HTMLAnchorElement.prototype.click = orig;
  return { ok: true, withScore, without, bytes, text: c.innerText.replace(/\\s+/g, " ").slice(0, 160) };
})()`);
check(cert.ok, "certificate renders after passing");
check(cert.withScore && cert.without, "score can be shown or hidden on the certificate");
check(cert.bytes > 20000, `certificate downloads as a PNG (${cert.bytes} bytes)`);
check(p.errors.length === 0, `no JS errors in total${p.errors.length ? ": " + p.errors.slice(0, 3).join(" | ") : ""}`);
p.close();

// Demo captions must not cover what the demo draws, on desktop and on a phone.
const CAPTION_JS = `(() => {
  const out = [];
  document.querySelectorAll(".viz .caption").forEach(c => {
    const cb = c.getBoundingClientRect(), viz = c.closest(".viz"), vb = viz.getBoundingClientRect();
    let hit = null;
    viz.querySelectorAll("*").forEach(el => {
      if (hit || el === c || c.contains(el) || el.contains(c)) return;
      if (el.children.length && !(el instanceof SVGTextElement)) return;
      if (["svg", "g", "defs", "clippath", "mask", "lineargradient", "stop", "marker", "tspan", "title"].includes(el.tagName.toLowerCase())) return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height || (r.width > vb.width * 0.9 && r.height > vb.height * 0.5)) return;
      const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.opacity === "0") return;
      if (Math.min(cb.bottom, r.bottom) - Math.max(cb.top, r.top) > 1 && Math.min(cb.right, r.right) - Math.max(cb.left, r.left) > 1) hit = el.tagName.toLowerCase();
    });
    if (hit) out.push((c.closest("section")?.dataset.title || "?") + ": " + c.textContent.slice(0, 40));
  });
  return out;
})()`;
for (const width of [1280, 390]) {
  const q = await open(file, { width, height: 900 });
  await q.sleep(700);
  const covered = (await q.ev(CAPTION_JS)) || [];
  check(!covered.length, `demo captions don't cover the picture at ${width}px${covered.length ? ": " + covered.slice(0, 4).join(" | ") : ""}`);
  q.close();
}
warn.forEach(w => console.log("  warn " + w));
console.log(fails.length ? `\n${fails.length} check(s) failed` : "\nall checks passed");
process.exit(fails.length ? 1 : 0);
