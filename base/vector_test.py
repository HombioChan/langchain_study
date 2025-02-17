# Create a vector store with a sample text
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

text = "hello"

vectorstore = InMemoryVectorStore.from_texts(
    [text],
    embedding=embeddings,
)

query = "What is LangChain?"

print(vectorstore.similarity_search(query))
# Use the vectorstore as a retriever
retriever = vectorstore.as_retriever()


# Retrieve the most similar text
retrieved_documents = retriever.invoke("What is LangChain?")
print(retrieved_documents)
# show the retrieved document's content
print(retrieved_documents[0].page_content)
