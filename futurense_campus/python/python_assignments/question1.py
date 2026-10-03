import json

records = [
    {"learner_id": " L01 ", "score": "82.5"},
    {"learner_id": "L02", "score": 60},
    {"learner_id": "L03", "score": None},
    {"learner_id": "   ", "score": 75},
    {"learner_id": "L04", "score": True},
    {"learner_id": "L05", "score": 48.0},
    {"learner_id": "L06", "score": 105},
]

def is_score_is_valid(score):
    if type(score)== int or type(score)== float:
        if 0<=score<=100:
            return True

    return False
        
def is_eligible(score):
    return True if float(score)>=60 else False


def clean_training_records(records):
    cleaned = []
    rejected_indices = []
    # if 'score' in records and 'learner_id' in records:
    for i, record in enumerate(records):
        if type(record) ==dict and 'score' in record and 'learner_id' in record:
            if type(record["learner_id"]) == str and len(record["learner_id"].strip()):
                stripped_learner_id = record["learner_id"].strip()
                if type(record["score"]) == str:
                    try:
                        value = float(record["score"])
                    except ValueError:
                        rejected_indices.append(i)
                        continue
                elif type(record["score"])== int or type(record["score"])== float:
                    value = float(record["score"])
                else:
                    rejected_indices.append(i)
                    continue
                print("Value",value)
                if is_score_is_valid(value) and value is not None:
                    cleaned.append({"learner_id": stripped_learner_id, "score": value, "eligible": is_eligible(value)})
                else:
                    rejected_indices.append(i)
            else:
                rejected_indices.append(i)
        else:
            rejected_indices.append(i)

    cleaned_records = {"cleaned": cleaned, "rejected_indices":rejected_indices,}
    print("Cleaned records:", cleaned_records)
    # print("Rejected indices:", rejected_indices)

    return cleaned_records


if __name__ == "__main__":

    cleaned_records = clean_training_records(records)
    print(json.dumps(cleaned_records, indent=4))

# {
#     "cleaned": [
#         {"learner_id": "L01", "score": 82.5, "eligible": True},
#         {"learner_id": "L02", "score": 60.0, "eligible": True},
#         {"learner_id": "L05", "score": 48.0, "eligible": False},
#     ],
#     "rejected_indices": [2, 3, 4, 6],
# }