// Screenshot part of a course page (for README images and visual checks).
// usage: node shot.mjs <index.html> <out.png> <selector> [--end <selector>] [--theme light|dark]
//        [--width 1280] [--scale 1|2] [--click "<button selector>"] [--pre "<js>"] [--hide "<css selector>"]
//   --end    capture from <selector> down to the bottom of this second element
//   --click  click a button first and wait until its demo finishes (data-busy cleared)
//   --pre    run JS first (may return a promise), e.g. to pick a mode or fill an input
//   --hide   hide matching elements (visibility) so they don't show in the shot
// Tip: use --width 390 for a phone check and --theme dark for dark mode.
import { writeFileSync } from "node:fs";
import { open, args, waitIdleJS } from "./cdp.mjs";

const a = args(); const [file, out, sel] = a._;
if (!sel) { console.error("usage: node shot.mjs <index.html> <out.png> <selector> [options]"); process.exit(2); }
const p = await open(file, { width: +(a.width || 1280), height: 1000, scale: +(a.scale || 1) });
const { ev, send, sleep } = p;
const J = JSON.stringify;
await ev(`document.documentElement.dataset.theme = ${J(a.theme || "light")}; document.documentElement.style.scrollBehavior = "auto"; true`);
if (a.hide) await ev(`(() => { const s = document.createElement("style"); s.textContent = ${J(a.hide + " { visibility: hidden !important; }")}; document.head.append(s); return 1; })()`);
if (a.pre) { const r = await ev(a.pre); if (r && r.__err) console.error("pre:", r.__err); await sleep(300); }
if (a.click) {
  const ok = await ev(`(() => { const b = document.querySelector(${J(a.click)}); if (!b) return "missing"; if (b.disabled) return "disabled"; DS.speed = 40; b.click(); return "clicked"; })()`);
  if (ok !== "clicked") console.error("click:", ok, a.click);
  await ev(waitIdleJS()); await sleep(400);
  if (a.debug) console.error("status after click:", await ev(`(document.querySelector(${J(a.click)}).closest(".card") || document.body).querySelector(".status")?.innerText`));
}
const r = await ev(`(() => {
  const s = document.querySelector(${J(sel)}), e = document.querySelector(${J(a.end || sel)});
  if (!s || !e) return null;
  window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 170);
  const A = s.getBoundingClientRect(), B = e.getBoundingClientRect();
  return { x: Math.min(A.x, B.x), y: A.y + scrollY, w: Math.max(A.right, B.right) - Math.min(A.x, B.x), h: B.bottom - A.top };
})()`);
if (!r) { console.error("selector not found:", sel, a.end || ""); p.close(); process.exit(1); }
await sleep(300);
const s = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
  clip: { x: Math.max(0, r.x - 8), y: Math.max(0, r.y - 8), width: r.w + 16, height: Math.min(r.h + 16, 4000), scale: 1 } });
writeFileSync(out, Buffer.from(s.result.data, "base64"));
console.log("saved", out, Math.round(r.w + 16) + "x" + Math.round(r.h + 16), "errors:", p.errors.length ? p.errors : "none");
p.close();
