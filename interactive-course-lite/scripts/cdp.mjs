// Minimal headless-Chrome driver over the DevTools protocol (Node 22+, no npm packages).
// open(url, { width, height, scale }) -> { ev, send, sleep, errors, close }
//   ev(expr)   evaluates JS in the page (awaits promises, returns JSON values; { __err } on exceptions)
//   send(m,p)  raw DevTools command, e.g. send("Page.captureScreenshot", {...})
//   errors     page exceptions and console.error messages collected so far
// Chrome is found automatically; set CHROME=<path> to override.
import { spawn } from "node:child_process";
import { mkdtempSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const CANDIDATES = [
  process.env.CHROME,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
].filter(Boolean);

export function chromePath() {
  const p = CANDIDATES.find(c => existsSync(c));
  if (!p) throw new Error("Chrome/Edge not found. Set CHROME=<path to chrome executable>.");
  return p;
}

// Turn a local path or URL into something Chrome can load.
export function toUrl(p) {
  if (/^(https?|file|about|data):/.test(p)) return p;
  const abs = p.replace(/\\/g, "/");
  return "file:///" + abs.replace(/^\/+/, "");
}

export async function open(url, { width = 1280, height = 1000, scale = 1 } = {}) {
  const port = 9300 + Math.floor(Math.random() * 600);
  const prof = mkdtempSync(join(tmpdir(), "course-cdp-"));
  const chrome = spawn(chromePath(), ["--headless=new", "--disable-gpu", "--hide-scrollbars",
    `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, "about:blank"]);
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  let targets;
  for (let i = 0; i < 75; i++) { try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
  if (!targets) throw new Error("Chrome did not start");
  const page = targets.find(t => t.type === "page");
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => (ws.onopen = r));
  let id = 0; const pend = new Map(); const errors = [];
  ws.onmessage = e => {
    const m = JSON.parse(e.data);
    if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
    if (m.method === "Runtime.exceptionThrown") errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
    if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error") errors.push("console.error: " + m.params.args.map(a => a.value ?? a.description).join(" "));
  };
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async expr => {
    const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.result?.exceptionDetails) return { __err: r.result.exceptionDetails.exception?.description };
    return r.result?.result?.value;
  };
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: scale, mobile: false });
  await send("Page.enable");
  await send("Page.navigate", { url: toUrl(url) });
  // wait until the page has fully loaded (big courses can take a few seconds), then let scripts settle
  await sleep(300);
  for (let i = 0; i < 100; i++) { if ((await ev("document.readyState")) === "complete") break; await sleep(150); }
  await sleep(400);
  const close = () => { try { ws.close(); } catch {} chrome.kill(); setTimeout(() => { try { rmSync(prof, { recursive: true, force: true }); } catch {} }, 500); };
  return { ev, send, errors, sleep, close };
}

// Small CLI-argument helper shared by the scripts: --key value pairs plus positionals.
export function args(argv = process.argv.slice(2)) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) { const k = argv[i].slice(2); const v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true; out[k] = v; }
    else out._.push(argv[i]);
  }
  return out;
}

// Wait until no element in the page is busy (DS.run sets data-busy while a demo animates).
export const waitIdleJS = (ms = 20000) => `(async () => { await new Promise(r => setTimeout(r, 60)); const t = Date.now();
  while (document.querySelector("[data-busy]") && Date.now() - t < ${ms}) await new Promise(r => setTimeout(r, 25));
  return !document.querySelector("[data-busy]"); })()`;

// Parse the final quiz's correct answer indexes from the course source.
export function finalAnswers(src) {
  const start = src.indexOf("const finalQs = [");
  const end = src.indexOf("\n  ];", start);
  return [...src.slice(start, end).matchAll(/answer:\s*(\d+)/g)].map(m => +m[1]);
}
