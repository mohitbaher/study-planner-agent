"""Fill study days with topic hours in order, skipping completed topics. JSON in/out."""
import json, sys

def distribute(topics, study_dates, hours_per_day, completed=()):
    todo = [[t["name"], float(t["hours"])] for t in topics if t["name"] not in set(completed)]
    rows, i = [], 0
    for day in study_dates:
        free = float(hours_per_day)
        while free > 0 and i < len(todo):
            h = min(free, todo[i][1])
            rows.append({"date": day, "topic": todo[i][0], "hours": h, "status": "planned"})
            free -= h; todo[i][1] -= h
            if todo[i][1] <= 0: i += 1
    left = [{"topic": n, "hours_left": h} for n, h in todo[i:] if h > 0]
    return {"schedule": rows, "unscheduled": left, "fits": not left}

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        ts = [{"name": "A", "hours": 3}, {"name": "B", "hours": 2}]
        r = distribute(ts, ["d1", "d2", "d3"], 2)
        assert r["fits"] and [x["hours"] for x in r["schedule"]] == [2, 1, 1, 1], r
        assert not distribute(ts, ["d1"], 2)["fits"]            # impossible schedule is reported
        assert distribute(ts, ["d1"], 2, ["A"])["schedule"][0]["topic"] == "B"  # replan skips done
        print("distribute_topics ok"); sys.exit()
    print(json.dumps(distribute(**json.load(sys.stdin))))
