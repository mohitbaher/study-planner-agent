---
name: replan-missed-days
description: "Re-plans an existing study schedule after missed days. Use when the user reports they skipped days, fell behind, or the exam date or daily hours changed."
license: MIT
allowed-tools: calc-days distribute-topics
metadata:
  author: mohit
  version: "1.0.0"
  category: education
---

# Replan Missed Days

## Instructions
1. Read memory for the saved plan and mark which days were done or missed.
2. Never change completed days. Collect the names of finished topics.
3. Call `calc-days` from today to the exam date.
4. Call `distribute-topics` with the remaining topics and the finished topic names in `completed`.
5. If `fits` is false, say what no longer fits and give the options from the create-plan skill.
6. Update memory and write today's entry in the daily log.

## Output Format
Same table as create-plan, plus a line on what changed: `Moved: N sessions | Dropped: N topics`
