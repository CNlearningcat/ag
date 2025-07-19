from typing import List, Dict, Optional
import json

class Conversation:
    """管理对话历史"""
    def __init__(self):
        self.history_messages: List[Dict] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def add_user(self, content: str):
        self.history_messages.append({"role": "user", "content": content})

    def add_assistant(self, answer: str):
        self.history_messages.append({"role": "assistant", "content": answer})

    def get_history(self) -> List[Dict]:
        return self.history_messages

    def save(self, filename="conversation.json"):
        with open(filename, "w") as f:
            json.dump(self.history_messages, f, indent=2)

    def load(self, filename="conversation.json"):
        try:
            with open(filename, "r") as f:
                self.history_messages = json.load(f)
        except FileNotFoundError:
            print("No saved conversation found.")
            pass
    
    def clear_history(self):
        self.history_messages: List[Dict] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]