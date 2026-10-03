# Scenario 3: Impossible schedule

## Input
```json
{
  "today": "2026-10-03",
  "exam": "2026-10-06",
  "hours": 2,
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
| 2026-10-03 | Algebra | 2 | planned |
| 2026-10-04 | Algebra | 2 | planned |
| 2026-10-05 | Revision | 2 | planned |

## Does not fit
- Algebra: 2 h left
- Calculus: 8 h left
- Probability: 5 h left
- Statistics: 4 h left
- Geometry: 5 h left

`Days left: 3 | Topics left: 1 | Hours/day: 2`

## Rule checks (RULES.md)
| Rule | Result |
|------|--------|
| No day exceeds the daily hours | PASS |
| At least 20% of days reserved for revision | PASS |
| Only syllabus topics are scheduled | PASS |
| Dates are YYYY-MM-DD | PASS |
| Overflow is reported (fits = false) | PASS |
