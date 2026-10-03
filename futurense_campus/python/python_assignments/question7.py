def get_rejected_positions(batch_items):
    rejected_positions = []

    for i,batch in enumerate(batch_items):
        print("batch ",batch)
        for j,num in enumerate(batch):
            if type(num) == int or type(batch) == float and 0 <= batch <= 100:
                pass
            else:
                # raise ValueError("All batches must have the same length")
                rejected_positions.append((i,j))

    return rejected_positions

def get_valid_scores(batch_items, rejected_positions):
    scores = []
    for i,batch in enumerate(batch_items):
        print("batch ",batch)
        for j,num in enumerate(batch):
            if (i,j) not in rejected_positions:
                scores.append((i,j,num))
    return scores


# def get_rejected_positions(*batches):
#     batch_items = batches[0]
#     for batch in batch_items:
#         if type(batch):
#             pass
def validate_top_n(top_n):
    if type(top_n) != int or top_n < 0:
        raise ValueError("top_n must be a non-negative integer")

def validate_batches(batches):
    for batch in batches:
        if type(batch) != list and type(batch) != tuple:
            raise ValueError("All batches must be lists or tuples")

def aggregate_scores(*batches, top_n=3):
    validate_top_n(top_n)
    batch_items = list(batches)
    print("batch_items ",batch_items)
    validate_batches(batch_items)
    rejected_positions = get_rejected_positions(batch_items)
    print("rejected_positions ",rejected_positions)
    scores = get_valid_scores(batch_items,rejected_positions)
    sorted_scores = sorted(scores, key=lambda x:(x[2],-x[0],-x[1]),reverse=True)
    print("sorted_scores ",sorted_scores)
    top_scores = sorted_scores[:top_n]
    print("top_scores ",top_scores)
    valid_count = len(sorted_scores)
    mean = sum(score[2] for score in scores)/valid_count
    result = {
        "valid_count": valid_count,
        "mean": mean,
        "top_scores": top_scores,
        "rejected_positions": rejected_positions,
    }
    return result


if __name__ == "__main__":
    # aggregate_scores(*batches,top_n=3)
    batch_a = [80, 90, None]
    batch_b = (90, 70, True)
    batch_c = []
    result = aggregate_scores(batch_a, batch_b, batch_c, top_n=3)
    print(result)
    # {
    #     "valid_count": 4,
    #     "mean": 82.5,
    #     "top_scores": [
    #         (0, 1, 90.0),
    #         (1, 0, 90.0),
    #         (0, 0, 80.0),
    #     ],
    #     "rejected_positions": [(0, 2), (1, 2)],
    # }