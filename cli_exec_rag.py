from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ✅ Chromaから呼び出し
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=None)
retriever = vectorstore.as_retriever()

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=retriever,
    return_source_documents=True
)

# ✅ 質問する
query = "What did the document say about Lee Harvey Oswald?"
result = qa_chain({"query": query})

print("\n📌 回答:")
print(result["result"])
print("\n📚 参照したドキュメント:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata['source']}")