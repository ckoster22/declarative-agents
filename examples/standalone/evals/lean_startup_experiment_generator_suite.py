lean_startup_experiment_generator_test_suite = [
    {
        "id": "experiments_are_smart_and_three",
        "prompt": "dinosaur popsicle",
    }
]

lean_startup_experiment_generator_criteria = [
    "Output contains key 'experiments' with exactly 3 items.",
    "Each experiment includes a clear 'objective' stating the learning and implicitly ties to demand/problem validation.",
    "Each experiment specifies a 'metric' and 'success_criteria' with explicit numeric thresholds (counts, percentages, or rates); qualitative-only criteria are unacceptable.",
    "Each experiment includes 'timeline_days' between 1 and 14 and is feasible for a solo founder with low cost; presence of 'estimated_cost' and minimal 'required_assets' supports practicality.",
    "Collectively, at least one experiment tests demand directly (e.g., smoke test, pre-order) and at least one probes problem severity (e.g., interviews with a numeric bar for severe pain reports).",
]


