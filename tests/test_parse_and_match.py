import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARSER = ROOT / "scripts" / "parse_and_match.py"


class ParseAndMatchSmokeTest(unittest.TestCase):
    def test_engaged_unbooked_post_linkdrop_lead_is_high_priority(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chat = tmp_path / "chat.txt"
            oncehub = tmp_path / "oncehub.csv"
            attendees = tmp_path / "attendees.csv"
            out_dir = tmp_path / "out"

            chat.write_text(
                "\n".join(
                    [
                        "00:01:00 From Preston Seo to Everyone:",
                        "Apply for a free 1-on-1 at https://www.managemoney101.com/",
                        "00:02:00 From Jane Buyer to Everyone:",
                        "How much does the program cost if I already have a CPA?",
                    ]
                ),
                encoding="utf-8",
            )

            with oncehub.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "Customer email",
                        "Customer name",
                        "Status",
                        "Creation date and time in UTC",
                    ],
                )
                writer.writeheader()

            with attendees.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Name", "Email"])
                writer.writeheader()
                writer.writerow({"Name": "Jane Buyer", "Email": "jane@example.com"})

            subprocess.run(
                [
                    sys.executable,
                    str(PARSER),
                    "--chat",
                    str(chat),
                    "--oncehub",
                    str(oncehub),
                    "--attendees",
                    str(attendees),
                    "--webinar-date",
                    "2026-06-14",
                    "--exclude-file",
                    str(ROOT / "reference" / "exclude-list.txt"),
                    "--out",
                    str(out_dir),
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            payload = json.loads((out_dir / "leads.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["engaged_by_priority"]["High"], 1)
            self.assertEqual(payload["summary"]["booked_active_total"], 0)
            self.assertEqual(len(payload["engaged_unbooked"]), 1)

            lead = payload["engaged_unbooked"][0]
            self.assertEqual(lead["email"], "jane@example.com")
            self.assertEqual(lead["priority_suggestion"], "High")
            self.assertEqual(lead["segment"], "price")
            self.assertTrue(lead["post_linkdrop"])


if __name__ == "__main__":
    unittest.main()
