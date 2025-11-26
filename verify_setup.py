import os
import sys
from unittest.mock import MagicMock, patch

# Mock keys
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["TODOIST_API_KEY"] = "dummy"

try:
    with patch("langchain_openai.ChatOpenAI") as mock_openai:
        from app.agent import agent
        print("Agent initialized successfully.")
        
    from app.main import app
    print("FastAPI app initialized successfully.")
    
except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
