# Scenario 1: Fresh plan

## Input
```json
{
  "today": "2026-10-03",
  "exam": "2026-10-17",
  "hours": 3,
  "topics": [
    {
      "name": "Algebra",
      "hours": 6
    },
    {
      "name": "Calculus",
      "hours": 8
    },
    {
      "name": "Probability",
      "hours": 5
    },
    {
      "name": "Statistics",
      "hours": 4
    },
    {
      "name": "Geometry",
      "hours": 5
    }
  ]
}
```

## Plan
| Date | Topic | Hours | Status |
|------|-------|-------|--------|
| 2026-10-03 | Algebra | 3 | planned |
| 2026-10-04 | Algebra | 3 | planned |
| 2026-10-05 | Calculus | 3 | planned |
| 2026-10-06 | Calculus | 3 | planned |
| 2026-10-07 | Calculus | 2 | planned |
| 2026-10-07 | Probability | 1 | planned |
| 2026-10-08 | Probability | 3 | planned |
| 2026-10-09 | Probability | 1 | planned |
| 2026-10-09 | Statistics | 2 | planned |
| 2026-10-10 | Statistics | 2 | planned |
| 2026-10-10 | Geometry | 1 | planned |
| 2026-10-11 | Geometry | 3 | planned |
| 2026-10-12 | Geometry | 1 | planned |
| 2026-10-14 | Revision | 3 | planned |
| 2026-10-15 | Revision | 3 | planned |
| 2026-10-16 | Revision | 3 | planned |

`Days left: 14 | Topics left: 5 | Hours/day: 3`

## Rule checks (RULES.md)
| Rule | Result |
|------|--------|
| No day exceeds the daily hours | PASS |
| At least 20% of days reserved for revision | PASS |
| Only syllabus topics are scheduled | PASS |
| Dates are YYYY-MM-DD | PASS |
| Whole syllabus fits | PASS |
