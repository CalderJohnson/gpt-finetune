This is a finetune of GPT-3.5 to serve as an information expert for students of computer science at The University of Windsor.

It's been trained on a wide corpus of domain knowledge about the university, and provides immediate articulated responses to students queries, providing convenient access to important information and empowering students to make informed decisions about their academic pathway.

General process:
- Gather many text documents with relevant information.
- Use GPT-3.5 to generate question/answer pairs based off the domain knowledge.
- Finetune GPT-3.5 on the generated examples.

NOTE:

Finetuning is more for learning patterns using knowledge already known to the model, not introducing new knowledge. This makes the finetuning process for GPT not the most suitable for this task :(

Still, I will be saving this code to use it as a scaffold for any generative LLM finetunes I do in the future :)