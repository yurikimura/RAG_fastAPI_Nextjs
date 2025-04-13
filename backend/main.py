from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import pandas as pd

from upload import router as upload_router
from qa.loader import get_vectorstore
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(upload_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = get_vectorstore()

class ChatRequest(BaseModel):
    question: str

def generate_index():
    # CSVファイルの読み込み
    data = pd.read_csv("./documents/takadakenshi.csv")
    
    # 埋め込みの生成
    embeddings = OpenAIEmbeddings()
    texts = data['column_name'].tolist()  # 'column_name'は実際のカラム名に置き換えてください
    embeddings_list = [embeddings.embed(text) for text in texts]
    
    # インデックスの作成と保存
    index = FAISS.from_embeddings(embeddings_list, texts)
    index.save_local("vectorstore")

@app.post("/chat")
async def chat(request: ChatRequest):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0),
        retriever=retriever,
    )

    result = chain.run(request.question)
    return {"answer": result}

