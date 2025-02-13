import json
from pathlib import Path

class FeedbackStore:
    def __init__(self, filename='feedback_data.json'):
        self.filename = filename
        self.feedback_data = self._load_feedback()

    def _load_feedback(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"successful_examples": [], "failed_examples": []}

    def save_feedback(self):
        with open(self.filename, 'w') as f:
            json.dump(self.feedback_data, f, indent=2)

    def add_example(self, task, code, is_successful):
        example = {
            "task": task,
            "code": code,
            "think": f"This code {'worked' if is_successful else 'failed'} for the task"
        }
        
        if is_successful:
            self.feedback_data["successful_examples"].append(example)
        else:
            self.feedback_data["failed_examples"].append(example)
        
        self.save_feedback() 
        
        
#this block of code is used to save the feedback to a json file
#the feedback is saved to a json file
#the feedback is used in the agent.py file to train the agent




