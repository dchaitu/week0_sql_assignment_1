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

def is_learner_id_valid(learner_id):
    if type(learner_id) == str and len(learner_id.strip()) > 0:
        return True
    return False

def validate_score(score):
    if type(score) == bool:
        return None
    if type(score) in (int, float):
        value = float(score)
    elif type(score) == str:
        try:
            value = float(score)
        except ValueError:
            return None
    else:
        return None

    if is_score_is_valid(value):
        return value
    return None

def validate_and_parse_record(record):
    if type(record) != dict:
        return None
    if not ('score' in record and 'learner_id' in record):
        return None

    if not is_learner_id_valid(record["learner_id"]):
        return None
    stripped_learner_id = record["learner_id"].strip()
    if type(stripped_learner_id) != str or len(stripped_learner_id) == 0:
        return None
    curr_score = record['score']
    score = validate_score(curr_score)

    if score is not None:
        return {"learner_id": stripped_learner_id,
            "score": score,
            "eligible": is_eligible(score)
            }



def clean_training_records(records):
    cleaned = []
    rejected_indices = []
    for i, record in enumerate(records):
        cleaned_record = validate_and_parse_record(record)
        if cleaned_record is not None:
            cleaned.append(cleaned_record)
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