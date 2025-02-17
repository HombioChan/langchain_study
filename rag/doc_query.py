from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="../db/chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

query = "What it does to your dignity"

results = vector_store.similarity_search_with_score(query, k=3)

for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")

retriever = vector_store.as_retriever(
    search_type="mmr",
    score_threshold=0.5,
    search_kwargs={'k': 6, 'lambda_mult': 0.25}
)

results = retriever.invoke(query)
for doc in results:
    print(f"* {doc.page_content} [{doc.metadata}]")
