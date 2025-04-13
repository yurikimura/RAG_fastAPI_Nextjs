from fastapi import FastAPI
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from qa.loader import get_vectorstore
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = get_vectorstore()

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        temperature=0,
        api_key=os.environ["OPENAI_API_KEY"]
    ),
    retriever=vectorstore.as_retriever(),
)

@app.get("/chat")
def chat(query: str):
    result = qa_chain.run(query)
    return {"response": result}
