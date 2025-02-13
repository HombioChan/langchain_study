from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field

load_dotenv()

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# Bind response formatter schema as a tool to the model
model_with_tools = model.bind_tools([ResponseFormatter])
# Invoke the model
ai_msg = model_with_tools.invoke("What is the powerhouse of the cell?")

# Get the tool call arguments
print(ai_msg.tool_calls[0]["args"])
# Parse the dictionary into a pydantic object
pydantic_object = ResponseFormatter.model_validate(ai_msg.tool_calls[0]["args"])
print(pydantic_object)