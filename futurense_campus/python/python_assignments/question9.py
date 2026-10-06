from functools import wraps


def validate_text_batch(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if args:
            texts = args[0]
        elif 'texts' in kwargs:
            texts = kwargs['texts']
        else:
            return func(*args,**kwargs)

        if not type(texts) is list:
            raise TypeError("texts must be a list")

        for text in texts:
            if type(text) != str:
                raise TypeError("All texts must be strings")
            if len(text.strip()) == 0:
                raise ValueError("All texts must be non-empty")

        return func(*args,**kwargs)

    return wrapper

@validate_text_batch
def text_lengths(texts: list[str], *, strip=True):
    if strip:
        texts = [text.strip() for text in texts]
    return [len(text) for text in texts]




if __name__ == "__main__":
    # validate_text_batch_text_lengths(texts, *, strip=True)
    texts = ["  agent ", "ML", "data"]


    print(text_lengths(texts))
    print(text_lengths(texts=texts, strip=False))
    try:
        print(text_lengths(texts=[" "], strip=True))
    except ValueError as e:
        print(f"Caught expected ValueError: {e}")

    # # First call:
    # [5, 2, 4]
    #
    # # Second call:
    # [8, 2, 4]