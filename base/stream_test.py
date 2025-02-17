from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_deepseek import ChatDeepSeek

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

chain = prompt_template | llm | StrOutputParser()

for token in chain.stream({"topic": "bears"}):
    print(token, end="|")
