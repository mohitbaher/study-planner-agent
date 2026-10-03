"""Run study-planner-agent on CrewAI with the parts the stock `opengap export -f crewai` drops:
RULES.md (appended to the backstory) and the real tool implementations.

    python crewai_runner.py --check            # build agent + exercise tools, no LLM key needed
    python crewai_runner.py "Plan my study for exam on 2026-10-17, 3h/day: Algebra 6h, Calculus 8h"
Needs ANTHROPIC_API_KEY (or set MODEL for another provider) for the non-check run.
"""
import json, os, sys
from pathlib import Path

import yaml
from crewai import Agent, Crew, Task
from crewai.tools import tool

AGENT = Path(__file__).parent / "study-planner-agent"
sys.path.insert(0, str(AGENT / "tools"))
from calc_days import calc                       # same code the OpenGAP tool scripts run
from distribute_topics import distribute

MODEL = os.environ.get("MODEL", "anthropic/claude-sonnet-4-5-20250929")


@tool("calc-days")
def calc_days_tool(today: str, exam_date: str, revision_pct: int = 20, skip_dates: list = None) -> str:
    """Count days before an exam (YYYY-MM-DD) and split them into study days and revision days."""
    return json.dumps(calc(today, exam_date, revision_pct, skip_dates or []))


@tool("distribute-topics")
def distribute_topics_tool(topics: list, study_dates: list, hours_per_day: float, completed: list = None) -> str:
    """Spread topic hours ({name, hours}) across study dates within the daily limit, skipping completed topics."""
    return json.dumps(distribute(topics, study_dates, hours_per_day, completed or []))


def build_agent():
    exported = yaml.safe_load((Path(__file__).parent / "exports" / "crewai.yaml").read_text("utf-8"))
    a = exported["agents"]["study-planner-agent"]
    rules = (AGENT / "RULES.md").read_text("utf-8")      # export drops this
    skills = "\n\n".join(p.read_text("utf-8") for p in sorted((AGENT / "skills").glob("*/SKILL.md")))
    return Agent(role=a["role"], goal=a["goal"],
                 backstory=f"{a['backstory']}\n\n{rules}\n\n{skills}",
                 tools=[calc_days_tool, distribute_topics_tool], llm=MODEL, allow_delegation=False)


if __name__ == "__main__":
    agent = build_agent()
    if "--check" in sys.argv:
        assert "Must Never" in agent.backstory, "rules missing"
        assert {t.name for t in agent.tools} == {"calc-days", "distribute-topics"}
        days = json.loads(agent.tools[0].run(today="2026-10-03", exam_date="2026-10-13"))
        out = json.loads(agent.tools[1].run(topics=[{"name": "A", "hours": 4}],
                                            study_dates=days["study_dates"], hours_per_day=2))
        assert days["days_left"] == 10 and out["fits"], (days, out)
        print("crewai_runner check ok: rules in backstory, 2 tools wired, tools run")
    else:
        task = Task(description=" ".join(sys.argv[1:]) or "Ask me for what you need to plan my studies.",
                    expected_output="A markdown study plan table and the one-line summary required by the rules.",
                    agent=agent)
        print(Crew(agents=[agent], tasks=[task]).kickoff())
