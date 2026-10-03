def validate_text_batch(func):
    def wrapper(*args,**kwargs):
        if args:
            for text in args[0]:
                print("Args ",args)
                print("Text",text)
                if type(text) != str:
                    raise TypeError("All texts must be strings")
                elif len(text.strip()) == 0:
                    raise ValueError("All texts must be non-empty")


        kwargs.setdefault('strip',True)

        return func(*args,**kwargs)

    return wrapper

@validate_text_batch
def text_lengths(texts, *, strip=True):
    if strip:
        texts = [text.strip() for text in texts]
    return [len(text) for text in texts]




if __name__ == "__main__":
    # validate_text_batch_text_lengths(texts, *, strip=True)
    texts = ["  agent ", "ML", "data"]


    print(text_lengths(texts))
    print(text_lengths(texts=texts, strip=False))
    print(text_lengths(texts=[" "], strip=True))

    # # First call:
    # [5, 2, 4]
    #
    # # Second call:
    # [8, 2, 4]