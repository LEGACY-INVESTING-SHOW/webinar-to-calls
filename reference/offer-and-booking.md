# Offer context, booking links & open questions

This file holds the **core offer facts** (what the thing is, who qualifies, the call, the
discount, compliance), the **booking links** (which link to use per situation), the
**do-not-say guardrails**, and the team's **open questions**. When a lead asked a question,
answer it briefly from the facts here plus correct general finance/tax knowledge, obey the
"Restricted information" list below, then drive to the call.

---

# Part 1 — Offer context + core facts

## What this is
Legacy Investing Show runs a free live **personal finance masterclass** (front-end name; the
program it leads to is the **Legacy Wealth Blueprint / LWB**), hosted by Preston Seo. It
teaches W-2 earners, 1099/self-employed, business owners, and retirees how to legally reduce
taxes and build long-term wealth (tax strategy, real estate / short-term rentals, retirement
structuring, entity setup). The program runs on a 5S framework: SLASH, SPOT, SHIFT, STACK,
SHIELD.

The next step offered at the end is a **free 1-on-1 strategy call**, booked by first filling a
30-second application at **managemoney101.com**. On that call the team reviews the person's
income, tax situation, and goals and shows what specifically could work for them.

## The program (what the call leads to)
- Not a course. The person is hiring a team that builds a **personalized 25–50 page wealth
  plan** for their situation, then provides **1-on-1 coaching/implementation**.
- Family membership is included — one investment covers a couple.
- A vetted network of tax professionals, attorneys, cost-segregation firms, and lenders is
  available to clients.

## Who it's built for (qualification)
- Built for people earning roughly **$100,000/year or more** with enough income and tax
  liability to make the strategies worth implementing.
- If someone clearly states they earn well under $100k, don't push the program. Be kind and
  invite them to future free trainings/resources; don't promise it's a fit. (The parser routes
  these to manual review rather than auto-emailing.)

## The call itself (reposition this in every email)
- It is **free**. About **30 minutes**, 1-on-1 with a strategist.
- It's an **application call**, not a hard pitch — they look at your numbers and see if it's a
  mutual fit. If it's not a fit, you still leave with clarity.
- Before the call, you get a short personalized video walkthrough based on your application.

## Pricing & discount (what may be said in writing)
- **Never state or invent a program price** — it isn't published; it's covered on the call.
- May be mentioned: the call itself is free; there are pay-as-you-implement options with 0%
  financing; people who book and join from a live training get **$2,000 off**.
- Never state a specific dollar/ROI guarantee in writing. If a lead asks about guarantees,
  refunds, or risk, keep it high-level (the call covers specifics) and promise nothing.

## Hard compliance lines (always)
- No guaranteed returns, no "you will save $X," no specific tax/legal/financial advice as a
  recommendation. Educational framing only.
- The call = personalized review, not advice. When a question needs real nuance, give a short
  safe answer and route to the call.

## Restricted information — never put these in an email
- Exact program prices, bundle prices, payment schedules, or internal offer architecture.
- Refund, cancellation, chargeback, legal-agreement, or arbitration terms.
- Specific dollar or ROI guarantees, or "you will save / make $X" claims.
- Individualized tax, legal, or financial advice as a recommendation (e.g. "you should set up
  an S-corp"). Explain a concept generally if helpful, then route the specifics to the call.
- Invented offer facts, credentials, results, or personal details about the lead.
- Promises about replays, slides, freebies, or bonuses beyond what's confirmed in this file.

---

# Part 2 — Booking links

The follow-up emails put a link in front of every lead. Use the right one for the situation.

## Primary link (use in almost every email)
**https://www.managemoney101.com/**

This is the **application page**. The lead fills out a 30-second application, then gets
redirected to choose a call time. This is the standard next step we want everyone to take.

## Backup link — ONLY for people who already applied and are stuck booking
**https://www.managemoney101.com/bookasessionworkshop**

Use this when a lead says they already filled out the application but are hitting an error,
can't find a time, got the wrong time slot, or otherwise can't get the booking to complete.
It takes them straight to the scheduler. Do NOT lead with this link for fresh leads — they
should apply first via the primary link.

## Second backup — application form mirror (if managemoney101.com itself won't load)
**https://form.typeform.com/to/DER4J5aJ**

This is the same application as the primary link, hosted on Typeform. Offer it if someone
reports the main site is blocked (e.g. a Norton/antivirus or firewall block on
managemoney101.com — this happened in chat). Apply here, then the team helps them book.

## Replay link — for "will I get the recording / can I rewatch?"
**https://www.managemoney101.com/replay**

Share this when a lead asks about the recording, replay, or rewatching the masterclass. Still
drive to the call as the main next step — the replay supports the booking, it doesn't replace it.

## Next live webinar — register link + schedule
**https://www.managemoney101.com/fbmasterclass**

We run the masterclass **three times a week**, all Eastern time:
- **Tuesday — 7:00 PM ET**
- **Thursday — 7:00 PM ET**
- **Sunday — 2:00 PM ET**

When inviting a lead to the next live session, don't guess the date. Run the helper to get the
correct next upcoming session for the current date/time, then name that date in the email:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/next_webinar.py"
```
It returns the next session in Eastern time (e.g. "Thursday, June 18 at 7:00 PM EDT") plus this
register link. (The label shows EST/EDT correctly by season — in summer it reads EDT, which is
the accurate name for 7 PM Eastern.) Use it for win-back, "I missed it / came in late," and
"is there another date?" leads. The booking link stays the primary CTA; the next live session is
a secondary option for people not ready to book a 1:1 yet.

## Which link, by situation
- Fresh engaged lead, never booked → **primary** (managemoney101.com).
- "How do I book / where's the link?" → **primary**.
- "I applied but can't book / wrong time / no times work" → **backup** (bookasessionworkshop).
- "The site is blocked / Norton won't let me on" → **Typeform mirror**, then team books them.
- "Will I get the recording / can I rewatch?" → **replay** (managemoney101.com/replay), then book.
- "When's the next class / can I attend again?" → **next live webinar** (fbmasterclass, with the
  computed date), then still nudge to book the 1:1.

## UTM / tracking (optional)
To track follow-up bookings separately, append a UTM to the primary link, e.g.:
`https://www.managemoney101.com/?utm_source=email&utm_medium=followup&utm_campaign=webinar_reengage`

---

# Part 3 — Open questions for the team (fill these in when you can)

These are the gaps the plugin can't fill on its own — business decisions only LIS knows.
None of them block the core job (finding likely bookers and getting them to book). They only
affect how confidently the follow-up email can answer a few specific questions. Until a gap is
answered, the email follows the safe default (give a short safe line and route to the call).

Answer any of these inline and we'll bake them into the reference content above.

## 1. Replay / recording / slides policy
"Will I get the recording / slides / resources?" is one of the most common chat asks.
- Do attendees actually get a recording or replay? If so, who (everyone, or only people who
  stayed / booked), and how is it delivered?
- Slides / a PDF / notes — do those go out?
- **Answer:** Replay is available to everyone at **https://www.managemoney101.com/replay**.
  Slides/PDF/notes policy still TBD.

## 2. The "freebies / gift for staying to the end"
Several people asked where the promised books / freebies / bonuses are.
- What are these exactly, and how does a lead claim them?
- Are they a booking incentive we can use in the email ("book and you'll also get X")?
- **Answer:** _(open)_

## 3. Next session / "are there other dates?"
People who can't book a time or came in late ask when the next class is.
- Is there a public schedule or a registration link for the next masterclass we can point
  them to?
- **Answer:** Yes. Register link **https://www.managemoney101.com/fbmasterclass**. We run
  it 3x/week, all ET: **Tue 7:00 PM, Thu 7:00 PM, Sun 2:00 PM**. Use
  `scripts/next_webinar.py` to compute the correct next upcoming date per run.

## 4. Reply-to inbox + sender confirmation
- Confirm which inbox replies should hit.
- **Answer:** Send-as and reply-to are both **preston@legacyinvestingshow.com**.
