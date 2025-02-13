from dotenv import load_dotenv
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

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = model.bind_tools([multiply])
result = llm_with_tools.invoke("Hello world!")
print(result)
result = llm_with_tools.invoke("What is 2 multiplied by 3?")
print(result)
