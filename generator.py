"""Generate ideal Q/A pairs based off of input corpus"""
import json
import re
from client import client
from loader import load_block

PROMPT_LONG = """

    Consider the following text containing information about the Computer Science program at The University of Windsor:

    %s

    Generate 20 prompts and completions pairs that would teach a GPT-3.5 model the content of this text. Questions should be from a student, answers from a knowledgeable academic advisor.
    Prompts should be complete questions.
    Completions should contain plenty of context so the model can understand the complex and detailed content present.
    Prompts and completions should be long and detailed. 

    Format: <Question goes here>? <newline> <Answer goes here>. <newline> SEPARATE EACH QUESTION AND ANSWER WITH A NEWLINE, DO NOT USE NEWLINES WITHIN A QUESTION OR ANSWER
"""
PROMPT_SHORT = """
    Consider the following text containing information about the Computer Science program at The University of Windsor:

    %s

    Generate 20 prompts and completions pairs that would teach a GPT-3.5 model the content of this text. Questions should be from a student, answers from a knowledgeable academic advisor.

    Format: <Question goes here>? <newline> <Answer goes here>. <newline> SEPARATE EACH QUESTION AND ANSWER WITH A NEWLINE, DO NOT USE NEWLINES WITHIN A QUESTION OR ANSWER
"""

def completion_long(block: str):
    """Generate a set of long completions for a given input block"""
    prompt = PROMPT_LONG % block
    completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content.strip()

def completion_short(block: str):
    """Generate a set of short completions for a given input block"""
    prompt = PROMPT_SHORT % block
    completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-3.5-turbo",
    )
    return completion.choices[0].message.content.strip()

def generate_pairs(block):
    print("Generating pairs for block: ", block)
    long_completion = completion_long(block)
    short_completion = completion_short(block)
    return long_completion, short_completion

def preprocess(qa_list):
    """Preprocess a generated list of Q/A pairs"""
    qa_list = [qa for qa in qa_list if qa != ""] # Remove extra newlines
    qa_list = [qa.replace("Prompt:", "").replace("Completion:", "").replace("Question:", "").replace("Answer:", "").strip() for qa in qa_list] # Remove prompt/completion labels
    qa_list = [re.sub(r'^\d+\.\s*', '', s) for s in qa_list] # Remove question numbers
    return qa_list

def generate_training_data():
    """Generate the total training dataset of Q/A pairs for the model given the input corpus"""

    # Format of each training example for a GPT finetune
    format = {
        "messages": [
            {
                "role": "system",
                "content": "You are an student advisor for the University of Windsor"
            },
            {
                "role": "user",
                "content": ""
            },
            {
                "role": "assistant",
                "content": ""
            }
        ]
    }

    # Write generated Q/A pairs to training.jsonl
    count = 0
    with open("./data/training.jsonl", "a") as f:
        for block in load_block():
            long, short = generate_pairs(block)
            qa_list = long.split("\n") + short.split("\n")
            qa_list = preprocess(qa_list)
            questions, answers = qa_list[::2], qa_list[1::2]
            for question, answer in zip(questions, answers):
                count += 1
                format["messages"][1]["content"] = question
                format["messages"][2]["content"] = answer
                f.write(json.dumps(format) + "\n")

    print("Added", count, "Q/A pairs to training.jsonl")
