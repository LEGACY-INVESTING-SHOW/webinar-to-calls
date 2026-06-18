#!/usr/bin/env python3
"""Next upcoming webinar(s) for Legacy Investing Show.

Schedule (America/New_York / Eastern):
  - Tuesday  7:00 PM ET
  - Thursday 7:00 PM ET
  - Sunday   2:00 PM ET

Prints the next upcoming session(s) relative to "now" in Eastern time, plus the
registration link, so the follow-up email always invites people to a real, future
date. The skill calls this each run instead of doing weekday/timezone math by hand.

Usage:
  python3 next_webinar.py                 # next session, ET now
  python3 next_webinar.py --count 3       # next 3 sessions
  python3 next_webinar.py --now 2026-06-18T20:30  # simulate a specific ET wall-clock time
  python3 next_webinar.py --json          # machine-readable

Times are computed in America/New_York, so "7 PM ET" is always 7 PM local New York
wall-clock whether the date falls in EST or EDT. Output labels the live abbreviation
(EST/EDT) for accuracy.
"""
import argparse
import datetime as dt
import json
import sys

try:
    from zoneinfo import ZoneInfo
except ImportError:  # py<3.9 fallback
    ZoneInfo = None

ET = ZoneInfo("America/New_York") if ZoneInfo else None
REGISTER_URL = "https://www.managemoney101.com/fbmasterclass"

# weekday(): Mon=0 .. Sun=6  ->  (hour, minute)
SCHEDULE = {
    1: (19, 0),  # Tuesday  7:00 PM
    3: (19, 0),  # Thursday 7:00 PM
    6: (14, 0),  # Sunday   2:00 PM
}


def _now_et(now_arg):
    if now_arg:
        naive = dt.datetime.fromisoformat(now_arg)
        return naive.replace(tzinfo=ET) if naive.tzinfo is None else naive.astimezone(ET)
    return dt.datetime.now(ET)


def upcoming(now, count=1):
    """Return the next `count` webinar datetimes strictly after `now` (ET-aware)."""
    results = []
    # scan day by day; check today first so a session later today still counts
    for day_offset in range(0, 9 * (count + 1)):
        day = (now + dt.timedelta(days=day_offset)).date()
        wd = day.weekday()
        if wd in SCHEDULE:
            hh, mm = SCHEDULE[wd]
            slot = dt.datetime(day.year, day.month, day.day, hh, mm, tzinfo=ET)
            if slot > now:
                results.append(slot)
                if len(results) >= count:
                    break
    return results


def fmt(slot):
    tzabbr = slot.tzname() or "ET"  # EST or EDT depending on date
    # e.g. "Thursday, June 18 at 7:00 PM EDT"
    return slot.strftime("%A, %B %-d at %-I:%M %p ") + tzabbr


def main(argv=None):
    ap = argparse.ArgumentParser(description="Next Legacy Investing Show webinar(s).")
    ap.add_argument("--count", type=int, default=1, help="how many upcoming sessions to show")
    ap.add_argument("--now", default=None,
                    help="simulate ET wall-clock 'now' as ISO, e.g. 2026-06-18T20:30")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    if ET is None:
        print("ERROR: zoneinfo unavailable; cannot compute Eastern time reliably.",
              file=sys.stderr)
        return 1

    now = _now_et(args.now)
    slots = upcoming(now, max(1, args.count))

    if args.json:
        print(json.dumps({
            "now_et": now.isoformat(),
            "register_url": REGISTER_URL,
            "next": [{"iso": s.isoformat(), "label": fmt(s)} for s in slots],
        }, indent=2))
        return 0

    print(f"As of {fmt(now)} (ET now), the next webinar(s):")
    for s in slots:
        print(f"  - {fmt(s)}")
    print(f"Register: {REGISTER_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
