---
name: ai-news-weekly
description: Generate a strict, fact-only weekly AI news briefing covering the last 7 days — foundation models, agents, research papers, open-source releases, dev tools, infra/GPUs, benchmarks, safety, regulation, funding, acquisitions, and enterprise AI announcements. Use whenever the user asks for a "weekly AI news" briefing, "AI news roundup", "what happened in AI this week", "AI news digest", or similar — even if they just say "give me the AI news" or "/ai-news" without specifying a date range. Requires live web search; never answer from memory since the report window is always the trailing 7 days from today. Do not use for general AI questions, single-topic deep dives, or news older than 7 days — this skill is specifically for the recurring weekly-briefing format.
---

# Weekly AI News Briefing

Produces a fact-only briefing of significant AI developments from the last 7 days, in a fixed output format, sourced primarily from official channels. This is a research + verification task, not a summarization-from-memory task — everything in the report must come from a live search performed during this conversation, since Claude's training data cannot contain this week's news.

## Step 1: Compute the reporting window

Get today's actual date (check the current date given in context, or run `date -u +%Y-%m-%d` if unsure). The reporting window is **today minus 6 days → today, inclusive, in UTC**, unless a specific source explicitly timestamps an announcement in another timezone (in which case convert or note it, using judgment — don't over-engineer this).

State the resolved window (e.g. "Reporting Window: 2026-07-11 → 2026-07-17") near the top of the output so the user can see exactly what was covered.

Never include an item whose *original* publication/announcement date falls outside this window, even if it's still being widely discussed. A follow-up article about a launch from two weeks ago doesn't count — only the original announcement date matters.

## Step 2: Search systematically, don't rely on general search alone

### Step 2a: Index sweep — FETCH index pages, don't search. Run this FIRST.

A lab-by-lab sweep only finds labs already on a list, so a significant release from a lab you've never heard of is invisible to it. Broad searches don't fix this: **search ranks by popularity and backlinks, so a two-day-old launch from an unknown lab loses to SEO roundups about the big labs.** This has been verified — generic and event-word queries both failed to surface a major small-lab model release that was, at that same moment, the most-read article on TechCrunch's AI page.

The mechanism that works is **fetching editorial index pages and reading every headline on them**. An index is chronological, not ranked, so everything the desk published appears regardless of how much traffic it got.

**Do this:** `web_fetch` at least **three** of these index pages in full and read *every* headline, not just the top few:

- `https://techcrunch.com/category/artificial-intelligence/` — strongest single source for small-lab and startup launches
- `https://aiweekly.co/ai-news-today` — 48-hour cross-industry river, strong on Chinese labs and infra
- The Register AI channel, VentureBeat AI, The Verge AI — any two
- `https://huggingface.co/models?sort=trending` and Hugging Face Daily Papers — for open-weight and research releases

These are **discovery-only**. Never cite them. For each headline that looks like a real announcement in the window, go to the announcing organization's own primary source and apply the Step 3 checks as normal.

Then collect the organization name from every candidate. **Any organization not already in the lab list below gets its own dedicated search.**

Budget note: index fetches are the highest-yield calls in this whole skill — worth far more than an equivalent number of searches. Spend tokens here and economize on the lab-by-lab sweep, not the other way round.

### Step 2b: Lab-by-lab and category sweep

A handful of generic "AI news this week" searches will surface mostly secondary reporting and miss primary sources. Instead, search source-by-source and category-by-category so coverage is actually comprehensive. As a starting point, check:

**Labs / vendors:** OpenAI, Anthropic, Google / Google DeepMind, Microsoft, Meta AI, NVIDIA, Hugging Face, Mistral AI, xAI, Cohere, AI2, Stability AI, GitHub (Copilot/AI features), Thinking Machines Lab. This list is not exhaustive and well-funded frontier labs are added faster than any static list keeps up — if a Hugging Face, arXiv, or general search surfaces a significant release from a lab not listed here, follow up with a dedicated search on that lab directly rather than skipping it.

**Also sweep every run, without exception:** Chinese labs (DeepSeek, Alibaba Qwen, Moonshot, Zhipu/Z.AI, MiniMax, StepFun) and open-weight releases (Mistral, Ai2, Meta, Hugging Face Hub, Gemma). These are routinely missed because they publish outside the US lab blog circuit.

**Official video channels:** Some launches are announced primarily via video (a keynote, product demo, or launch stream) rather than a blog post. Check the official YouTube channels of OpenAI, Anthropic, and Google DeepMind for anything published in the window — search e.g. "OpenAI YouTube July 2026" or "site:youtube.com OpenAI [topic]". These three official channels are the *only* video sources this skill treats as trusted — no third-party tech-news channels, reaction/commentary channels, or news-aggregator channels, regardless of how reputable they seem. A third-party video *about* a lab's announcement is not itself a source; find and cite the lab's own post or video instead.

Direct video fetches frequently fail or get rate-limited. When that happens, don't guess at the video's content from its title alone — confirm the actual claims either from the video's own description/metadata in search results, or from the same-day written post the lab almost always publishes alongside a launch video. If neither is available to confirm specifics, drop the item.

**Research & venues:** arXiv (cs.AI / cs.CL / cs.LG new submissions), NeurIPS, ICML, ICLR announcements

**Other:** relevant government/regulatory publications (e.g. EU AI Office, NIST, UK AI Safety Institute) for policy items, and major funding/M&A trackers only when no primary source (official blog post, SEC filing, press release) exists

Run enough distinct searches to cover this properly — this is a broad research task, not a single-fact lookup. Search each major lab individually (e.g. "OpenAI announcement July 2026", "Anthropic blog July 2026") rather than one combined query, since combined queries return shallow results for everyone. For anything that looks significant, use web_fetch on the actual primary source page to confirm the date and details before including it — don't trust a snippet alone.

Ignore anything not related to AI/ML (general tech news, non-AI product launches, unrelated business news).

## Step 3: Apply the verification rules

Every item included must satisfy all of the following. If any one fails, drop the item rather than including it with caveats.

- **Date check** — original publication/announcement date falls inside the window.
- **Primary-source check** — sourced from an official blog, press release, official docs, official GitHub repo, arXiv, a conference site, a government publication, or an official video on the lab's own verified YouTube channel (OpenAI, Anthropic, or Google DeepMind only — see the Official video channels note in Step 2) whenever one exists. Only fall back to reputable tech press (with no primary source available) as a last resort, and note that it's secondary if so. For multi-party announcements (e.g. a joint venture or deal announced by two or more companies together), a wire-service distribution of the actual joint press release (BusinessWire, GlobeNewswire, PR Newswire) counts as primary — it's the companies' own release, just distributed through a wire, not third-party coverage of it.
- **Officiality check** — it's an actual announcement, not a rumor, leak, forecast, or "sources say" report.
- **Verifiability check** — facts are corroborated, not speculative.
- **Direct-URL check** — the URL must resolve straight to the specific article, post, or press release being cited. Never cite a homepage, newsroom index, blog listing, "/news/" or "/blog/" root, category/tag page, or any other hub page — even if that hub page is where the article was discovered. If a search or fetch only turns up a hub page, find and use the individual article's own permalink (fetch the hub page and pull the specific link if needed) before including the item. If no direct permalink can be found, drop the item rather than citing the hub page.

Also exclude on sight: editorials/opinion pieces, duplicate reports of the same news (keep only the earliest official announcement), pure follow-ups with no new information, hiring news, stock-price commentary, and anything non-AI.

**When a paper + GitHub repo + blog post all launch together**, cite the blog post as primary, treat arXiv as secondary, and only mention the GitHub repo if it adds something the blog doesn't cover — don't cite all three as separate items.

## Step 4: Rank and assemble

Sort items by:
1. Significance (frontier model releases, **a genuinely new model class, architecture, or training method — from any organization, however small or unknown**, major research breakthroughs, major open-source releases, new infra, large funding rounds/acquisitions, and major regulation outrank minor feature updates, small SDK point-releases, and routine product tweaks). Novelty outranks the size of the organization announcing it: a first release from an unknown lab that introduces a new approach ranks above a routine point-release from a frontier lab.
2. Within similar significance, newest publication date first

Produce a maximum-quality list — if fewer than 10 items genuinely qualify, report only those; don't pad with borderline items to hit a round number. If literally nothing qualifies, say so explicitly (exact wording below) rather than stretching the window or the criteria.

## Output format

Use this exact structure. Keep summaries to one factual sentence — no analysis, no speculation, no predictions, no opinions.

```
# 🤖 Top AI News (Last 7 Days)
Reporting Window: YYYY-MM-DD → YYYY-MM-DD (UTC)

---

📰 [Headline]
Category: [one of the 15 scope categories]
Organizations: [org(s) involved]
Published: YYYY-MM-DD
Summary: [one factual sentence]
Original Source: [direct URL]

---

[repeat per item]

# Weekly Summary

| Metric | Count |
|--------|------:|
| Total news items | |
| Model releases | |
| Research papers | |
| Open-source projects | |
| Product announcements | |
| Infrastructure updates | |
| Business/Funding | |
| Safety/Regulation | |

# Sources Checked
[list the primary sources actually searched this run, and the discovery queries used]

# Not Checked
[sources, labs, regions, or categories skipped this run — state them plainly so the reader knows where the blind spots are. If nothing was skipped, say so.]

# Dropped Candidates
[items that surfaced but didn't make the cut, each with a one-line reason: outside window / no primary source / rumor or unofficial / duplicate. This makes near-misses visible instead of silent.]
```

If no qualifying announcements exist for the window, skip straight to stating: *"No significant AI announcements satisfying the reporting criteria were officially published during the reporting window."*

## Things to double check before sending

- Every date is inside the window — re-verify anything you're not 100% sure about rather than assuming.
- No item appears twice under different headlines.
- No item is analysis, opinion, hiring news, or stock commentary.
- Every URL is a direct link to the specific primary-source article, fetched and confirmed — not a guessed URL, and not a homepage/newsroom-index/blog-listing/hub page (e.g. `nvidianews.nvidia.com` alone is wrong; the specific press-release permalink under it is right).
- The summary counts table actually matches the items listed above it.
- **Did you actually FETCH at least three index pages in Step 2a, and read every headline on them?** If you only ran searches, stop and do the fetches now — searching is a proven failure mode for this skill and will silently drop small-lab releases.
- **Did the index sweep surface at least one organization that isn't in the lab list?** If it surfaced none, you probably skimmed the index instead of reading it through. Re-read, or fetch another index page.
- The "Not Checked" and "Dropped Candidates" sections are filled in, not left empty by default.
