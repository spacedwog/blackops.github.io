class Blackboard:
    def __init__(self):
        self.memory = {}

    def set(self, user_id, key, value):
        if user_id not in self.memory:
            self.memory[user_id] = {}
        self.memory[user_id][key] = value

    def get(self, user_id, key):
        return self.memory.get(user_id, {}).get(key, None)

blackboard = Blackboard()