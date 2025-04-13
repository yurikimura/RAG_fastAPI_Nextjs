import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

VECTOR_DB_PATH = os.getenv("CHROMA_DB_PATH", "./vectorstore_index")

def get_vectorstore():
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-ada-002")
    try:
        return FAISS.load_local(VECTOR_DB_PATH, embeddings)
    except:
        return FAISS.from_texts(["初期データです"], embedding=embeddings)
