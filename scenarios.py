"""Stage 3 evidence: run the agent's tools on 3 scenarios via the JSON stdin/stdout protocol,
check the output against RULES.md, and write evidence/*.md. No LLM needed.
Exit code 1 if any rule check fails."""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent
TOOLS = ROOT / "study-planner-agent" / "tools"
OUT = ROOT / "evidence"
SYLLABUS = [{"name": "Algebra", "hours": 6}, {"name": "Calculus", "hours": 8},
            {"name": "Probability", "hours": 5}, {"name": "Statistics", "hours": 4},
            {"name": "Geometry", "hours": 5}]


def tool(script, payload):
    r = subprocess.run([sys.executable, str(TOOLS / script)], input=json.dumps(payload),
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def plan(today, exam, hours, topics, completed=(), skip=()):
    days = tool("calc_days.py", {"today": today, "exam_date": exam, "skip_dates": list(skip)})
    dist = tool("distribute_topics.py", {"topics": topics, "study_dates": days["study_dates"],
                                         "hours_per_day": hours, "completed": list(completed)})
    rows = dist["schedule"] + [{"date": d, "topic": "Revision", "hours": hours, "status": "planned"}
                               for d in days["revision_dates"]]
    return days, dist, rows


def check_common(rows, days, hours, topics):
    names = {t["name"] for t in topics} | {"Revision"}
    per_day = {}
    for r in rows:
        if r["status"] != "missed":
            per_day[r["date"]] = per_day.get(r["date"], 0) + r["hours"]
    return {
        "No day exceeds the daily hours": all(h <= hours for h in per_day.values()),
        "At least 20% of days reserved for revision":
            len(days["revision_dates"]) >= round(days["days_left"] * 0.2),
        "Only syllabus topics are scheduled": all(r["topic"] in names for r in rows),
        "Dates are YYYY-MM-DD": all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]) for r in rows),
    }


def report(name, title, inputs, rows, days, dist, hours, checks):
    lines = [f"# {title}", "", "## Input", "```json", json.dumps(inputs, indent=2), "```", "",
             "## Plan", "| Date | Topic | Hours | Status |", "|------|-------|-------|--------|"]
    lines += [f"| {r['date']} | {r['topic']} | {r['hours']:g} | {r['status']} |"
              for r in sorted(rows, key=lambda r: r["date"])]
    if dist["unscheduled"]:
        lines += ["", "## Does not fit", *[f"- {u['topic']}: {u['hours_left']:g} h left" for u in dist["unscheduled"]]]
    topics_left = len({r["topic"] for r in rows if r["status"] == "planned" and r["topic"] != "Revision"})
    lines += ["", f"`Days left: {days['days_left']} | Topics left: {topics_left} | Hours/day: {hours}`", "",
              "## Rule checks (RULES.md)", "| Rule | Result |", "|------|--------|"]
    lines += [f"| {k} | {'PASS' if v else 'FAIL'} |" for k, v in checks.items()]
    (OUT / f"{name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return all(checks.values())


def main():
    OUT.mkdir(exist_ok=True)
    results = {}

    # 1. Fresh plan
    inp = {"today": "2026-10-03", "exam": "2026-10-17", "hours": 3, "topics": SYLLABUS}
    days, dist, rows = plan(inp["today"], inp["exam"], 3, SYLLABUS)
    checks = check_common(rows, days, 3, SYLLABUS)
    checks["Whole syllabus fits"] = dist["fits"]
    results["1-fresh-plan"] = report("1-fresh-plan", "Scenario 1: Fresh plan", inp, rows, days, dist, 3, checks)
    first_plan = rows

    # 2. Re-plan: studied 10-03..10-05, missed 10-06 and 10-07, today is 10-08
    done_dates, missed_dates, today = {"2026-10-03", "2026-10-04", "2026-10-05"}, {"2026-10-06", "2026-10-07"}, "2026-10-08"
    kept = [dict(r, status="done") for r in first_plan if r["date"] in done_dates]
    kept += [dict(r, status="missed") for r in first_plan if r["date"] in missed_dates]
    done_hours = {}
    for r in kept:
        if r["status"] == "done":
            done_hours[r["topic"]] = done_hours.get(r["topic"], 0) + r["hours"]
    completed = [t["name"] for t in SYLLABUS if done_hours.get(t["name"], 0) >= t["hours"]]
    remaining = [{"name": t["name"], "hours": t["hours"] - done_hours.get(t["name"], 0)} for t in SYLLABUS]
    days, dist, new_rows = plan(today, inp["exam"], 3, remaining, completed)
    rows = kept + new_rows
    checks = check_common(rows, days, 3, SYLLABUS)
    checks["Completed days unchanged"] = [r for r in rows if r["status"] == "done"] == \
        [dict(r, status="done") for r in first_plan if r["date"] in done_dates]
    checks["Completed topics not rescheduled"] = not any(r["topic"] in completed for r in new_rows)
    checks["Nothing scheduled before today"] = all(r["date"] >= today for r in new_rows)
    checks["Remaining syllabus fits"] = dist["fits"]
    results["2-replan-missed-days"] = report(
        "2-replan-missed-days", "Scenario 2: Re-plan after 2 missed days",
        {"today": today, "done": sorted(done_dates), "missed": sorted(missed_dates), "completed_topics": completed},
        rows, days, dist, 3, checks)

    # 3. Impossible schedule: 28 h of syllabus, 3 days, 2 h/day
    inp = {"today": "2026-10-03", "exam": "2026-10-06", "hours": 2, "topics": SYLLABUS}
    days, dist, rows = plan(inp["today"], inp["exam"], 2, SYLLABUS)
    checks = check_common(rows, days, 2, SYLLABUS)
    checks["Overflow is reported (fits = false)"] = not dist["fits"] and bool(dist["unscheduled"])
    results["3-impossible-schedule"] = report("3-impossible-schedule", "Scenario 3: Impossible schedule",
                                              inp, rows, days, dist, 2, checks)

    summary = ["# Verification summary", "", "| Scenario | Result |", "|----------|--------|"]
    summary += [f"| [{k}]({k}.md) | {'PASS' if v else 'FAIL'} |" for k, v in results.items()]
    (OUT / "SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
