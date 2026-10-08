import json
from collections import defaultdict, Counter


def audit_dataset_ids(train_ids, validation_ids):
    filtered_train_ids,invalid_train_indices = get_filtered_ids_and_invalid_indices(train_ids)
    filtered_validation_ids,invalid_indices = get_filtered_ids_and_invalid_indices(validation_ids)
    result = defaultdict(list)
    result["train_duplicates"] = get_duplicates(filtered_train_ids)
    result["validation_duplicates"] = get_duplicates(filtered_validation_ids)
    result["overlap"] = sorted(set(filtered_train_ids) & set(filtered_validation_ids))
    result["train_only"] = sorted(get_unique_ids(filtered_train_ids, filtered_validation_ids))
    result["validation_only"] = sorted(get_unique_ids(filtered_validation_ids, filtered_train_ids))
    result["invalid_train_indices"] = invalid_train_indices
    result["invalid_validation_indices"] = invalid_indices
    result["snapshots"] = {"train": frozenset(filtered_train_ids), "validation": frozenset(filtered_validation_ids)}
    return result

def get_filtered_ids_and_invalid_indices(ids):
    filtered_ids = []
    invalid_indices = []
    for i,id in enumerate(ids):
        # if id is None:
        #     invalid_indices.append(i)
        if type(id)==str:
            if len(id.strip())>0:
                filtered_ids.append(id.strip())
            else:
                invalid_indices.append(i)
        else:
            invalid_indices.append(str(id))

    return filtered_ids,invalid_indices

def get_duplicates(ids):
    id_dict= Counter(ids)
    print("id_dict ",id_dict)
    return sorted([id for id, count in id_dict.items() if count > 1])

def get_common_ids(ids1, ids2):
    unique_ids1 = list(Counter(ids1).keys())
    unique_ids2 = list(Counter(ids2).keys())
    print("Unique ids ",unique_ids1,unique_ids2)
    return list(set(unique_ids1) & set(unique_ids2))

def get_unique_ids(ids1, ids2):
    return list(set(ids1) - set(ids2))

# def get_info_in_json_format(result):
#     return json.dumps(result, indent=4)

if __name__ == "__main__":
    train_ids = ["R3", "R1", " R2 ", "R1", None]
    validation_ids = ["R2", "R4", "R4", " "]
    answer = audit_dataset_ids(train_ids, validation_ids)
    print(answer)
# {
#     "train_duplicates": ["R1"],
#     "validation_duplicates": ["R4"],
#     "overlap": ["R2"],
#     "train_only": ["R1", "R3"],
#     "validation_only": ["R4"],
#     "invalid_train_indices": [4],
#     "invalid_validation_indices": [3],
#     "snapshots": {
#         "train": frozenset({"R1", "R2", "R3"}),
#         "validation": frozenset({"R2", "R4"}),
#     },
# }