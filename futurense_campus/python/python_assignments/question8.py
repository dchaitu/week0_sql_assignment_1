from collections import defaultdict


def get_final_record_per_caller_id(records):
    final_record_per_caller_id= {record["call_id"]: record for record in records}
    return final_record_per_caller_id

def get_call_details_per_tool(final_record_per_caller_id):
    call_details = {}
    for call_id, record in final_record_per_caller_id.items():
        tool = record["tool"]
        if tool not in call_details:
            call_details[tool] = {"calls":0,
                             "successes":0,
                             "failures":0,
                             "total_duration_ms":0
                             }
        stats = call_details[tool]
        if record["status"] == "ok":
            stats["successes"] += 1
        else:
            stats["failures"] += 1
        stats["total_duration_ms"] += record["duration_ms"]
        stats["calls"] += 1

    return call_details




def get_failed_call_ids(final_record_per_caller_id):
    failed_call_ids = []
    for call_id, record in final_record_per_caller_id.items():
        if record["status"] == "error":
            failed_call_ids.append(call_id)
    failed_call_ids =sorted(failed_call_ids)
    return failed_call_ids


# def call_details_by_tool(records):
#     tool_caller_id_wise_status = {}
#     for record in records:
#         tool_caller_id_wise_status[(record['tool'],record['call_id'])] = record['status']
#     return tool_caller_id_wise_status

def get_tool_ranking(by_tool):
    # Rank tools by descending failure count, then descending total calls, then ascending tool name.
    tool_ranking = sorted(by_tool.items(), key=lambda x: (-x[1]["failures"], -x[1]["calls"], x[0]))
    return [tool[0] for tool in tool_ranking]





def summarise_tool_calls(records):
    result = {}
    # tool_caller_id_wise_status = call_details_by_tool(records)
    final_record_per_caller_id = get_final_record_per_caller_id(records)
    # print("final_record_per_caller_id ",final_record_per_caller_id)
    by_tool = get_call_details_per_tool(final_record_per_caller_id)
    # print("\nby_tool ", by_tool,"\n")
    failed_call_ids = get_failed_call_ids(final_record_per_caller_id)
    # print("failed_call_ids ",failed_call_ids)
    tool_ranking = get_tool_ranking(by_tool)
    result["unique_calls"] = len(final_record_per_caller_id)
    result["by_tool"] = by_tool
    result["failed_call_ids"] = failed_call_ids
    result["tool_ranking"] = tool_ranking
    return result







if __name__ == "__main__":
    all_records = [
        {"call_id": "C1", "tool": "search", "status": "error", "duration_ms": 120},
        {"call_id": "C2", "tool": "calculator",  "status": "ok", "duration_ms": 10},
        {"call_id": "C1", "tool": "search", "status": "ok", "duration_ms": 80},
        {"call_id": "C3", "tool": "search",  "status": "error", "duration_ms": 40},
        {"call_id": "C4", "tool": "retriever", "status": "error", "duration_ms": 50},
    ]
    result = summarise_tool_calls(all_records)
    print(result)

# {
#     "unique_calls": 4,
#     "by_tool": {
#         "calculator": {
#             "calls": 1, "successes": 1, "failures": 0,
#             "total_duration_ms": 10,
#         },
#         "search": {
#             "calls": 2, "successes": 1, "failures": 1,
#             "total_duration_ms": 120,
#         },
#         "retriever": {
#             "calls": 1, "successes": 0, "failures": 1,
#             "total_duration_ms": 50,
#         },
#     },
#     "failed_call_ids": ["C3", "C4"],
#     "tool_ranking": ["search", "retriever", "calculator"],
# }