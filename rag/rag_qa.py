from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="../db/chroma_langchain_db",  # Where to save data locally, remove if not necessary
)


retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 1, 'lambda_mult': 0.25}
)

query = "Where is Joshua?"

docs = retriever.invoke(query)
for doc in docs:
    print(f"* {doc.page_content} [{doc.metadata}]")

docs_content = "\n\n".join(doc.page_content for doc in docs)

prompt = f"""
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {query}
Context: {docs_content}
Answer:
"""

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

ai_message = llm.invoke(prompt)
print(ai_message)
