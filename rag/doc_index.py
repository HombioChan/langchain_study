from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# index
## 1.load
with open("../doc/state_of_the_union.txt") as f:
    state_of_the_union = f.read()

## 3.spit
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
documents = text_splitter.create_documents([state_of_the_union])

## 3. store
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="../db/chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)


