from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek

load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [multiply]

llm_with_tools = model.bind_tools(tools)

query = "What is 2 multiplied by 3?"
messages = [HumanMessage(query)]

ai_msg = llm_with_tools.invoke(messages)
messages.append(ai_msg)

# pass tool outputs to chat models
for tool_call in ai_msg.tool_calls:
    selected_tool = {"multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

ai_msg = model.invoke(messages)
messages.append(ai_msg)

for message in messages:
    print(message)