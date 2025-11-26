import os
from dotenv import load_dotenv
from todoist_api_python.api import TodoistAPI

# Load environment variables
load_dotenv()

def check_todoist():
    api_key = os.environ.get("TODOIST_API_KEY")
    if not api_key:
        print("Error: TODOIST_API_KEY not found in environment variables.")
        return

    print(f"API Key found: {api_key[:4]}...{api_key[-4:]}")

    try:
        api = TodoistAPI(api_key)
        print("Attempting to fetch tasks...")
        tasks = api.get_tasks()
        print(f"Type of tasks: {type(tasks)}")
        print(f"Dir of tasks: {dir(tasks)}")
        try:
            print(f"Successfully fetched {len(tasks)} tasks.")
        except Exception as e:
            print(f"Could not get len(tasks): {e}")

        print("Applying fix logic (flattening pages)...")
        all_tasks = []
        if hasattr(tasks, '__iter__') and not isinstance(tasks, list):
             for page in tasks:
                 if isinstance(page, list):
                     all_tasks.extend(page)
                 else:
                     # Fallback if it's not a list (e.g. if it was a single task, unlikely)
                     all_tasks.append(page)
        elif isinstance(tasks, list):
            all_tasks = tasks
        
        print(f"Total flattened tasks: {len(all_tasks)}")
        for t in all_tasks[:3]:
            print(f"- {t.content} (Due: {t.due.string if t.due else 'None'})")
    except Exception as e:
        print(f"Error connecting to Todoist: {e}")

if __name__ == "__main__":
    check_todoist()
