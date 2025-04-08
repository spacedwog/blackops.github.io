# blackboard.py
blackboard = {}

def set(user_id, key, value):
    if user_id not in blackboard:
        blackboard[user_id] = {}
    blackboard[user_id][key] = value

def get(user_id, key):
    return blackboard.get(user_id, {}).get(key, None)