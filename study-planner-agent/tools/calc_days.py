"""Split the days from `today` to `exam_date` into study days and revision days. JSON in/out."""
import json, sys
from datetime import date, timedelta

def calc(today, exam_date, revision_pct=20, skip_dates=()):
    d0, d1 = date.fromisoformat(today), date.fromisoformat(exam_date)
    skip = set(skip_dates)
    days = [(d0 + timedelta(n)).isoformat() for n in range((d1 - d0).days)]  # exam day itself excluded
    days = [d for d in days if d not in skip]
    n_rev = round(len(days) * revision_pct / 100) if days else 0
    split = len(days) - n_rev
    return {"days_left": len(days), "study_dates": days[:split], "revision_dates": days[split:]}

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        r = calc("2026-10-01", "2026-10-11", 20, ["2026-10-03"])
        assert r["days_left"] == 9 and len(r["revision_dates"]) == 2 and "2026-10-03" not in r["study_dates"], r
        assert calc("2026-10-11", "2026-10-11")["days_left"] == 0
        print("calc_days ok"); sys.exit()
    print(json.dumps(calc(**json.load(sys.stdin))))
