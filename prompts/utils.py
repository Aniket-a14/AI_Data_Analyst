def create_prompt(instruction: str, columns: list) -> str:
    """Creates the prompt with all examples"""
    from . import get_examples
    examples = get_examples()
    
    prompt = f"""SYSTEM: You are a data analyst. You MUST follow these rules:
1. Find the most similar example to the given task
2. Output ONLY the code after "CODE:" with no thinking or explanations
3. Never include any text, markdown, or explanations in your response

The DataFrame is loaded as 'df' with columns: {columns}.

Common patterns:
- Sum of a column: df['column_name'].sum()
- First n rows: df.head(n)
- Last n rows: df.tail(n)
- Filter data: df[df['column'] > value]
"""
    
    for i, example in enumerate(examples, 1):
        prompt += f"""Example {i}:
Task: {example['task']}
CODE: {example['code']}

"""
    
    prompt += f"""IMPORTANT: For the task below, respond ONLY with the code, nothing else.

Task: {instruction}
CODE:"""
    
    return prompt 