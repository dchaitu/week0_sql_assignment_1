def build_experiment_config(base, *, run_name,
                        parameter_updates=None, **metadata):
    result = base.copy()
    stripped_run_name = run_name.strip()
    if len(stripped_run_name) == 0:
        raise ValueError("run_name must be non-empty")
    result["run_name"] = stripped_run_name
    result["parameters"] = result["parameters"].copy()
    if parameter_updates and type(parameter_updates)==dict:
        result["parameters"].update(parameter_updates)
    elif parameter_updates is None:
        pass
    else:
        raise TypeError("parameter_updates must be a dictionary")
    result["metadata"] = result["metadata"].copy()
    result["metadata"].update(metadata)
    return result








if __name__ == "__main__":
    base = {
        "model": "ticket_classifier",
        "parameters": {"threshold": 0.5, "max_tokens": 128},
        "metadata": {"owner": "platform", "stage": "baseline"},
    }
    # build_experiment_config(base, *, run_name,
    #                     parameter_updates=None, **metadata)
    result = build_experiment_config(
        base, run_name="trial_02",
        parameter_updates={"threshold": 0.7},
        owner="nlp_team", seed=42,
    )
    another_result = build_experiment_config(
        base, run_name="trial_02",
        parameter_updates={"threshold": 0.7,"max_tokens": 256,"t":123},
        seed=42,
    )

    print(result)
    print(another_result)


# {
#     "model": "ticket_classifier",
#     "parameters": {"threshold": 0.7, "max_tokens": 128},
#     "metadata": {
#         "owner": "nlp_team",
#         "stage": "baseline",
#         "seed": 42,
#     },
#     "run_name": "trial_02",
# }