# Webinar → Calls

A Claude Code **plugin** that turns one webinar's chat engagement into booked sales
calls. After each webinar it cross-references the exports, finds engaged people who
**didn't book**, prioritizes them by what they asked **and when** they asked it, drafts a
personalized follow-up email per lead **as a Gmail draft for review**, and produces a
manual follow-up list for the team.

## What it does
1. **Parses** the Zoom chat export + Zoom attendee/registrant report(s) + OnceHub booking
   report (a deterministic Python script — `scripts/parse_and_match.py`).
2. **Matches** the email universe → OnceHub (by email) to remove people who already booked,
   and → chat (by name) to attach what each person actually asked.
3. **Prioritizes** the unbooked (High / Medium / Low) from their questions, their intent, and
   **timing** — it auto-detects when the booking link was dropped in chat and ranks people who
   asked a real question *after the pitch* the highest.
4. **Segments** them: booking-friction (tried to book, hit a problem), price, skeptic,
   win-back (booked then canceled), plus review/skip buckets (below-income, claims-booked,
   ambiguous identity, trolls).
5. **Drafts** a short, specific follow-up email per High-priority lead and saves it as a
   **Gmail draft** — using the right booking link for the situation.
6. **Flags** complex / high-intent / booking-problem leads for manual follow-up.

## One-time setup
1. Make sure **Gmail is connected** in Claude Code (the connector that exposes "create
   draft"). Drafts are created there; nothing is auto-sent.
2. The reference files are pre-filled for Legacy Investing Show (links, FAQ, voice). Review
   them and adjust if the offer changes.
3. Install / load the plugin:
   - Dev/test:  `claude --plugin-dir /Users/deveshdhardubey/webinar-to-calls`
   - Or publish via a marketplace and `/plugin install` for the teammate.

## The one job
Find attendees who didn't book but look **likely to book**, reach out, and get them to book.
It's a re-engagement-to-booking play, not a Q&A service. If a lead asked a question, the email
answers it briefly to clear the objection, then drives to the call.

## Reference files (`reference/`)
- **`offer-and-booking.md`** — core offer facts (the $100k qualification floor, pricing rules,
  compliance lines), all booking/replay/register links with rules for which to use, plus the
  team's open questions (replay policy, freebies, next session, etc.).
- **`email-style.md`** — voice, framing, banned phrases, signature (from Preston Seo).
- **`exclude-list.txt`** — team / closer / moderator names to ignore (pre-filled).

## Running it (per webinar)
In Claude Code, with the export files ready:

```
/webinar-to-calls:run <chat.txt> <oncehub.csv> <attendees.csv> <registrants.csv> 2026-06-14
```

Claude runs the parser, drafts the emails into Gmail, and prints the summary + the manual
follow-up list. You review the Gmail drafts and hit send.

### Inputs
| File | Where it comes from | Why it's needed |
|------|--------------------|-----------------|
| Zoom **chat** `.txt` | Zoom → recordings / saved chat | What each person asked + WHEN |
| Zoom **attendee** and/or **registrant** `.csv` | Zoom → Webinar → Attendee/Registration report → Export | **Name + email** (the only email source) |
| **OnceHub** `.csv` | OnceHub → reports → export | Who already booked |

> ⚠️ Without an attendee/registrant report there are **no email addresses** — the chat export
> almost never contains them. In that case the plugin still produces a prioritized manual
> call list, but can't draft emails.

## Notes
- Nothing is ever auto-sent. Gmail **drafts** only, for human review.
- People who typed "I'm booked" in chat but aren't in OnceHub are routed to review, not emailed.
- "Canceled" in OnceHub = booked then canceled → a separate **win-back** segment.
- People who state income under $100k are routed to manual review, not auto-emailed.
- The parser is stdlib-only Python — no installs required.
