import json

def UpdateMemory(new_info, category="task"):
    path = r'Data\memory.json'
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        
        if category == "task":
            data["interaction_history"]["last_task"] = new_info
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Memory Update Error: {e}")