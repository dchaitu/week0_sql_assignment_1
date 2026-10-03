def remove_spl_chars_from_sides(sentence):
    spl_chars = ['.' ,',', "!" ,"?" ,";", ":"]
    while sentence:
        if sentence[0] in spl_chars:
            sentence = sentence[1:]
        if sentence[-1] in spl_chars:
            sentence = sentence[:-1]
        else:
            break

    return sentence


def tokens_for_payload(payload, min_length):
    new_tokens = []
    if type(payload) == str:
        payload = payload.strip()
        tokens = payload.split()
        for token in tokens:
            token = remove_spl_chars_from_sides(token)
            if len(token) >= min_length:
                 new_tokens.append(token)
        return new_tokens

    elif type(payload) == bytearray or type(payload) == bytes:
        try:
            payload = payload.decode()
            return tokens_for_payload(payload, min_length)
        except UnicodeDecodeError:
            return None


def validate_min_length(min_length):
    if type(min_length)==str:
        raise TypeError("min_length must be an integer")
    elif type(min_length)==bool:
        pass

    if min_length >= 0:
        pass
    else:
        raise ValueError("min_length must be greater than 1")

def prepare_messages(payloads, min_length=3):
    result  = {}
    token_lists = []
    rejected_indices = []
    for i, payload in enumerate(payloads):
        payload_index = i
        tokens = tokens_for_payload(payload,min_length)
        if tokens is None:
            rejected_indices.append(payload_index)
            continue
        tokens = [token.lower() for token in tokens]
        token_lists.append(tokens)

    result["token_lists"] = token_lists
    flat_list = [item for sublist in token_lists for item in sublist]
    result["vocabulary"] = sorted(list(set(flat_list)))
    result["rejected_indices"] = rejected_indices

    return result


if __name__ == "__main__":
    payloads = [
        "  AI, helps TEAMS! ",
        b"Build reliable agents.",
        bytearray(b"AI helps."),
        None,
        b"\xff",
    ]
    result = prepare_messages(payloads, min_length=3)
    print(result)


# {
#     "token_lists": [
#         ["helps", "teams"],
#         ["build", "reliable", "agents"],
#         ["helps"],
#     ],
#     "vocabulary": ["agents", "build", "helps", "reliable", "teams"],
#     "rejected_indices": [3, 4],
# }