import copy
from typing import Dict, Any, Optional


def validate_run_name(run_name: str):
    if type(run_name) != str:
        raise ValueError("run_name must be a string")
    stripped_run_name = run_name.strip()
    if stripped_run_name:
        pass
    else:
        raise ValueError("run_name must be non-empty")
    return stripped_run_name

def validate_parameter_updates(result_dict: dict, parameter_updates):
    if parameter_updates is None:
        pass
    elif type(parameter_updates)!=dict :
        # print("parameter_updates ", parameter_updates,type(parameter_updates))
        raise TypeError("parameter_updates must be a dictionary")
    else:
        print("result ",result_dict)
        for key in parameter_updates:
            if key not in result_dict["parameters"]:
                print(key, "not in ",result_dict["parameters"])
                raise KeyError(f"Parameter {key} not present")

        result_dict["parameters"].update(copy.deepcopy(parameter_updates))


def build_experiment_config(base: Dict[str, Any], *, run_name,
                        parameter_updates: Optional[Dict[str, Any]]=None, **metadata: Any)-> Dict[str, Any]:

    stripped_run_name = validate_run_name(run_name)

    result = copy.deepcopy(base)
    result["run_name"] = stripped_run_name
    validate_parameter_updates(result, parameter_updates)
    result["metadata"] = copy.deepcopy(result["metadata"])
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
    print(result)
    # another_result = build_experiment_config(
    #     base, run_name="trial_02",
    #     parameter_updates={"threshold": 0.7,"max_tokens": 256,"t":123},
    #     seed=42,
    # )


    # print(another_result)


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