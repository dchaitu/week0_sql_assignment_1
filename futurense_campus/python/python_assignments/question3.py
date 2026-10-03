from collections import defaultdict

def is_valid_result(result):
    if type(result) != dict:
        return False
    for key in ("id", "actual", "predicted"):
        val = result.get(key)
        if not type(val)==str or not val.strip():
            return False
    return True

def validate_results(results):
    rejected_indices = []
    valid_count = 0
    for i, result in enumerate(results):
        if not is_valid_result(result):
            rejected_indices.append(i)
        else:
            valid_count += 1
    return valid_count, rejected_indices


def get_correct_count_and_misclassified_ids(results):
    count=0
    misclassified_ids = []
    for result in results:
        if is_valid_result(result):
            res_id = result["id"].strip()
            actual = result["actual"].strip().lower()
            predicted = result["predicted"].strip().lower()
            if actual == predicted:
                count+=1
            else:
                misclassified_ids.append(res_id)

    return count, misclassified_ids



def get_correct_fields(results: list[dict]):
    correct_label = defaultdict(int)
    for result in results:
        if not is_valid_result(result):
            continue

        actual = result["actual"].strip().lower()
        predicted = result["predicted"].strip().lower()

        if actual == predicted:
            correct_label[actual] += 1

    return correct_label

def get_actual_details(labels: list[str],results: list[dict]):
    actual_dict = {}
    correct_label = get_correct_fields(results)
    for label in labels:
        if label not in actual_dict:
            actual_dict[label] = {"total": labels.count(label), "correct": correct_label[label]}
    return actual_dict

def get_misclassified_ids(results: list[dict]):
    misclassified_ids = []
    for result in results:
        if result["predicted"] is not None and result["actual"] is not None:
            if result["actual"].lower().strip() != result["predicted"].lower().strip():
                misclassified_ids.append(result["id"])
    return misclassified_ids


def validate_accuracy(answer):
    try:
        accuracy = round(answer["correct_count"] / answer["valid_count"], 4)
        return accuracy
    except ZeroDivisionError:
        print("Valid count is 0")
        return None


def summarise_predictions(results: list[dict]):
    answer = {}
    valid_count,rejected_indices = validate_results(results)
    labels = [result["actual"].lower().strip() for result in results if result["actual"] is not None]
    correct_count, misclassified_ids= get_correct_count_and_misclassified_ids(results)
    answer["valid_count"] = valid_count
    answer["correct_count"] = correct_count
    validate_accuracy(answer)
    answer["accuracy"] = validate_accuracy(answer)
    answer["by_actual"] = get_actual_details(labels,results)
    answer["misclassified_ids"] = misclassified_ids
    answer["rejected_indices"] = rejected_indices

    return answer





if __name__ == "__main__":
    all_results = [
        {"id": "T1", "actual": "Billing", "predicted": " billing "},
        {"id": "T2", "actual": "Technical", "predicted": "billing"},
        {"id": "T3", "actual": "billing", "predicted": "billing"},
        {"id": "T4", "actual": "Account", "predicted": "ACCOUNT"},
        {"id": "T5", "actual": None, "predicted": "account"},
    ]
    print(summarise_predictions(all_results))



# {
#     "valid_count": 4,
#     "correct_count": 3,
#     "accuracy": 0.75,
#     "by_actual": {
#         "billing": {"total": 2, "correct": 2},
#         "technical": {"total": 1, "correct": 0},
#         "account": {"total": 1, "correct": 1},
#     },
#     "misclassified_ids": ["T2"],
#     "rejected_indices": [4],
# }