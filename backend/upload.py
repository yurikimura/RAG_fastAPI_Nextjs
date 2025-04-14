from fastapi import APIRouter, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil

UPLOAD_DIR = "uploads"
VECTOR_DB_DIR = "vectorstore"

router = APIRouter()

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    # 既存のベクトルストアを削除
    if os.path.exists(VECTOR_DB_DIR):
        shutil.rmtree(VECTOR_DB_DIR)
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # ファイルを保存
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

    # テキスト分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    splits = text_splitter.split_documents(docs)

    # ベクトル化
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    
    # 既存のベクトルストアを読み込むか、新規作成
    faiss_path = os.path.join(VECTOR_DB_DIR, "index.faiss")
    if os.path.exists(faiss_path):
        vectorstore = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(splits)
    else:
        vectorstore = FAISS.from_documents(splits, embeddings)

    # 保存
    vectorstore.save_local(VECTOR_DB_DIR)

    # 一時ファイルを削除
    os.remove(file_path)

    return {"message": f"{file.filename} uploaded and indexed successfully"}
