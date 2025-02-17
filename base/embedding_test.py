from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

text = "LangChain is the framework for building context-aware reasoning applications"
floats = embeddings.embed_query(text)
print(floats)