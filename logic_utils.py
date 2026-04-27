from dataclasses import dataclass
from typing import Iterable, Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    text = raw.strip()
    if text == "":
        return False, None, "Enter a guess."

    try:
        if "." in text:
            value = int(float(text))
        else:
            value = int(text)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        return current_score + max(points, 10)
    if outcome in {"Too High", "Too Low"}:
        return current_score - 5
    return current_score


@dataclass(frozen=True)
class AgentPlan:
    """Structured plan output for the AI strategist."""

    candidate_guess: int
    rationale: str
    confidence: float


def _derive_bounds(low: int, high: int, history: Iterable[tuple[int, str]]) -> tuple[int, int]:
    """Infer current valid bounds from hint history."""
    min_possible = low
    max_possible = high
    for guess, outcome in history:
        if outcome == "Too Low":
            min_possible = max(min_possible, guess + 1)
        elif outcome == "Too High":
            max_possible = min(max_possible, guess - 1)
    return min_possible, max_possible


def plan_ai_guess(low: int, high: int, history: list[tuple[int, str]]) -> AgentPlan:
    """
    Multi-step "AI" planner:
    1) Infer remaining bounds from history.
    2) Propose midpoint candidate.
    3) Emit confidence and explanation.
    """
    min_possible, max_possible = _derive_bounds(low, high, history)
    if min_possible > max_possible:
        # inconsistent history, keep game alive with a safe fallback
        candidate = (low + high) // 2
        return AgentPlan(
            candidate_guess=candidate,
            rationale="History is inconsistent; fallback to global midpoint.",
            confidence=0.1,
        )

    candidate = (min_possible + max_possible) // 2
    width = max_possible - min_possible + 1
    confidence = 1.0 if width == 1 else round(min(0.95, 1.0 / (width / 2)), 2)
    return AgentPlan(
        candidate_guess=candidate,
        rationale=f"Narrowed search space to [{min_possible}, {max_possible}].",
        confidence=confidence,
    )


def guardrail_ai_guess(
    plan: AgentPlan,
    low: int,
    high: int,
    history: list[tuple[int, str]],
) -> tuple[int, str]:
    """
    Reliability harness:
    - validates guessed number is within current inferred bounds.
    - applies deterministic repair when invalid.
    """
    min_possible, max_possible = _derive_bounds(low, high, history)

    if min_possible <= plan.candidate_guess <= max_possible:
        return plan.candidate_guess, "pass"

    repaired_guess = (min_possible + max_possible) // 2 if min_possible <= max_possible else (low + high) // 2
    return repaired_guess, "repaired_out_of_bounds"
