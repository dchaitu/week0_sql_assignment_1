from functools import wraps


def track_calls(history: list):
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            record = {"call_number": len(history) + 1, "function": func.__name__}
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                record["status"] = "error"
                record["error_type"] = type(e).__name__
                history.append(record)
                raise e
            else:
                record["status"] = "success"
                record["error_type"] = None
                history.append(record)
            return result

        return wrapper

    return my_decorator

history = []

@track_calls(history)
def average_score(scores):
    n = len(scores)
    if n:
        return sum(scores)/n
    else:
        raise ValueError("No scores provided")

@track_calls(history)
def format_run_name(prefix, *, number):
    if number < 0:
        raise ValueError("Number must be non-negative")
    return f'{prefix}_{number:02d}'






if __name__ == "__main__":

    # Both utility functions use track_calls(history).
    # Execute in this order:

    print(average_score([60, 80]))
    print(repr(format_run_name("eval", number=3)))
    try:
        average_score([])
    except Exception as e:
        print("Call raises ",type(e).__name__)
    print(history)

    # Catch the last exception to display history.
    # track_calls(history)

    # First call returns:
    # 70.0
    # # Second call returns:
    # "eval_03"
    # # Third call raises ValueError.
    #
    # # History after all three attempted calls:
    # [
    #     {"call_number": 1, "function": "average_score",
    #      "status": "success", "error_type": None},
    #     {"call_number": 2, "function": "format_run_name",
    #      "status": "success", "error_type": None},
    #     {"call_number": 3, "function": "average_score",
    #      "status": "error", "error_type": "ValueError"},
    # ]