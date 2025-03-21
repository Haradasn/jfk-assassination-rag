import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ 1. JSONLファイルをアップロード
def upload_batch_file(file_path):
    print("📤 JSONLファイルアップロード中...")
    upload = openai.files.create(
        file=open(file_path, "rb"),
        purpose="batch"
    )
    print(f"✅ アップロード完了 File ID: {upload.id}")
    return upload.id

# ✅ 2. Batch Jobを実行
def start_batch_job(file_id):
    print("🚀 Batch実行開始...")
    batch = openai.batches.create(
        input_file_id=file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    print(f"✅ Batchジョブ作成完了！Job ID: {batch.id}")
    print(f"📊 進捗確認はこちら: https://platform.openai.com/batch/{batch.id}")
    return batch.id

if __name__ == "__main__":
    jsonl_path = "vision_batch_job.jsonl"  # 事前に作ったJSONLファイル

    # アップロード → バッチ実行
    file_id = upload_batch_file(jsonl_path)
    batch_id = start_batch_job(file_id)

    print("\n⏳ バッチ実行中。進捗は上記URLから確認！")