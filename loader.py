"""Divide input corpus into input chunks that are logically cohesive and fit into the GPT context window"""

def load_block():
    """Generator that yields one chunk of text at a time from the input corpus"""
    with open("./data/corpus.txt", "r") as f:
        block = ""
        for line in f:
            if line.strip() == "":
                if block:
                    yield block
                    block = ""
            else:
                block += line
        if block:
            yield block
