import os
import json
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

batch_results_dir = "batch_results"   # ダウンロードしたjsonlフォルダ
chroma_dir = "chroma_db"
os.makedirs(chroma_dir, exist_ok=True)

all_docs = []

# ✅ 1. JSONL全読み込み
for file in os.listdir(batch_results_dir):
    if not file.endswith(".jsonl"):
        continue

    with open(os.path.join(batch_results_dir, file), "r") as f:
        for line in f:
            data = json.loads(line)
            custom_id = data.get("custom_id", "unknown")

            # ✅ 正しいパスでGPTのcontent取り出す
            try:
                text = data["response"]["body"]["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                print(f"❌ データ欠損スキップ: {custom_id}")
                continue

            if not text.strip():
                print(f"⚠️ 空テキストスキップ: {custom_id}")
                continue

            # ✅ LangChain用ドキュメント化
            all_docs.append(Document(page_content=text, metadata={"source": custom_id}))

print(f"✅ 読み込んだドキュメント数: {len(all_docs)}")

# ✅ 2. チャンク分割
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(all_docs)

if not chunks:
    print("❌ チャンクが空です。処理を終了します。")
    exit()

# ✅ 3. ベクトル化してChroma保存
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory=chroma_dir)
vectorstore.persist()

print("✅ 全バッチ結果 → ChromaDB ベクトル化完了！")