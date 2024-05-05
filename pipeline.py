"""GPT finetune pipeline"""
import re
import json
from client import client
from generator import generate_training_data
from finetune import finetune

# Generate training dataset with Q/A pairs
#generate_training_data()

# Finetune GPT-3.5 turbo using generated dataset
finetune()
