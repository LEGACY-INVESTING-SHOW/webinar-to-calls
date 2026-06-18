---
name: run
description: Turn one webinar's chat into booked-call follow-ups. Parses the Zoom chat export, the Zoom attendee/registrant report(s), and the OnceHub booking report; finds engaged leads who did not book; prioritizes them by question type AND when they asked (questions after the pitch/link-drop rank highest); drafts a personalized follow-up email per lead as a Gmail DRAFT for review; and produces a manual follow-up list. Trigger manually after each webinar.
argument-hint: [chat.txt] [oncehub.csv] [attendees.csv] [registrants.csv] [webinar-date]
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Webinar → Calls: follow-up run

You are running the post-webinar follow-up for **Legacy Investing Show**.

**The one job:** find the attendees who did **not** book a call but look **likely to book**,
reach out, and get them to book. That is the goal. This is a re-engagement-to-booking play,
**not** a Q&A service. If a lead asked a question, answer it briefly to remove the friction in
their way, then drive them to the call — but the email's purpose is the booking, not the
answer. Don't turn a follow-up into a long explainer. When in doubt, shorter and more
booking-focused wins.

Output is **Gmail drafts a human reviews before sending** — never auto-send.

## Inputs (ask the operator for any that are missing)
1. **Zoom chat export** (`.txt`) for the webinar.
2. **OnceHub booking report** (`.csv`) covering this webinar's window.
3. **Zoom attendee and/or registrant report(s)** (`.csv`) — the source of names + **emails**.
   Pass both if you have them (the parser merges and dedupes; it prefers people who actually
   attended). If you have NEITHER, STOP and tell the operator: without an email source we can
   only produce a manual call list. (Zoom → Webinars → the session → Attendee/Registration
   report → Export.)
4. **Webinar date** (e.g. 2026-06-14).

Arguments, if passed: `$0`=chat, `$1`=oncehub, `$2`=attendees, `$3`=registrants, `$4`=date.

## Step 1 — Parse, match & prioritize (deterministic; do not eyeball the files)
Run the parser. Use the plugin's own path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/parse_and_match.py" \
  --chat "<chat.txt>" \
  --oncehub "<oncehub.csv>" \
  --attendees "<attendees.csv>" \
  --registrants "<registrants.csv>" \
  --webinar-date "<YYYY-MM-DD>" \
  --exclude-file "${CLAUDE_PLUGIN_ROOT}/reference/exclude-list.txt" \
  --out "./webinar-out-<YYYY-MM-DD>"
```

Then `Read` `./webinar-out-<date>/leads.json`. Key fields:
- `summary` — counts, plus `link_drop_at` / `pitch_assumed_at` (the timing anchors the parser
  auto-detected from the chat) and `booked_this_webinar`.
- `engaged_unbooked` — your email list, pre-sorted High → Medium → Low, post-pitch askers first.
  Each lead has `name, email, signals, segment, asked_question, post_pitch, post_linkdrop,
  first_q_at, last_q_at, income_status, messages, priority_suggestion`, and maybe `verify_note`,
  `alt_emails`.
- `winback_canceled` — booked then canceled = separate win-back segment.
- `below_income_review` — stated income under the $100k floor → manual review, do NOT auto-email.
- `claims_booked_review` — typed "I'm booked" but unconfirmed → manual review, do NOT email.
- `ambiguous_identity_review` — one chat line matched to several same-name registrations →
  manual review, do NOT email (we can't tell who actually asked).
- `hostile_skip` — trolls/insults → skip entirely.

### How priority works (so you can trust the sort)
- **Timing matters.** The parser finds the moment the booking link was first dropped in chat
  and flags anyone who asked a substantive question *after* it (`post_linkdrop`) — these are
  the hottest leads and are boosted up.
- **Segment matters.** `booking_friction` (tried to book, hit a problem) is always top
  priority. `price`, `applies_to_me`, `objection/skeptic`, `intent_book` are High.

## Step 2 — Load the approved content
`Read` these before drafting:
- `${CLAUDE_PLUGIN_ROOT}/reference/offer-and-booking.md` — core offer facts, qualification
  ($100k), pricing/discount rules, compliance lines, the **Restricted information / do-not-say**
  list, the booking/replay/register links per situation, and the team's open questions. This is
  your source of truth for what may and may not be said.
- `${CLAUDE_PLUGIN_ROOT}/reference/email-style.md` — voice, framing, banned phrases, signature.

## Step 3 — Draft one email per High-priority engaged lead (with an email address)
Default scope is **High only** (the operator can ask you to extend to Medium). Skip any lead
with no email, and skip everyone in the review/skip buckets above. Follow `email-style.md`
exactly — it is the source of truth for voice, framing, banned phrases, and the signature.
Key points:
- Open with the approved framing: thank them for joining the **personal finance masterclass**
  on Zoom, and say you were going back through the chat and saw the question you didn't get to
  answer live. NEVER call it the "Legacy Wealth Blueprint webinar" (too salesy).
- Then quote their actual question and answer it plainly.
- **Answering questions:** each lead has a `themes`/`answer_key` topic tag from the parser —
  treat it as a hint for what they asked, but trust the actual question text over the tag. Build
  a short, plain answer from the facts in `offer-and-booking.md` plus correct, non-personalized
  general finance/tax knowledge, then route to the call. Obey the **Restricted information /
  do-not-say** list in `offer-and-booking.md`: NEVER state or invent prices, dollar/ROI
  guarantees, refund/cancellation terms, individualized tax/legal/financial advice, or offer
  facts not in the reference files. If the lead didn't ask a clear question (`answer_key` empty),
  send the shorter general version (masterclass thank-you + free call + link).
- Bridge to the free call as the next step; include the **primary** booking link
  (managemoney101.com). UNLESS the lead is `segment: booking_friction`, in which case use the
  **backup** link (bookasessionworkshop), or the Typeform mirror if they reported a site block.
- **Next live webinar (secondary CTA):** for win-back, "I missed it / came in late," or "is
  there another date?" leads, you can also invite them to the next live masterclass. Don't guess
  the date — run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/next_webinar.py"` and use the exact next
  session it returns (Eastern time) with the register link (managemoney101.com/fbmasterclass).
  Keep the 1:1 booking as the primary ask; the live session is the softer option for people not
  ready to book yet. See `offer-and-booking.md` for the schedule.
- 100–160 words. Subject specific to their question. **No em-dashes or en-dashes.** Avoid the
  banned phrases in `email-style.md` ("honest best next step," "no pressure," "clearer
  picture," "grab a time," etc.). From **Preston Seo**, reply-to preston@legacyinvestingshow.com.
- Match the email to the lead's `segment` (booking_friction / skeptic / price / winback /
  standard) per the segment notes in `email-style.md`.
- If the lead has a `verify_note`, prepend `[VERIFY BOOKING]` to the draft subject so the
  reviewer double-checks OnceHub before sending.

## Step 4 — Draft the extra segments
- **Win-back** (`winback_canceled`, High first): a softer "noticed your call didn't end up
  happening" re-book email — no guilt — using the primary link.
- **Booking-friction**: covered in Step 3 but always include; these convert fastest.
- **Skeptics**: a brief reassurance email (skepticism is reasonable, free no-pressure call).

## Step 5 — Create Gmail drafts (review mode)
For each drafted email, create a **Gmail draft** (do not send) to the lead's email. If the
Gmail connector is not authenticated, ask the operator to connect Gmail, or fall back to
writing the drafts to files for review. Confirm the count created. NEVER auto-send.

## Step 6 — Manual follow-up list for Ronaldo
Output a table of people Ronaldo should personally handle (not the automated drafts):
`below_income_review`, `claims_booked_review`, `ambiguous_identity_review`, anyone with a
complex/nuanced situation, strong objections worth a call, and booking/tech problems that
need a human. For each: why flagged, what to say/do, and channel (email / SMS / IG DM) if known.

## Step 7 — Report
Print, in this order:
1. **Summary** (from `summary`, including the timing anchors and `booked_this_webinar`).
2. **High-priority unbooked** table: Priority | Segment | Name | Email | Question/Context |
   When asked (`last_q_at`, post-pitch?) | Notes.
3. **Gmail drafts created** (count + who).
4. **Win-back (canceled)** shortlist.
5. **Manual follow-up list for Ronaldo** (the review/skip buckets).
6. **Data issues**: missing emails, ambiguous identities, possible OnceHub duplicates,
   claims-booked-unconfirmed, anyone needing SMS/IG instead of email.

## Hard rules
- Never auto-send. Drafts only.
- Never email anyone whose `oncehub_status` is `active` (already booked).
- Never email the review/skip buckets (below-income, claims-booked, ambiguous, hostile).
- Never state a program price or a specific dollar/ROI guarantee in writing.
- Never give tax/legal/financial advice as a recommendation — the call is where their
  situation gets reviewed.
- Don't invent personal details, offer facts, prices, or answers not in the reference files
  (general finance-concept knowledge is OK for a brief answer, then route to the call).
- Keep every email short, specific, helpful, not hypey, not pushy.
