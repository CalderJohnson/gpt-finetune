"""Train the model on the training set and evaluate on the validation set."""
import os
from client import client

def finetune(new_upload=False):
    """Submit finetuning job"""
    if new_upload:
        file_response = client.files.create(
            file=open("./data/training.jsonl", "rb"),
            purpose="fine-tune",
        )

        file_id = file_response["id"]
    else:
        file_id="file-7jOlZw27ut1PeZOsQ557IerS"

    finetune_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo",
        suffix="uwindsor_chatbot",
    )


