import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

VECTOR_DB_PATH = "vectorstore"

def get_vectorstore():
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    faiss_path = os.path.join(VECTOR_DB_PATH, "index.faiss")
    if os.path.exists(faiss_path):
        return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("FAISS index not found. Initializing with sample texts...")
        sample_texts = [
            "これは初期化用のサンプルテキストです。",
            "このテキストはFAISSの初期化に使用されます。",
            "新しいドキュメントがアップロードされると、このサンプルは上書きされます。"
        ]
        return FAISS.from_texts(sample_texts, embeddings)
