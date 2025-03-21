import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

batch_dir = "batch_splits"  # 分割JSONL格納フォルダ

def upload_and_run_batch(jsonl_path):
    print(f"📤 アップロード開始: {jsonl_path}")
    upload = openai.files.create(
        file=open(jsonl_path, "rb"),
        purpose="batch"
    )
    print(f"✅ アップロード成功 File ID: {upload.id}")

    print(f"🚀 Batchジョブ実行開始 for {jsonl_path}")
    batch = openai.batches.create(
        input_file_id=upload.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    print(f"✅ Batchジョブ登録成功！Batch ID: {batch.id}")
    print(f"🔗 確認リンク: https://platform.openai.com/batch/{batch.id}")
    return batch.id

if __name__ == "__main__":
    # 分割されたファイル順に回す
    for file_name in sorted(os.listdir(batch_dir)):
        if file_name.endswith(".jsonl"):
            jsonl_path = os.path.join(batch_dir, file_name)
            try:
                upload_and_run_batch(jsonl_path)
            except Exception as e:
                print(f"❌ エラー発生: {file_name} - {e}")