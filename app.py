import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.title("📚 JFK Document RAG Search")

query = st.text_input("質問を入力してください")
if st.button("検索"):
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=None)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="map_reduce",
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain({"query": query})

    st.subheader("📌 回答")
    st.write(result["result"])

    st.subheader("📚 参照元")
    for doc in result["source_documents"]:
        st.write(f"- {doc.metadata['source']}")