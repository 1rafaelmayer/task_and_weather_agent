import os
from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage

from app.tools.todoist import get_tasks, add_task
from app.tools.weather import get_current_weather, get_forecast

# Define the tools
tools = [get_tasks, add_task, get_current_weather, get_forecast]

# Define the state
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Initialize the model
def get_model():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

# Define the graph
def create_agent():
    model = get_model()
    model_with_tools = model.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    
    return graph_builder.compile()

agent = create_agent()
