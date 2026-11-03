import json
import os


class MemoryManager:

    def __init__(self, file_path="memory/dhmif_memory.json"):
        self.file_path = file_path
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)

        return []

    def save_memory(self):
        with open(self.file_path, "w") as file:
            json.dump(self.memory, file, indent=4)

    def store(self, task, result):
        self.memory.append({
            "task": task,
            "result": result
        })

        self.save_memory()

    def retrieve(self, task):
        matches = []

        for item in self.memory:
            if any(word in item["task"].lower()
                   for word in task.lower().split()):
                matches.append(item)

        return matches[-3:]