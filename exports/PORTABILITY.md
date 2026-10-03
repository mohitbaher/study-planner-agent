# Portability report: study-planner-agent v0.1.0

Source: `study-planner-agent/` (OpenGAP format). Exported with `opengap export -f <target>` (opengap 0.5.0).
Method: grep each export for a marker from each part of the agent, then load the CrewAI export in CrewAI 1.15.23.

| Part of the agent | claude-code | openai | crewai | lyzr | system-prompt |
|---|---|---|---|---|---|
| Identity (`SOUL.md`) | yes | yes | yes | yes | yes |
| Rules (`RULES.md`) | yes | yes | **no** | yes | yes |
| Skills (names + descriptions) | yes | yes | yes (names/descriptions only) | yes | yes |
| Tools (names + schemas) | yes (listed) | yes (as function stubs) | **no** | yes (listed) | yes (listed) |
| Tool implementations (`*.py`) | no | **no, `# TODO` stubs** | no | no | no |

## Findings

1. **CrewAI export drops `RULES.md` and the tools.** The generated YAML has only `role`, `goal`, `backstory`, `verbose` and `allow_delegation`. The behavior contract is lost on that target.
2. **OpenAI export generates tool signatures but not implementations.** `calc_days` and `distribute_topics` are `pass` stubs marked `# TODO`. The real logic stays in `study-planner-agent/tools/*.py`.
3. **No export carries the tool scripts.** They have to be shipped alongside, or wired by hand on each runtime.
4. **CrewAI export is loadable.** `yaml.safe_load` works, and `crewai.Agent(role=..., goal=..., backstory=...)` builds without error. Not run end to end because no LLM key was available.

## Fix for the CrewAI gap

[`crewai_runner.py`](../crewai_runner.py) loads the exported `crewai.yaml`, appends `RULES.md` and both `SKILL.md` files to the backstory, and wires the real `calc_days.py` / `distribute_topics.py` code in as CrewAI tools (same functions the OpenGAP tool scripts run, no copy).

`python crewai_runner.py --check` asserts: rules present in the backstory, exactly the 2 tools attached, and both tools return correct results when called through CrewAI's tool interface. Passes with CrewAI 1.15.23 + `crewai[anthropic]`.

| Part of the agent | crewai (stock export) | crewai (export + `crewai_runner.py`) |
|---|---|---|
| Rules | no | **yes** |
| Tools | no | **yes, real implementations** |

## What was not tested

- No export was run against a live LLM. Behavior equivalence across runtimes is unverified.
- Only the CrewAI export was loaded into its framework. The others were checked as text.
- The `lyzr` export was not pushed to Lyzr Studio.

## Files

`exports/system-prompt.txt`, `claude-code.txt`, `openai.txt`, `crewai.txt` (and `crewai.yaml`, a copy for loading), `lyzr.txt`.
