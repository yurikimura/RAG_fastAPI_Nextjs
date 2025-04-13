from fastapi import APIRouter, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vectorstore"

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 保存
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # ローダー選定
    if file.filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file.filename.endswith(".csv"):
        loader = CSVLoader(file_path)
    else:
        return {"error": "Unsupported file type"}

    # ドキュメント読み込み
    docs = loader.load()

    # ベクトル化
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 保存
    vectorstore.save_local(VECTOR_DB_DIR)

    return {"message": f"{file.filename} uploaded and indexed successfully"}
