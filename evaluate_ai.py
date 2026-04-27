"""
Evaluation harness for the AI Guess Strategist.

Runs deterministic games and reports:
- win rate
- average attempts
- guardrail interventions
"""

from logic_utils import check_guess, guardrail_ai_guess, plan_ai_guess


def run_single_game(secret: int, low: int = 1, high: int = 100, max_attempts: int = 8):
    history = []
    guardrail_repairs = 0

    for attempt in range(1, max_attempts + 1):
        planning_history = [(g, o) for g, o in history if o in {"Too Low", "Too High"}]
        plan = plan_ai_guess(low, high, planning_history)
        guess, guardrail_status = guardrail_ai_guess(plan, low, high, planning_history)
        if guardrail_status != "pass":
            guardrail_repairs += 1

        outcome, _ = check_guess(guess, secret)
        history.append((guess, outcome))

        if outcome == "Win":
            return {
                "secret": secret,
                "won": True,
                "attempts": attempt,
                "guardrail_repairs": guardrail_repairs,
                "history": history,
            }

    return {
        "secret": secret,
        "won": False,
        "attempts": max_attempts,
        "guardrail_repairs": guardrail_repairs,
        "history": history,
    }


def run_evaluation():
    secrets = [7, 42, 88]
    results = [run_single_game(secret=s) for s in secrets]

    wins = sum(1 for r in results if r["won"])
    avg_attempts = sum(r["attempts"] for r in results) / len(results)
    repairs = sum(r["guardrail_repairs"] for r in results)

    print("=== AI Strategist Evaluation ===")
    print(f"Scenarios: {len(results)}")
    print(f"Wins: {wins}/{len(results)}")
    print(f"Average attempts: {avg_attempts:.2f}")
    print(f"Guardrail repairs: {repairs}")
    print()
    for result in results:
        print(
            f"secret={result['secret']} won={result['won']} "
            f"attempts={result['attempts']} repairs={result['guardrail_repairs']}"
        )
        print(f"  history={result['history']}")


if __name__ == "__main__":
    run_evaluation()
