import json
from collections import deque

def creating_queue(curr_queue):
    new_queue= deque()
    set_queue = set()
    for val in curr_queue:
        if val not in set_queue:
            new_queue.append(val)
            set_queue.add(val)
    return new_queue

def add_incoming_to_queue(curr_queue, incoming_tasks,priority):
    for item in incoming_tasks:
        if item not in curr_queue and item != priority:
            curr_queue.append(item)
        elif item == priority:
            curr_queue.appendleft(item)
        elif priority is None:
            pass
    return curr_queue

# def add_priority_to_queue(queue, priority):
#     if priority:
#         queue = queue[::-1]
#         queue.append(priority)
#         queue = queue[::-1]
#
#     return queue

def remove_completed_tasks_from_queue(curr_queue, elements):
    try:
        for item in elements:
            curr_queue.remove(item)

    except ValueError:
        pass
    return curr_queue

def get_next_batch(curr_queue, batch_size):
    next_batch = []
    for i in range(batch_size):
        next_batch.append(curr_queue[i])
    return next_batch

def update_annotation_queue(queue, incoming, completed, priority=None, batch_size=3):
    user_queue = creating_queue(queue)
    print("Queue created as ",user_queue)
    user_queue = add_incoming_to_queue(user_queue,incoming,priority)
    print("After adding incoming",user_queue)


    # queue = add_priority_to_queue(queue, priority)
    user_queue = remove_completed_tasks_from_queue(user_queue, completed)
    print("After removing completion tasks", user_queue)

    next_batch = get_next_batch(user_queue, batch_size)
    print("Last Item",user_queue[-1])
    # last_item = queue

    return user_queue,next_batch



if __name__== "__main__":
    queue = ["D3", "D1", "D3", "D2"]
    incoming = ["D4", "D2", "D5"]
    completed = ["D1", "D9"]


    queue,next_batch= update_annotation_queue(queue, incoming, completed,priority="D5", batch_size=3)
    positions_list = []
    for i,val in enumerate(queue,1):
        positions_list.append((i,val))

    final_dict = {
        "queue": queue,
        "next_batch": next_batch,
        "last_item": queue[-1],
        "positions": positions_list
    }
    print(final_dict)

# {
#     "queue": ["D5", "D3", "D2", "D4"],
#     "next_batch": ["D5", "D3", "D2"],
#     "last_item": "D4",
#     "positions": [
#         (1, "D5"), (2, "D3"), (3, "D2"), (4, "D4"),
#     ],
# }