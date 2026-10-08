import json
from collections import deque
from typing import Optional


def creating_queue(curr_queue: list):
    new_queue= list()
    set_queue = set()
    for val in curr_queue:
        if val not in set_queue:
            new_queue.append(val)
            set_queue.add(val)
    return new_queue

def add_priority(curr_queue: list,priority: Optional[str] = None):
    if priority is not None and priority in curr_queue:
        curr_queue.remove(priority)
        curr_queue.insert(0, priority)


def add_incoming_to_queue(curr_queue: list, incoming_tasks: list):

    for item in incoming_tasks:
        if item not in curr_queue:
            curr_queue.append(item)
    return curr_queue

def remove_completed_tasks_from_queue(curr_queue: list, elements: list):

    for item in elements:
        try:
            curr_queue.remove(item)

        except ValueError:
            pass
    return curr_queue

def validate_batch_size(batch_size: int):

    if type(batch_size) is not int or batch_size < 0:
        raise ValueError("Batch size must be a non-negative integer")

def get_next_batch(curr_queue: list, batch_size: int):
    next_batch = []
    if len(curr_queue) < batch_size:
        return list(curr_queue)
    for i in range(batch_size):
        next_batch.append(curr_queue[i])
    return next_batch

def update_annotation_queue(queue:list, incoming:list, completed:list, priority=None, batch_size=3):
    validate_batch_size(batch_size)
    user_queue = creating_queue(queue)
    print("Queue created as ",user_queue)
    user_queue = add_incoming_to_queue(user_queue,incoming)
    print("After adding incoming",user_queue)


    # queue = add_priority_to_queue(queue, priority)
    user_queue = remove_completed_tasks_from_queue(user_queue, completed)
    # print("After removing completion tasks", user_queue)
    user_queue = add_priority(user_queue, priority)

    next_batch = get_next_batch(user_queue, batch_size)
    # last_item = queue

    positions_list = []
    for i, val in enumerate(user_queue, 1):
        positions_list.append((i, val))

    final_dict = {
        "queue": user_queue,
        "next_batch": next_batch,
        "last_item": user_queue[-1] if user_queue else None,
        "positions": positions_list
    }

    return final_dict



if __name__== "__main__":
    queue = ["D3", "D1", "D3", "D2"]
    incoming = ["D4", "D2", "D5"]
    completed = ["D1", "D9"]


    final_dict= update_annotation_queue(queue, incoming, completed,priority="D5", batch_size=3)

    print(final_dict)

# {
#     "queue": ["D5", "D3", "D2", "D4"],
#     "next_batch": ["D5", "D3", "D2"],
#     "last_item": "D4",
#     "positions": [
#         (1, "D5"), (2, "D3"), (3, "D2"), (4, "D4"),
#     ],
# }