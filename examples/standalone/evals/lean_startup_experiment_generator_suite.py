lean_startup_experiment_generator_test_suite = [
    {
        "id": "experiments_are_smart_and_three",
        "prompt": "dinosaur popsicle",
    }
]

lean_startup_experiment_generator_criteria = """
Goal: Validate the subagent outputs exactly three SMART experiments suitable for a 14-day window.

PASS only if ALL conditions are met:

1) Count & Presence
   - Output contains key `experiments` with exactly 3 items.

2) Specific & Hypothesis-linked
   - Each experiment has a clear `objective` stating the learning and implicitly ties to demand/problem validation.

3) Measurable
   - Each experiment includes a `metric` and `success_criteria` with explicit numeric thresholds (counts, percentages, or rates). Qualitative-only criteria are not acceptable.

4) Achievable & Time-bound
   - Each experiment has `timeline_days` between 1 and 14.
   - Scope appears feasible for a solo founder with low cost; presence of `estimated_cost` and minimal `required_assets` supports practicality.

5) Relevant
   - At least one experiment tests demand directly (e.g., smoke test, pre-order), and one probes problem severity (e.g., interviews with a numeric bar for severe pain reports).

Fail if: fewer/greater than 3 experiments; any missing metrics/thresholds; timelines outside 1–14; or all three experiments fail to address demand/problem validation.
"""


