# Import relevant functionality
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

model = ChatOllama(
    model="llama3.2",
    temperature=0,
    # other params...
)

# Create the agent
memory = MemorySaver()

tools = [multiply]

agent_executor = create_react_agent(model, tools)
# Use the agent
config = {"configurable": {"thread_id": "abc123"}}

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! ")]}, config
):
    print(chunk)
    print("---->")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="What is 2 multiplied by 3?")]}, config
):
    print(chunk)
    print("----")