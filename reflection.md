# Reflection: AI Collaboration and System Design

## Original Bugs and Baseline

When I started, the game had multiple reliability issues: hint direction could be wrong, session state behavior was inconsistent across reruns, and game reset behavior was not always clean after win/loss states. Range handling and validation were also fragile, so out-of-bound guesses could still interfere with game flow. The base project worked as a small Streamlit guessing game, but it was not robust enough to trust repeated use.

## How I Used AI During Development

I used AI in three ways: prompt-based debugging, refactoring guidance, and test generation. First, I asked it to isolate pure game logic from UI code and suggest deterministic functions to test. Next, I used it to design a multi-step AI planner workflow (plan -> validate -> execute) instead of only patching surface bugs. Finally, I used AI-generated test ideas, then adapted them to match actual behavior and edge cases in this project.

## Helpful vs Flawed AI Suggestions

A very helpful suggestion was to introduce a guardrail layer between AI planning and final execution. That changed the design from "AI recommends a guess" to "AI recommends, then self-check verifies," which is much safer. A flawed suggestion was an earlier version of tests that assumed the wrong return type from `check_guess`; that would have caused false failures. I corrected this by rewriting tests to assert tuple outputs (`outcome, message`) and by adding guardrail-focused tests.

## Reliability and Validation Mindset

I now treat AI features as probabilistic components that require validation, not as trusted outputs. In this project, I added input validation, bounded AI behavior, and an evaluation harness script (`evaluate_ai.py`) to verify performance across multiple secrets. This made the app behavior repeatable and inspectable instead of depending on one-off manual trials.

## System Limitations and Future Improvements

The current AI strategist uses a deterministic binary-search style policy, so it is reliable but not very adaptive or language-aware. A next step would be adding model-driven reasoning (for explanations) while keeping the same guardrail contract, plus saving run metrics to a file for trend tracking over time. I would also add UI-level integration tests and a replay mode to compare "manual player vs AI strategist" over many games.
