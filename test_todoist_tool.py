import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.tools.todoist import get_tasks

# Load environment variables
load_dotenv()

def test_get_tasks():
    print("Testing get_tasks() function from app/tools/todoist.py...")
    result = get_tasks.invoke({})
    
    if isinstance(result, list) and len(result) > 0:
        if "error" in result[0]:
            print(f"Error: {result[0]['error']}")
        else:
            print(f"Success! Retrieved {len(result)} tasks.")
            for task in result[:5]:
                print(f"- {task['content']} (ID: {task['id']}, Due: {task['due']})")
    else:
        print("No tasks found or empty result.")

if __name__ == "__main__":
    test_get_tasks()
