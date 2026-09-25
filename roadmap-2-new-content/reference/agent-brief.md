# Writer brief (shared by all writer agents)

Project folder: /home/user/webinar-to-calls/roadmap-2-new-content  (ignore everything else in the repo; it is a separate project)

Read these first, fully:
1. reference/brief.md  (the production brief; your items' "Description" and "Topics to include" are mandatory coverage)
2. reference/writing-guide.md  (voice, accuracy, structure; follow exactly)
3. reference/recurring-examples.md  (canonical numbers; use them verbatim, never change them)
4. tools/examples.py if you need to derive a new figure from the canonical assumptions (run it with python3; do your own arithmetic in python, never in your head)

Today is 2026-09-25. Tracker titles were verified against the live Google Sheet today.

Your job: write complete teaching content for your assigned items, one Markdown file per item at parts/<NN>-<CODE>.md (NN given below). This is the actual lesson material a teacher records from, not an outline.

Research: verify every rule/product/tax/financing claim with primary sources. Direct fetches of most official sites are blocked; use WebSearch with allowed_domains restricted to the official domain (airbnb.com, irs.gov, consumerfinance.gov, fanniemae.com, nyc.gov, lacity.gov, sba.gov, cpsc.gov, help.vrbo.com, kiavi.com, etc.) and read what the tool reports. WebFetch may work for some domains; try it once, don't loop on blocked ones. Prefer the URLs given in the brief. Only cite URLs that appeared in search results or the brief. Write a sources log at parts/sources-<GROUP>.md with a table: Claim | URL | How verified (search summary / fetched / brief-provided, not independently opened) | Date | Notes. Add an "Unresolved" section listing anything you could not confirm and who must confirm it.

Quality bar:
- Every lesson has: learning outcome; full teaching narrative in numbered subsections; the recurring example worked with visible calculations (use Alder Street for Part One arbitrage lessons, Cedar Ridge for STR Concierge lessons; either or both for resources); a practical exercise or decision tool the student fills in; "Who confirms what"; a transition to the next lesson; sources.
- Numbers you add must be marked (assumption) and must be computed with python. Keep them consistent with the canonical file.
- Conditional phrasing for rules. Links right beside the claims they support.
- Keep Preston's lesson distinct from Sam's demos; hand off by code.
- Follow the voice rules strictly: no em dashes or en dashes at all (search your output for "—" and "–" before finishing and remove them), no banned words, no invented Preston stories or client results.

When finished, reply with: files written, word counts (wc -w), and a bullet list of unresolved facts. Do not write anything outside parts/.
