lean_startup_validation_test_suite = [
    {
        "id": "smart_experiments_dinosaur_popsicle",
        "prompt": "dinosaur popsicle",
    }
]

lean_startup_validation_criteria = [
    "The output contains 'validation_plan.experiments' as a non-empty list with at least 2 distinct experiments.",
    "Each experiment has a clear 'objective' that states exactly what learning it targets and is traceable to a specific hypothesis or riskiest assumption.",
    "Each experiment specifies a 'metric' and a 'success_criteria' with an explicit numeric threshold or unambiguous comparator (e.g., '>= 15 signups', 'conversion >= 5%', 'at least 8/10 report X').",
    "Each experiment includes a short timeline and cost that make it realistically executable by a solo founder within ~14 days and low budget (evidence: 'timeline_days' ≤ 14, minimal 'required_assets', modest 'estimated_cost').",
    "Experiments collectively focus on validating the top 1–2 riskiest assumptions first, with at least one experiment directly testing demand or strong problem validation.",
    "Each experiment includes 'timeline_days' as a positive integer with a short duration (ideally ≤ 14 days).",
    "Internal consistency: 'success_criteria' aligns with the 'metric' and the experiment's 'objective', and plan-level criteria do not contradict experiment thresholds.",
]


