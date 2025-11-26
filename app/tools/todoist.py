import os
from todoist_api_python.api import TodoistAPI
from typing import List, Dict, Any
from langchain_core.tools import tool

def get_api():
    api_key = os.environ.get("TODOIST_API_KEY")
    if not api_key:
        raise ValueError("TODOIST_API_KEY environment variable not set")
    return TodoistAPI(api_key)

@tool
def get_tasks() -> List[Dict[str, Any]]:
    """Get a list of active tasks from Todoist."""
    try:
        api = get_api()
        tasks_paginator = api.get_tasks()
        
        # Flatten the paginator (which yields pages of tasks)
        all_tasks = []
        for page in tasks_paginator:
            if isinstance(page, list):
                all_tasks.extend(page)
            else:
                all_tasks.append(page)
        
        return [{"id": t.id, "content": t.content, "due": t.due.string if t.due else None} for t in all_tasks]
    except Exception as e:
        return [{"error": str(e)}]

@tool
def add_task(content: str, due_string: str = "today") -> Dict[str, Any]:
    """Add a new task to Todoist.
    
    Args:
        content: The text content of the task (e.g., "Buy milk").
        due_string: Natural language due date (e.g., "today", "tomorrow at 5pm", "next monday").
    """
    try:
        api = get_api()
        task = api.add_task(content=content, due_string=due_string)
        return {"id": task.id, "content": task.content, "due": task.due.string if task.due else None, "status": "created"}
    except Exception as e:
        return {"error": str(e)}
