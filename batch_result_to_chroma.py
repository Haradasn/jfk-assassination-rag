import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

ocr_text_dir = "ocr_texts"  # さっきの保存フォルダ
chroma_dir = "chroma_db"
os.makedirs(chroma_dir, exist_ok=True)

# ✅ OCR済みテキストを全部ロード
all_docs = []
for file in os.listdir(ocr_text_dir):
    if file.endswith('.txt'):
        loader = TextLoader(os.path.join(ocr_text_dir, file))
        all_docs.extend(loader.load())

# ✅ チャンク分割（長文対応）
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(all_docs)

# ✅ Embedding生成＆Chroma登録
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory=chroma_dir)
vectorstore.persist()

print("✅ OCR結果 → ベクトル化完了！ChromaDB構築済み！")