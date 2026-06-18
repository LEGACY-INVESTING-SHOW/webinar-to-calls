#!/usr/bin/env python3
"""
parse_and_match.py — Webinar -> Calls lead builder (v2: timing + segments).

Cross-references the webinar inputs and produces ONE prioritized leads table plus
ready-to-use segments for follow-up.

  1. Zoom webinar CHAT export(s)        (.txt)  -> what each person SAID + WHEN they said it
  2. Zoom ATTENDEE and/or REGISTRANT report(s) (.csv) -> name + EMAIL universe (the email source)
  3. OnceHub booking report             (.csv) -> who already BOOKED a call

Output: <out>/leads.csv and <out>/leads.json

WHAT'S NEW IN v2
- TIMING: auto-detects the moment the booking link was first dropped in chat
  (the "managemoney101.com" message). Questions asked AFTER the pitch/link-drop while
  still un-booked are the hottest leads and get a priority boost.
- BOOKING-FRICTION segment: people who tried to book and hit a problem ("how do I book",
  "Norton is blocking the page", "booked the wrong time", "can someone help me book").
  These convert fastest and should get the BACKUP booking link.
- INCOME screen: pulls the dollar figure out of "I only make $60k" style messages and
  compares to the $100k qualification floor; below-floor people are routed to review,
  not auto-emailed.
- NEGATIVITY/SPAM: trolls/insults are routed to a skip list; genuine skeptics
  ("is this legit / too good to be true") are KEPT as a reassurance segment.
- Merges ATTENDEES + REGISTRANTS as the email universe (prefers people who showed up).

Stdlib only. No installs.

Usage:
  python3 parse_and_match.py \
      --chat "chat1.txt" \
      --oncehub OnceHubReport.csv \
      --attendees ZoomAttendees.csv \
      --registrants ZoomRegistrants.csv \
      --webinar-date 2026-06-14 \
      --out ./out
"""
import argparse, csv, json, os, re, sys
from difflib import SequenceMatcher

# ---------------------------------------------------------------- name helpers
_PRONOUN = re.compile(r'\(([^)]*?(she|her|he|him|they|them)[^)]*?)\)', re.I)
_PRONOUN_DASH = re.compile(r'\s*[-–—]\s*(he/him|she/her|they/them|him|her|them)\b', re.I)
_NONNAME = re.compile(r"[^a-z0-9'\- ]")
_LEAD_NUM = re.compile(r'^\s*\d+\s*[-–—]\s*')   # attendee rows like "18 - Ruben Pulido"

def undouble(name: str) -> str:
    """'Rick Rick' -> 'Rick'; 'Arun Dayalu Arun Dayalu' -> 'Arun Dayalu'."""
    toks = name.split()
    n = len(toks)
    if n >= 2 and n % 2 == 0 and toks[:n // 2] == toks[n // 2:]:
        return " ".join(toks[:n // 2])
    return name

def norm_name(s: str) -> str:
    if not s:
        return ""
    s = s.strip()
    s = _LEAD_NUM.sub("", s)
    s = _PRONOUN.sub(" ", s)
    s = _PRONOUN_DASH.sub(" ", s)
    s = s.lower()
    s = _NONNAME.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = undouble(s)
    return s

def norm_email(s: str) -> str:
    return (s or "").strip().lower()

def fuzzy(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# ---------------------------------------------------------------- exclude list
DEFAULT_EXCLUDE = [
    "abby from preston's team", "abby from prestons team", "abby from presont's team",
    "preston", "preston seo", "fireflies.ai notetaker", "fireflies ai notetaker",
    "legacy investing", "host", "panelist", "moderator",
]
def is_excluded(raw: str, extra) -> bool:
    n = norm_name(raw)
    blob = (raw or "").lower()
    for x in DEFAULT_EXCLUDE + extra:
        x = x.strip().lower()
        if not x:
            continue
        if x in n or x in blob:
            return True
    if "fireflies" in blob or "notetaker" in blob:
        return True
    return False

# ---------------------------------------------------------------- chat parsing
HEADER = re.compile(r'^\s*(\d{1,2}):(\d{2}):(\d{2})\s+From\s+(.+?)\s+to\s+(.+?)\s*:\s*$')

# The host message that drops the booking link — used to anchor "after the pitch".
LINKDROP_MARKER = re.compile(r'(managemoney101|apply for a free 1-?on-?1|apply to join)', re.I)

def hms_to_sec(h, m, s):
    return int(h) * 3600 + int(m) * 60 + int(s)

# trivial messages that carry no signal on their own (incl. host call-and-response chants)
TRIVIAL = {
    "1", "2", "3", "0", "yes", "no", "y", "n", "yes!", "yep", "yeah", "yup", "ya",
    "ready", "ready!", "deal", "deal!", "me", "hi", "hello", "hey", "ok", "okay",
    "thanks", "thank you", "ty", "same", "here", "here!", "cool", "kool", "nice",
    "agreed", "agree", "lets go", "let's go", "wow", "true", "done", "present",
    "got it", "good", "great", "yes.", "no.", "1.", "ditto", "same here", "amen",
    "absolutely", "for sure", "lets go!", "roll em", "yes to both", "this is great",
    # poll / call-and-response chants taken straight from the webinar script
    "stuck", "owner", "system", "slash", "slap", "boom", "shield", "fire",
    "i can do this", "i can do it", "i need a system", "owner results",
    "owner-type results", "owner type results",
    # poll answers (income type / status)
    "w2", "w-2", "w 2", "1099", "k1", "k-1", "retired", "business owner", "biz owner",
    "self employed", "self-employed", "homeowner", "renter", "kids", "no kids",
    "let's gooo", "lets gooo", "shake hand", "shake hands", "slap hands",
}
def is_trivial(msg: str) -> bool:
    m = msg.strip().lower()
    if not m:
        return True
    if m in TRIVIAL:
        return True
    if re.fullmatch(r'[\d\s\W_]+', m):   # only digits / punctuation / emoji
        return True
    if len(m) <= 2:
        return True
    return False

def is_rich(msg: str) -> bool:
    """A message worth scanning for topic signals (a real sentence/question,
    not a one-word poll answer or chant)."""
    m = msg.strip()
    return ("?" in m) or (len(m.split()) >= 5) or (len(m) >= 25)

# device / junk display names that are never real, emailable leads
_JUNK_HANDLE = re.compile(r'^(zoom user|iphone|ipad|android|galaxy|user|guest|test|'
                          r'\d+|.*\bnotetaker\b)', re.I)
def is_junk_handle(name: str) -> bool:
    return bool(_JUNK_HANDLE.match((name or "").strip()))

def parse_chat(paths, extra_exclude):
    """Return (people, webinar_start_sec, linkdrop_sec).
    people: norm_name -> {'display':..., 'messages':[(sec, body), ...]}"""
    people = {}
    start_sec = None
    linkdrop_sec = None
    for p in paths:
        try:
            lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as e:
            print(f"  ! could not read {p}: {e}", file=sys.stderr)
            continue
        cur, cur_sec = None, None
        for line in lines:
            h = HEADER.match(line)
            if h:
                cur_sec = hms_to_sec(h.group(1), h.group(2), h.group(3))
                cur = h.group(4).strip()
                if start_sec is None or cur_sec < start_sec:
                    start_sec = cur_sec
                continue
            if cur is None:
                continue
            body = line.strip()
            if not body:
                continue
            # Zoom reaction artifacts ("Reacted to ... with 👍", "Removed a reaction")
            # are not real messages — they echo someone else's text and create false signals.
            if body.startswith("Reacted to ") or body.startswith("Removed a reaction"):
                continue
            # detect the link drop from ANY sender (hosts included) before excluding
            if LINKDROP_MARKER.search(body):
                if linkdrop_sec is None or (cur_sec is not None and cur_sec < linkdrop_sec):
                    linkdrop_sec = cur_sec
            if is_excluded(cur, extra_exclude):
                continue
            key = norm_name(cur)
            if not key:
                continue
            rec = people.setdefault(key, {"display": undouble(cur.strip()), "messages": []})
            rec["messages"].append((cur_sec, body))
    return people, start_sec, linkdrop_sec

# ---------------------------------------------------------------- signal rules
# 'already_booked' is scanned across ALL messages (even short ones) — it is a
# guard, not a topic signal: never email "you didn't book" to someone who said they did.
ALREADY_BOOKED = re.compile(
    r"(i'?m booked|i am booked|i booked|just booked|already booked|booked (a|my) call|"
    r"locked (in|my call)|locked my call in|i scheduled|got my call|signed up( already)?|"
    r"just signed up|i did it|on the calendar)", re.I)

# Booking-friction: tried to book and hit a wall. HIGHEST conversion — send backup link.
BOOKING_HELP = re.compile(
    r"(how (do|to|can|does) (you|i|one)\b.{0,8}book|where.{0,8}(do i book|to book|the link)|"
    r"can'?t book|cannot book|trouble booking|won'?t let me book|unable to book|"
    r"help.{0,15}book|book.{0,12}(help|wrong)|booked.{0,15}wrong|"
    r"wrong.{0,10}(time|slot|appt|appointment|day)|sent.{0,15}(different|wrong).{0,10}(time|appt|appointment)|"
    r"norton|\bblocked\b|blocking|firewall|page (won'?t|wont|not|isn'?t).{0,10}(load|open|work)|"
    r"link.{0,15}(not work|broken|doesn'?t|won'?t|isn'?t)|"
    r"no time.{0,10}(work|avail)|don'?t see a time|no times|jot ?form|applied but|"
    r"filled.{0,15}(out )?(the )?(form|application)|did.{0,8}(my |the )?booking.{0,8}go through|"
    r"tell if.{0,8}(i'?m |im )?booked|confirm.{0,8}book|is my (booking|call|appointment))", re.I)

# Program-price questions (cost of the OFFER, not generic 'I pay too much tax' venting).
PRICE = re.compile(
    r"(how much (is|does|will|do|to|are|for)\b|how much\b.{0,18}(cost|invest|program|join|it|this|you|service)|"
    r"what.{0,15}(the )?(cost|price|investment|range|fee)|what'?s the (cost|price|range|investment|fee)|"
    r"the total cost|total cost|cost (of|to|if|for)\b|price (of|to|for|range)|\bpricing\b|"
    r"\bfees?\b|monthly (cost|payment|fee)|payment plan|financing|how much.{0,12}(over|for) 12 months|"
    r"can i afford|afford (it|this|the)|out of pocket|how much is it)", re.I)

# Topic signals are only scanned over 'rich' messages (real sentences/questions).
SIGNAL_RULES = [
    ("applies_to_me",  r"(only for|is (this|it) (only )?for|do i qualify|qualify for|apply to me|right for me|work for me|benefit me|is it just for|even though i|am i (not )?the (right )?type|for me\?|for someone (like|that)|what about someone|stick around)"),
    ("tax",            r"(\btax|deduction|write.?off|\bstr\b|short.?term rental|cost seg|depreciation|\bllc\b|capital gain|tax bracket|tax strateg|loophole|irs)"),
    ("retirement",     r"(retire|retirement|401k|roth|\bira\b|pension|nest egg|\brmd\b|social security|senior)"),
    ("intent_book",    r"(how do i (book|sign up|get started|start|join|enroll)|where.*(book|the link|sign up)|can i book|want to book|ready to (book|start|sign|join)|book a call|schedule a call|count me in|sign me up|how do i enroll|i'?m in\b|let'?s do (it|this))"),
    ("objection",      r"(\bscam\b|is this (a )?(recording|live|real|legit)|are you (a )?(real|bot)|real person|bots? responding|too good to be true|skeptical|hesitant|high pressure|pyramid|\bmlm\b|catch\b|what'?s the catch|guarantee|no value|waste of time|is this legit)"),
    ("cpa_advisor",    r"(my cpa|have a cpa|already have a cpa|financial advisor|my accountant|already have (an|a) (accountant|advisor)|tax (guy|person|preparer))"),
    ("spouse",         r"(my (spouse|husband|wife|partner)|talk to my (husband|wife|spouse|partner)|we both|joint|household)"),
]
SIGNAL_RES = [(name, re.compile(rx, re.I)) for name, rx in SIGNAL_RULES]

# Hostile / spam: trolls and insults. SKIPPED (not emailed). Skeptics are NOT here —
# 'is this legit / too good to be true' is captured by the 'objection' signal and kept.
HOSTILE = re.compile(
    r"(\bfake news\b|\bf+u+c+k|\bs+h+i+t\b|\bbull ?shit\b|\bshut up\b|\bidiot|\bstupid\b|"
    r"\bliar\b|\blying\b|monitoring bot|\bai bot\b|she'?s (a|the) (ai|bot)|stop spamming|"
    r"this is (a )?spam|piece of (shit|crap)|get lost|nonsense)", re.I)

# Income extraction — only over messages that talk about what the person MAKES.
# Only treat a figure as personal income when it sits in an income context.
# Note: 'no income property' is about real estate, NOT personal income — excluded.
INCOME_CONTEXT = re.compile(r"(i (only )?(make|earn|made|bring)\b|we (make|earn)\b|my (income|salary)|household income|i'?m (making|earning)|i (gross|net))", re.I)
INCOME_NUM = re.compile(r"\$?\s*(\d{2,3})\s*(k\b|,?000\b|\s*thousand)", re.I)
QUAL_FLOOR = 100  # $100k qualification floor stated in the webinar

def extract_income_k(text: str):
    """Return (min_k, max_k) of personal-income figures, else None.
    Requires BOTH an income context AND an actual number — avoids false positives."""
    if not INCOME_CONTEXT.search(text):
        return None
    vals = []
    for m in INCOME_NUM.finditer(text):
        n = int(m.group(1))
        if 10 <= n <= 900:
            vals.append(n)
    if not vals:
        return None
    return (min(vals), max(vals))

def detect_signals(rich_text: str):
    out = [name for name, rx in SIGNAL_RES if rx.search(rich_text)]
    if PRICE.search(rich_text):
        out.append("program_price")
    if BOOKING_HELP.search(rich_text):
        out.append("booking_help")
    return out

# ---- Question topic themes ----------------------------------------------------
# Each lead's chat question is tagged with the topic(s) it matches, so the skill knows
# what they asked and can answer from offer-and-booking.md + general knowledge. Ordered
# most-specific first; the first match becomes the primary `answer_key` (a topic hint).
THEME_RULES = [
    ("booking_scheduling",          BOOKING_HELP),
    ("pricing_cost",                PRICE),
    ("recording_slides_resources",  re.compile(r"(replay|recording|recorded|the slides|copy of (the|this)|the deck|transcript|notes|hand ?out|the video|rewatch|re-?watch|send (me |us )?(the|this)|will (we|i) (get|receive)|where.*(freebie|gift|book that was promised|materials|resources))", re.I)),
    ("llc_entity_augusta",          re.compile(r"(\bllc\b|s-?corp|c-?corp|incorporat|entity|augusta rule|hold ?co|holding company|sole prop)", re.I)),
    ("real_estate_str_depreciation",re.compile(r"(real estate|\bstr\b|short.?term rental|air ?bnb|rental(s| propert)|depreciation|cost seg|recapture|buy (the |a )?propert)", re.I)),
    ("retirement_rmd_ira",          re.compile(r"(retire|retirement|\brmd\b|social security|\bira\b|roth|401k|403b|\btsp\b|pension|annuit|nest egg)", re.I)),
    ("w2_employee_fit",             re.compile(r"(w-?2|employee|remote work|work from home|no business|don'?t have a business|just (a|an) employee)", re.I)),
    ("business_1099_self_employed", re.compile(r"(1099|self-?employed|self employed|side hustle|side business|freelance|business owner|my business)", re.I)),
    ("refund_guarantee_risk",       re.compile(r"(guarantee|refund|money back|what.{0,12}risk|if (it|this) (doesn'?t|does not) work|what if it fails|no risk)", re.I)),
    ("existing_advisor_cpa",        re.compile(r"(my cpa|have a cpa|already have a cpa|financial advisor|my advisor|my accountant|fiduciary|wealth manager|tax (guy|person|preparer))", re.I)),
    ("financing_affordability_income", re.compile(r"(financing|payment plan|pay-?as-?you|\bafford|less than \$?100|under \$?100|make less|lower income|minimum income|can'?t (pay|afford)|too expensive)", re.I)),
    ("legal_tax_compliance",        re.compile(r"(\blegal\b|is this legal|audit|\birs\b|tax law.*(change|new)|loophole.*legal|compliance|get flagged|too good to be true)", re.I)),
    ("results_roi_timeline",        re.compile(r"(\broi\b|return on|how (long|soon).*(result|see)|when.*(see|results)|how fast|timeline|payback|7k.*72k|how does.*become)", re.I)),
    ("diy_youtube_free",            re.compile(r"(youtube|free (tax )?content|learn (this|it) (myself|online)|do it myself|on my own|why pay)", re.I)),
    ("not_real_estate_only_tax",    re.compile(r"(just (want )?(help with )?(my )?tax|not (into|interested in) (investing|real estate)|only.*tax help|don'?t want (real estate|rentals))", re.I)),
    ("tax_prep_filing_advice",      re.compile(r"(file (my|our) (taxes|return)|prepare (my )?tax|tax prep|amend|back taxes|federal and state|do you do taxes)", re.I)),
    ("estate_asset_protection",     re.compile(r"(trust\b|estate|gifting|asset protection|inherit|beneficiar|foundation|irrevocable|revocable)", re.I)),
    ("visa_international",           re.compile(r"(visa|green card|non-?citizen|residency|h1b|immigra|not a citizen)", re.I)),
    ("investment_strategy",         re.compile(r"(invest in|stocks?|crypto|bonds?|portfolio|market|allocation|which fund|where (should i|to) (invest|put))", re.I)),
    ("spouse_partner_family",       re.compile(r"(my (spouse|husband|wife|partner)|talk to my (husband|wife)|bring my|household decision|we both)", re.I)),
    ("credentials_team",            re.compile(r"(credential|who (are you|is the team|will i work)|can i trust|are you certified|your background|vetted)", re.I)),
    ("time_commitment",             re.compile(r"(how much time|too busy|i'?m busy|hours? (a|per) (week|month)|time commitment|don'?t have time)", re.I)),
    ("call_process_prep",           re.compile(r"(what (should i|do i) (expect|bring)|what happens on the call|prepare for the call|what do i need|before the call)", re.I)),
    ("program_structure_support",   re.compile(r"(what (do i get|happens after|support)|after (i )?join|12 months|coaching|community|curriculum|how does the program work)", re.I)),
    ("live_trust_webinar_ops",      re.compile(r"(is this (actually )?live|pre-?recorded|monitoring the chat|anyone (there|monitoring)|skipping (my )?question|how long is (this|the) (webinar|training|presentation))", re.I)),
    ("tech_webinar_access",         re.compile(r"(blurry|can'?t (see|hear)|no (audio|volume|sound)|frozen|screen|fuzzy|cut.?out|can'?t read)", re.I)),
]
THEME_RES = [(k, rx) for k, rx in THEME_RULES]

def detect_themes(rich_text: str, asked_q: bool):
    themes = [k for k, rx in THEME_RES if rx.search(rich_text)]
    if themes:
        return themes, themes[0]
    # asked something we couldn't classify -> generic "had a question" topic hint
    return ([], "specific_advisor_review" if asked_q else "")

# Signals that indicate someone is LIKELY TO BOOK (evaluating/deciding to buy).
HIGH_SIGNALS = {"program_price", "applies_to_me", "intent_book", "objection", "booking_help", "cpa_advisor"}
# Themes that are pure curiosity/logistics — NOT buying intent. Never High on their own.
LOW_INTENT_THEMES = {"recording_slides_resources", "tech_webinar_access", "live_trust_webinar_ops"}

def suggest_priority(signals, asked_q, substantive_count, claims_booked,
                     post_linkdrop, income_status, hostile, has_substance, themes):
    # The goal is to find people LIKELY TO BOOK and get them to book — not to answer chat
    # questions. So buying-intent signals drive priority; pure logistics/curiosity does not.
    if hostile and not has_substance:
        return "Skip-Hostile"
    if claims_booked and not has_substance:
        return "Review-ClaimsBooked"
    if "booking_help" in signals:
        return "High"                       # tried to book = hottest
    if income_status == "below" and "program_price" not in signals and not asked_q:
        return "Review-BelowIncome"

    buying = any(s in HIGH_SIGNALS for s in signals)
    qualified = income_status == "qualified"
    # logistics-only: they asked something, but only curiosity/logistics and no buying signal
    logistics_only = (not buying and not qualified and bool(themes)
                      and all(t in LOW_INTENT_THEMES for t in themes))

    if logistics_only:
        return "Low"                        # recording/replay/tech/"is this live" = not a buyer

    base = "Low"
    if buying:
        base = "High"
    elif qualified and asked_q:
        base = "High"                       # stated $100k+ and engaged with a question
    elif ("tax" in signals or "retirement" in signals or "spouse" in signals) and asked_q:
        base = "High"
    elif asked_q or substantive_count >= 2 or signals:
        base = "Medium"

    # TIMING BOOST: still engaged with a real (non-logistics) question after the pitch/link
    # drop = closer to booking. Bump one level.
    if post_linkdrop and (asked_q or signals) and base in ("Low", "Medium"):
        base = "High" if base == "Medium" else "Medium"
    return base

def pick_segment(signals, oncehub_status, income_status):
    if oncehub_status == "canceled":
        return "winback"
    if "booking_help" in signals:
        return "booking_friction"
    if income_status == "below":
        return "below_threshold"
    if "objection" in signals:
        return "skeptic"
    if "program_price" in signals:
        return "price"
    return "standard"

# ---------------------------------------------------------------- csv loading
def detect_columns(headers):
    lower = {h.lower().strip(): h for h in headers}
    email_col = next((lower[k] for k in lower if "email" in k), None)
    name_col = next((lower[k] for k in lower if k in ("name", "customer name", "full name", "attendee name", "registrant name", "user name (original name)")), None)
    first_col = next((lower[k] for k in lower if "first" in k and "name" in k), None)
    last_col = next((lower[k] for k in lower if "last" in k and "name" in k), None)
    if name_col is None and first_col is None:
        name_col = next((lower[k] for k in lower if "name" in k), None)
    return email_col, name_col, first_col, last_col

def load_people_csv(path):
    """Load a Zoom attendee OR registrant csv -> list of {name, email}."""
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig", errors="replace")))
    if not rows:
        return []
    email_col, name_col, first_col, last_col = detect_columns(rows[0].keys())
    out = []
    for r in rows:
        email = norm_email(r.get(email_col, "")) if email_col else ""
        if name_col:
            name = (r.get(name_col) or "").strip()
        else:
            name = " ".join(x for x in [(r.get(first_col) or "").strip(),
                                        (r.get(last_col) or "").strip()] if x)
        name = _LEAD_NUM.sub("", name)   # strip "18 - " attendee prefixes
        if not email and not name:
            continue
        out.append({"name": name, "email": email})
    return out

def merge_universe(attendee_lists, registrant_lists):
    """Union of attendees + registrants, deduped by email (prefer rows that have email/showed up)."""
    by_email = {}
    no_email = []
    order = []
    def add(rec, showed):
        e = rec["email"]
        if e:
            if e not in by_email:
                by_email[e] = {"name": rec["name"], "email": e, "showed": showed}
                order.append(e)
            else:
                by_email[e]["showed"] = by_email[e]["showed"] or showed
                if not by_email[e]["name"] and rec["name"]:
                    by_email[e]["name"] = rec["name"]
        else:
            no_email.append({"name": rec["name"], "email": "", "showed": showed})
    for lst in attendee_lists:
        for rec in lst:
            add(rec, True)
    for lst in registrant_lists:
        for rec in lst:
            add(rec, False)
    universe = [by_email[e] for e in order] + no_email
    return universe

# ---------------------------------------------------------------- oncehub
MONTHS = {m: i for i, m in enumerate(
    ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"], 1)}
def parse_oh_date(s):
    """'Sun, Jun 14, 2026, 07:43 PM' -> (2026,6,14) or None."""
    m = re.search(r'(\w{3})\s+(\d{1,2}),\s+(\d{4})', s or "")
    if not m:
        return None
    mon = MONTHS.get(m.group(1).lower())
    if not mon:
        return None
    return (int(m.group(3)), mon, int(m.group(2)))

def booking_state(status: str):
    s = (status or "").lower()
    if "trash" in s:
        return None
    if "complete" in s or "schedul" in s or "reschedul" in s:
        return "active"
    if "cancel" in s:
        return "canceled"
    return "active"

def load_oncehub(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig", errors="replace")))
    by_email, by_name = {}, {}
    order = {"active": 2, "canceled": 1}
    def stronger(old, new):
        return new if order.get(new, 0) >= order.get(old, 0) else old
    for r in rows:
        email = norm_email(r.get("Customer email", ""))
        name = (r.get("Customer name") or "").strip()
        state = booking_state(r.get("Status", ""))
        if state is None:
            continue
        created = parse_oh_date(r.get("Creation date and time in UTC", ""))
        info = {"state": state, "created": created}
        if email:
            cur = by_email.get(email)
            if cur is None or order.get(state, 0) >= order.get(cur["state"], 0):
                by_email[email] = info
        if name:
            nk = norm_name(name)
            cur = by_name.get(nk)
            if cur is None or order.get(state, 0) >= order.get(cur["state"], 0):
                by_name[nk] = info
    return by_email, by_name

# ---------------------------------------------------------------- chat matching
def build_chat_index(chat_people):
    full, firstlast, firstname = {}, {}, {}
    for key, rec in chat_people.items():
        full[key] = rec
        toks = key.split()
        if toks:
            firstname.setdefault(toks[0], []).append((key, rec))
        if len(toks) >= 2:
            firstlast[(toks[0], toks[-1])] = (key, rec)
    return full, firstlast, firstname

def match_chat(name, idx):
    full, firstlast, firstname = idx
    key = norm_name(name)
    if not key:
        return None, 0.0, ""
    if key in full:
        return full[key], 1.0, "name-exact"
    toks = key.split()
    if len(toks) >= 2 and (toks[0], toks[-1]) in firstlast:
        k, rec = firstlast[(toks[0], toks[-1])]
        return rec, 0.85, "first+last"
    best, best_score = None, 0.0
    for ckey, rec in full.items():
        sc = fuzzy(key, ckey)
        if sc > best_score:
            best, best_score = rec, sc
    if best_score >= 0.92:
        return best, best_score, "fuzzy"
    if len(toks) == 1 and toks[0] in firstname and len(firstname[toks[0]]) == 1:
        k, rec = firstname[toks[0]][0]
        return rec, 0.5, "first-name-only"
    return None, 0.0, ""

def fmt_offset(sec, start):
    if sec is None or start is None:
        return ""
    d = sec - start
    return f"{d//60}:{d%60:02d}"

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat", nargs="+", required=True)
    ap.add_argument("--oncehub", required=True)
    ap.add_argument("--attendees", nargs="*", default=[])
    ap.add_argument("--registrants", nargs="*", default=[])
    ap.add_argument("--webinar-date", default="")
    ap.add_argument("--pitch-lead-min", type=int, default=10,
                    help="minutes before the link drop that the pitch is assumed to start")
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--exclude-file", default=None)
    ap.add_argument("--out", default="./out")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    extra_exclude = list(args.exclude)
    if args.exclude_file and os.path.exists(args.exclude_file):
        for line in open(args.exclude_file, encoding="utf-8", errors="replace"):
            line = line.split("#", 1)[0].strip()
            if line:
                extra_exclude.append(line)

    chat_people, start_sec, linkdrop_sec = parse_chat(args.chat, extra_exclude)
    idx = build_chat_index(chat_people)
    by_email, by_name = load_oncehub(args.oncehub)

    pitch_sec = (linkdrop_sec - args.pitch_lead_min * 60) if linkdrop_sec is not None else None

    # parse webinar date for "this webinar" booking attribution
    wd = None
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', args.webinar_date or "")
    if m:
        wd = (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # ---- build the email universe ------------------------------------------
    att = [load_people_csv(p) for p in args.attendees if os.path.exists(p)]
    reg = [load_people_csv(p) for p in args.registrants if os.path.exists(p)]
    if att or reg:
        universe = merge_universe(att, reg)
        srcs = []
        if att: srcs.append(f"{sum(len(x) for x in att)} attendees")
        if reg: srcs.append(f"{sum(len(x) for x in reg)} registrants")
        universe_source = " + ".join(srcs) + " (deduped)"
    else:
        universe = [{"name": rec["display"], "email": "", "showed": True}
                    for key, rec in chat_people.items() if not is_junk_handle(rec["display"])]
        universe_source = "chat-only (no attendee/registrant file — emails unavailable)"

    leads = []
    for person in universe:
        name, email = person["name"], person["email"]
        nkey = norm_name(name)

        # booking status (+ was it for THIS webinar?)
        state, match, oh_created = "none", "none", None
        if email and email in by_email:
            state, match, oh_created = by_email[email]["state"], "email-exact", by_email[email]["created"]
        elif nkey and nkey in by_name:
            state, match, oh_created = by_name[nkey]["state"], "name-fuzzy", by_name[nkey]["created"]
        this_webinar_booking = bool(wd and oh_created and oh_created >= wd)

        # chat enrichment
        chat_rec, chat_conf, chat_how = match_chat(name, idx)
        msg_pairs = chat_rec["messages"] if chat_rec else []
        all_bodies = [b for _, b in msg_pairs]
        substantive = [(t, b) for (t, b) in msg_pairs if not is_trivial(b)]
        rich = [(t, b) for (t, b) in substantive if is_rich(b)]
        joined = " | ".join(b for _, b in substantive)
        rich_text = " | ".join(b for _, b in rich)

        claims_booked = bool(ALREADY_BOOKED.search(" | ".join(all_bodies))) if all_bodies else False
        hostile = bool(HOSTILE.search(" | ".join(all_bodies))) if all_bodies else False
        signals = detect_signals(rich_text) if rich_text else []
        asked_q = "?" in joined

        # timing: did they ask something substantive after the pitch / link drop?
        rich_times = [t for t, _ in rich if t is not None]
        first_rich = min(rich_times) if rich_times else None
        last_rich = max(rich_times) if rich_times else None
        post_pitch = bool(pitch_sec is not None and last_rich is not None and last_rich >= pitch_sec)
        post_linkdrop = bool(linkdrop_sec is not None and last_rich is not None and last_rich >= linkdrop_sec)

        # income screen
        inc = extract_income_k(rich_text) if rich_text else None
        if inc is None:
            income_status, income_note = "unknown", ""
        elif inc[1] < QUAL_FLOOR:
            income_status, income_note = "below", f"states ~${inc[0]}k-${inc[1]}k (below ${QUAL_FLOOR}k floor)"
        else:
            income_status, income_note = "qualified", f"states ~${inc[0]}k-${inc[1]}k (meets floor)"

        themes, answer_key = detect_themes(rich_text, asked_q) if rich_text else ([], "")
        has_substance = bool(signals) or asked_q
        priority = suggest_priority(signals, asked_q, len(substantive), claims_booked,
                                    post_linkdrop, income_status, hostile, has_substance, themes)
        segment = pick_segment(signals, state, income_status)

        leads.append({
            "name": name,
            "email": email,
            "showed": person.get("showed", False),
            "webinar_date": args.webinar_date,
            "oncehub_status": state,                 # active / canceled / none
            "oncehub_match": match,
            "this_webinar_booking": this_webinar_booking,
            "chat_match": chat_how,
            "chat_confidence": round(chat_conf, 2),
            "asked_question": asked_q,
            "claims_booked": claims_booked,
            "hostile": hostile,
            "signals": ";".join(signals),
            "themes": ";".join(themes),
            "answer_key": answer_key,
            "income_status": income_status,
            "income_note": income_note,
            "post_pitch": post_pitch,
            "post_linkdrop": post_linkdrop,
            "first_q_at": fmt_offset(first_rich, start_sec),
            "last_q_at": fmt_offset(last_rich, start_sec),
            "priority_suggestion": priority,
            "segment": segment,
            "message_count": len(substantive),
            "messages": joined[:1500],
        })

    # ---- segment for the operator ------------------------------------------
    def has_substance(l):
        return bool(l["signals"]) or l["asked_question"]
    def is_unbooked(l):
        return l["oncehub_status"] != "active"

    unbooked = [l for l in leads if is_unbooked(l)]
    handled = set()

    # win-back FIRST (booked then canceled) — takes precedence over every other bucket
    winback = [l for l in unbooked if l["oncehub_status"] == "canceled" and l["message_count"] > 0]
    for l in winback:
        handled.add(id(l))

    # then trolls, below-income, and unconfirmed claims (from the not-canceled remainder)
    hostile_skip = [l for l in unbooked if id(l) not in handled and l["hostile"] and not has_substance(l)]
    for l in hostile_skip: handled.add(id(l))
    below_income = [l for l in unbooked if id(l) not in handled and l["income_status"] == "below"
                    and l["message_count"] > 0]
    for l in below_income: handled.add(id(l))
    claims_booked = [l for l in unbooked if id(l) not in handled and l["claims_booked"]
                     and not has_substance(l)]
    for l in claims_booked: handled.add(id(l))

    engaged_unbooked = []
    for l in unbooked:
        if id(l) in handled or l["message_count"] == 0:
            continue
        if l["claims_booked"]:
            l["verify_note"] = ("Typed 'booked'/'locked in' in chat — confirm they are NOT "
                                "in OnceHub under another email before sending.")
        engaged_unbooked.append(l)

    # ---- one chat message claimed by multiple distinct emails ----------------------
    # Two outcomes per group (grouped by the exact substantive chat text):
    #   * same full multi-token name  -> same person registered twice -> COLLAPSE (keep one,
    #     record the alternate email).
    #   * single-token name or differing names -> genuinely AMBIGUOUS (e.g. three different
    #     'Kim' registrations matched to one 'Kim' chat line) -> route to manual review,
    #     don't email any of them a question they may not have asked.
    from collections import defaultdict
    by_msg = defaultdict(list)
    singletons = []
    for l in engaged_unbooked:
        if l["messages"]:
            by_msg[l["messages"]].append(l)
        else:
            singletons.append(l)
    ambiguous = []
    keep = []
    for grp in by_msg.values():
        emails = {x["email"] for x in grp if x["email"]}
        if len(grp) == 1 or len(emails) <= 1:
            keep.extend(grp)
            continue
        names = {norm_name(x["name"]) for x in grp}
        if len(names) == 1 and len(next(iter(names)).split()) >= 2:
            # confident same-person duplicate -> collapse
            primary = grp[0]
            primary["alt_emails"] = [x["email"] for x in grp[1:] if x["email"]]
            keep.append(primary)
        else:
            for x in grp:
                x["ambiguity_note"] = (f"{len(emails)} different emails share this name/first-name "
                                       f"and were matched to one chat line — confirm who actually "
                                       f"asked before emailing.")
                ambiguous.append(x)
    engaged_unbooked = keep + singletons

    booked = [l for l in leads if l["oncehub_status"] == "active"]
    canceled_all = [l for l in leads if l["oncehub_status"] == "canceled"]
    booked_this = [l for l in booked if l["this_webinar_booking"]]

    prio_order = {"High": 0, "Medium": 1, "Low": 2}
    def sort_key(l):
        return (prio_order.get(l["priority_suggestion"], 3),
                0 if l["post_linkdrop"] else 1,
                -l["message_count"])
    engaged_unbooked.sort(key=sort_key)
    winback.sort(key=sort_key)

    # ---- write outputs ------------------------------------------------------
    cols = ["priority_suggestion", "segment", "answer_key", "name", "email", "showed",
            "oncehub_status", "this_webinar_booking", "asked_question", "post_pitch",
            "post_linkdrop", "first_q_at", "last_q_at", "income_status", "income_note",
            "signals", "themes", "chat_match", "chat_confidence", "message_count", "messages"]
    with open(os.path.join(args.out, "leads.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for l in engaged_unbooked + winback:
            w.writerow({k: l.get(k, "") for k in cols})

    def counts(rows):
        return {p: sum(r["priority_suggestion"] == p for r in rows) for p in ("High", "Medium", "Low")}

    payload = {
        "summary": {
            "webinar_date": args.webinar_date,
            "universe_source": universe_source,
            "universe_size": len(universe),
            "webinar_start": fmt_offset(start_sec, start_sec) if start_sec else "",
            "link_drop_at": fmt_offset(linkdrop_sec, start_sec),
            "pitch_assumed_at": fmt_offset(pitch_sec, start_sec),
            "booked_active_total": len(booked),
            "booked_this_webinar": len(booked_this),
            "winback_canceled": len(winback),
            "canceled_total": len(canceled_all),
            "unbooked_total": len(unbooked),
            "engaged_unbooked": len(engaged_unbooked),
            "engaged_by_priority": counts(engaged_unbooked),
            "booking_friction": sum(l["segment"] == "booking_friction" for l in engaged_unbooked),
            "skeptics": sum(l["segment"] == "skeptic" for l in engaged_unbooked),
            "below_income_review": len(below_income),
            "claims_booked_review": len(claims_booked),
            "ambiguous_identity_review": len(ambiguous),
            "hostile_skip": len(hostile_skip),
            "chat_distinct_people": len(chat_people),
        },
        "engaged_unbooked": engaged_unbooked,
        "winback_canceled": winback,
        "below_income_review": below_income,
        "claims_booked_review": claims_booked,
        "ambiguous_identity_review": ambiguous,
        "hostile_skip": hostile_skip,
        "all_leads": leads,
    }
    with open(os.path.join(args.out, "leads.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    s = payload["summary"]
    print("=" * 64)
    print("WEBINAR -> CALLS  parse complete (v2: timing + segments)")
    print("=" * 64)
    for k, v in s.items():
        print(f"  {k:26s}: {v}")
    print(f"\n  wrote: {os.path.join(args.out, 'leads.csv')}")
    print(f"  wrote: {os.path.join(args.out, 'leads.json')}")
    if universe_source.startswith("chat-only"):
        print("\n  NOTE: no attendee/registrant file -> emails are blank. Pass --attendees")
        print("        and/or --registrants to enable email drafting.")
    if linkdrop_sec is None:
        print("\n  NOTE: could not auto-detect the link-drop time (no 'managemoney101' line).")
        print("        Timing boost was skipped. Check the chat export or marker.")

if __name__ == "__main__":
    main()
