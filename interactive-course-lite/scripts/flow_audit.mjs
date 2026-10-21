// Flow audit: find terms that are USED before the lesson that EXPLAINS them.
// usage: node flow_audit.mjs <index.html> [--terms "LLM,token,JSON"]
// How it works: a term counts as "introduced" in the first lesson that bolds it in running text (lead,
// paragraphs, list items, callouts), because that is where the course names and explains it. For each such
// term (plus any --terms), the script finds the first lesson whose explanatory text mentions it. A mention in
// an EARLIER lesson is reported, unless the text nearby already points forward, e.g. "(tokens, lesson 4)".
// Demo cards, code panels, quizzes and SVG labels are ignored: they are UI text, not explanations.
// It is a heuristic: read each flagged line and decide (explain briefly on first use, add a pointer, or ignore).
// The visible lesson text is also written to flow_text.json next to the course for a reading pass (delete it after).
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { open, args } from "./cdp.mjs";

const a = args(); const file = a._[0];
if (!file) { console.error('usage: node flow_audit.mjs <index.html> [--terms "a,b"]'); process.exit(2); }
const p = await open(file);
const data = await p.ev(`(() => [...document.querySelectorAll("section[data-title]")].filter(s => !["intro", "finalquiz"].includes(s.id)).map(s => {
  const c = s.cloneNode(true);
  c.querySelectorAll(".code, .quizbox, script, style, .log, .card, svg, .controls").forEach(e => e.remove());
  const bold = [...c.querySelectorAll("p b, li b, .callout b, p strong, li strong")].filter(b => !b.closest("td, th"))
    .map(b => b.innerText.trim().replace(/[:.,]$/, ""));
  return { id: s.id, title: s.dataset.title, text: c.innerText.replace(/\\s+/g, " "), bold };
}))()`);
p.close();
const outJson = join(dirname(file), "flow_text.json");
writeFileSync(outJson, JSON.stringify(data, null, 1));

const STOP = new Set(("the a an and or of to in on it is are be for with by as at from this that these those not no yes all any one two " +
  "each more most very much many some what why how when where who which only also new old high low medium step steps example examples " +
  "note tip result results answer question start done first next last same different good bad right wrong").split(" "));
const isTerm = t => t.length >= 3 && t.length <= 40 && /[A-Za-z]/.test(t) && !STOP.has(t.toLowerCase()) && t.split(" ").length <= 5;
const intro = new Map();
data.forEach((s, i) => s.bold.filter(isTerm).forEach(t => { const k = t.toLowerCase(); if (!intro.has(k)) intro.set(k, { term: t, at: i }); }));
(a.terms ? String(a.terms).split(",") : []).forEach(t => { const k = t.trim().toLowerCase(); if (k && !intro.has(k)) intro.set(k, { term: t.trim(), at: data.length }); });

const esc = s => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const issues = [];
for (const [k, { term, at }] of intro) {
  const re = new RegExp(`(^|[^A-Za-z])${esc(k)}([^A-Za-z]|$)`, "i");
  for (let i = 0; i < Math.min(at, data.length); i++) {
    const m = data[i].text.match(re);
    if (!m) continue;
    const around = data[i].text.slice(Math.max(0, m.index - 90), m.index + k.length + 90);
    if (/\([^)]*lesson \d+\)/i.test(around)) break;   // already points forward, e.g. "(tokens, lesson 4)"
    issues.push({ term, usedIn: data[i].title, explainedIn: at < data.length ? data[at].title : "(never bolded)", context: "…" + around.trim() + "…" });
    break;
  }
}
console.log(`lessons: ${data.length}, introduced terms: ${intro.size}, possible early uses: ${issues.length}`);
issues.forEach(x => console.log(`\n• "${x.term}" used in [${x.usedIn}] before it's explained in [${x.explainedIn}]\n  ${x.context}`));
console.log(`\nlesson text saved to ${outJson} (delete it before committing)`);
