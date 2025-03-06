# FILE: cornelius_os/app/modules/knowledge_base.py
import json
import os

class KnowledgeBase:
    """
    A simple knowledge base that stores information in a JSON file.
    """
    def __init__(self, filepath="knowledge_base.json"):
        self.filepath = filepath
        self.data = self.load()

    def load(self):
        """Loads the knowledge base from the JSON file. Creates the file if it doesn't exist."""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r") as f:
                    return json.load(f)
            else:
                # Create an empty knowledge base if the file doesn't exist
                data = {
                    "concepts": [],
                    "relationships": [],
                    "code_snippets": [],
                    "feedback": [],
                    "user_preferences": {},
                    "error_history": [],
                    "interaction_history": [],
                    "tasks": [] #Added
                }
                with open(self.filepath, "w") as f:
                    json.dump(data, f)
                return data
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return {
                "concepts": [],
                "relationships": [],
                "code_snippets": [],
                "feedback": [],
                "user_preferences": {},
                "error_history": [],
                "interaction_history": [],
                "tasks": []
            }

    def save(self):
        """Saves the knowledge base to the JSON file."""
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=4)  # Use indent for readability
        except Exception as e:
            print(f"Error saving knowledge base: {e}")

    def add_information(self, info):
        """Adds new information to the knowledge base."""
        for key, value in info.items():
            if key in self.data:
                if isinstance(value, list):
                    for item in value:
                        if item not in self.data[key]:
                           self.data[key].append(item)
                elif isinstance(value, dict):
                    self.data[key].update(value)
                else:
                    print(f"Warning: Unsupported data type for {key}")
            else:
                print(f"Warning: Unknown knowledge base key: {key}")
        self.save()
    def display(self):
        """Prints the contents of the knowledge base (for debugging)."""
        print("\n--- Knowledge Base ---")
        print(json.dumps(self.data, indent=4))
        print("--- End Knowledge Base ---")

    def summarize(self):
        """Prints a brief summary of the knowledge base."""
        print("\n--- Knowledge Base Summary ---")
        print(f"Number of concepts: {len(self.data['concepts'])}")
        print(f"Number of relationships: {len(self.data['relationships'])}")
        print(f"Number of code snippets: {len(self.data['code_snippets'])}")
        print(f"Number of feedback entries: {len(self.data['feedback'])}")
        print(f"User preferences: {self.data['user_preferences']}")
        print(f"Error history entries: {len(self.data['error_history'])}")
        print(f"Interaction History entries: {len(self.data['interaction_history'])}")
        print(f"Tasks: {', '.join(self.data.get('tasks', []))}")  # Display tasks
        print("--- End Summary ---")
    