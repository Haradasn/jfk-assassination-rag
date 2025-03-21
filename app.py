import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="JFK RAG Search（推論＋スコア表示）", layout="wide")
st.title("📚 JFK Document RAG Search")

query = st.text_input("質問を入力してください（例: オズワルドとCIAの関係は？）")

if st.button("検索する"):
    with st.spinner("検索中..."):
        embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
        vectorstore = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding
        )

        # ✅ チャンク数制限して取得（上位10件）
        retrieved_docs = vectorstore.similarity_search(query, k=10)

        # ✅ ドキュメント結合
        docs_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

        # ✅ System Prompt強化
        system_prompt = """
あなたはJFK関連の専門家AIです。
以下のドキュメントを読み取り、質問に答えてください。
ドキュメント内に直接的な回答が無い場合は、文脈から推測・補完して回答してください。
絶対に「わかりません」などと言わず、ドキュメントから得られる情報・状況証拠・背景知識を元に考察してください。
        """

        # ✅ Chat APIへ直接投げる
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"【ドキュメント】\n{docs_content}\n\n【質問】\n{query}"}
        ]

        llm_response = llm.invoke(messages)

        # ✅ 回答表示
        st.subheader("📌 回答（推論・補完あり）")
        st.write(llm_response.content)

        # ✅ 参照ソース表示（チャンク10件）
        st.subheader("📚 参照したソース")
        for doc in retrieved_docs:
            st.write(f"- {doc.metadata.get('source')}")