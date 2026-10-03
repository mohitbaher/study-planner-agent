# Scenario 2: Re-plan after 2 missed days

## Input
```json
{
  "today": "2026-10-08",
  "done": [
    "2026-10-03",
    "2026-10-04",
    "2026-10-05"
  ],
  "missed": [
    "2026-10-06",
    "2026-10-07"
  ],
  "completed_topics": [
    "Algebra"
  ]
}
```

## Plan
| Date | Topic | Hours | Status |
|------|-------|-------|--------|
| 2026-10-03 | Algebra | 3 | done |
| 2026-10-04 | Algebra | 3 | done |
| 2026-10-05 | Calculus | 3 | done |
| 2026-10-06 | Calculus | 3 | missed |
| 2026-10-07 | Calculus | 2 | missed |
| 2026-10-07 | Probability | 1 | missed |
| 2026-10-08 | Calculus | 3 | planned |
| 2026-10-09 | Calculus | 2 | planned |
| 2026-10-09 | Probability | 1 | planned |
| 2026-10-10 | Probability | 3 | planned |
| 2026-10-11 | Probability | 1 | planned |
| 2026-10-11 | Statistics | 2 | planned |
| 2026-10-12 | Statistics | 2 | planned |
| 2026-10-12 | Geometry | 1 | planned |
| 2026-10-13 | Geometry | 3 | planned |
| 2026-10-14 | Geometry | 1 | planned |
| 2026-10-15 | Revision | 3 | planned |
| 2026-10-16 | Revision | 3 | planned |

`Days left: 9 | Topics left: 4 | Hours/day: 3`

## Rule checks (RULES.md)
| Rule | Result |
|------|--------|
| No day exceeds the daily hours | PASS |
| At least 20% of days reserved for revision | PASS |
| Only syllabus topics are scheduled | PASS |
| Dates are YYYY-MM-DD | PASS |
| Completed days unchanged | PASS |
| Completed topics not rescheduled | PASS |
| Nothing scheduled before today | PASS |
| Remaining syllabus fits | PASS |
