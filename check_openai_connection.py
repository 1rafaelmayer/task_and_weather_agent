import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

def check_connection():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return

    print(f"Found API Key: {api_key[:5]}...{api_key[-4:]}")

    try:
        model = ChatOpenAI(model="gpt-4o", api_key=api_key)
        print("Attempting to connect to OpenAI...")
        response = model.invoke([HumanMessage(content="Hello")])
        print("\nSuccess! Connected to OpenAI.")
        print(f"Response: {response.content}")
    except Exception as e:
        print(f"\nConnection failed: {e}")

if __name__ == "__main__":
    check_connection()
