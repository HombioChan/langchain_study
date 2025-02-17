from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

print(prompt_template)

prompt_value = prompt_template.invoke({"topic": "cats"})

print(prompt_value)

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

print(prompt_template.invoke({"topic": "cats"}))

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

print(prompt_template.invoke({"msgs": [HumanMessage(content="hi!"),HumanMessage(content="hii!")]}))