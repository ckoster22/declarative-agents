lean_startup_validation_test_suite = [
    {
        "id": "smart_experiments_dinosaur_popsicle",
        "prompt": "dinosaur popsicle",
    }
]

lean_startup_validation_criteria = """
Goal: Verify the agent outputs a Lean Startup validation plan whose experiments include SMART measures (Specific, Measurable, Achievable, Relevant, Time-bound).

PASS only if ALL conditions below are met:

1) Experiments Presence & Count
   - The output contains `validation_plan.experiments` as a non-empty list.
   - There are at least 2 distinct experiments proposed.

2) Specific
   - Each experiment has a clear `objective` that states exactly what learning it targets (e.g., validates a specific customer behavior or value proposition element), not vague wording.
   - The `objective` should be traceable to a particular hypothesis or riskiest assumption (directly referenced or clearly implied).

3) Measurable
   - Each experiment specifies a `metric` and a `success_criteria` with an explicit numeric threshold or unambiguous comparator (e.g., ">= 15 signups", "conversion >= 5%", "at least 8/10 interviewees report X").
   - Thresholds must be concrete (numbers, percentages, counts, or rates). Qualitative-only criteria (e.g., "good feedback") are insufficient.

4) Achievable
   - Each experiment includes a short timeline and cost that make it realistically executable by a solo founder within ~14 days and low budget.
   - Evidence in the plan (e.g., `timeline_days` ≤ 14, minimal `required_assets`, modest `estimated_cost`) supports practicality.

5) Relevant
   - Experiments collectively focus on validating the top 1–2 riskiest assumptions first (e.g., real demand, willingness to pay, problem severity), not low-risk implementation details.
   - At least one experiment directly tests demand (e.g., smoke test, pre-order/payment intent, strong sign-up signal) or strong problem validation (e.g., interviews with clear pain signals).

6) Time-bound
   - Each experiment includes `timeline_days` with a positive integer and a short duration (ideally ≤ 14 days).

7) Internal Consistency
   - `success_criteria` aligns with the specified `metric` and the experiment's `objective`.
   - The plan’s `go_pivot_kill_criteria` are compatible with experiment thresholds (no contradictions).

Failure cases:
   - Fewer than 2 experiments; missing metrics; thresholds not numeric; missing or unrealistic timelines; objectives not tied to hypotheses; experiments unrelated to top risks; or contradictory thresholds.
"""


