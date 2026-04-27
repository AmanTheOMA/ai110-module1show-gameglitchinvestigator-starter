import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from logic_utils import (
    AgentPlan,
    check_guess,
    get_range_for_difficulty,
    guardrail_ai_guess,
    parse_guess,
    plan_ai_guess,
)


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_parse_guess_blank():
    ok, guess, err = parse_guess("   ")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_ai_planner_reduces_search_space():
    history = [(50, "Too Low"), (75, "Too High")]
    plan = plan_ai_guess(1, 100, history)
    assert 51 <= plan.candidate_guess <= 74
    assert plan.confidence > 0


def test_guardrail_repairs_invalid_plan():
    bad_plan = AgentPlan(candidate_guess=999, rationale="bad", confidence=0.2)
    history = [(50, "Too Low"), (75, "Too High")]
    repaired_guess, status = guardrail_ai_guess(bad_plan, 1, 100, history)
    assert status == "repaired_out_of_bounds"
    assert 51 <= repaired_guess <= 74
