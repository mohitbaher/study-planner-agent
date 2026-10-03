---
name: create-plan
description: "Builds a day-by-day study plan from a syllabus, exam date and daily hours. Use when the user asks for a new study plan, timetable or schedule."
license: MIT
allowed-tools: calc-days distribute-topics
metadata:
  author: mohit
  version: "1.0.0"
  category: education
---

# Create Plan

## Instructions
1. Confirm exam date, daily hours and topic list. Ask for anything missing. Estimate hours per topic only if the user gives none, and say so.
2. Call `calc-days` with today's date, the exam date and any days off.
3. Call `distribute-topics` with the topics, `study_dates` and the daily hours.
4. If `fits` is false, show the `unscheduled` topics and offer options: more hours per day, fewer topics, or a later exam date.
5. Add the `revision_dates` to the plan as revision days.
6. Save the plan and the profile to memory.

## Output Format
| Date | Topic | Hours | Status |
|------|-------|-------|--------|

Finish with: `Days left: N | Topics left: N | Hours/day: N`
