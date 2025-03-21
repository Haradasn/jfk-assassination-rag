import os
import openai
import requests
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

save_dir = "batch_results"
os.makedirs(save_dir, exist_ok=True)

all_batches = []
next_page = None

print("📥 Batch一覧をすべて取得中...")

# ✅ ページネーション対応で全件取得
while True:
    response = openai.batches.list(limit=200, after=next_page) if next_page else openai.batches.list(limit=200)
    all_batches.extend(response.data)

    if not response.has_more:
        break
    next_page = response.data[-1].id

print(f"✅ 総バッチ数: {len(all_batches)} 件")

# ✅ 各バッチの結果をダウンロード
for batch in all_batches:
    batch_id = batch.id
    status = batch.status
    print(f"{batch_id} {status}")

    if status != "completed":
        print(f"❌ 未完了のためスキップ")
        continue

    output_file_id = batch.output_file_id
    download_url = f"https://api.openai.com/v1/files/{output_file_id}/content"
    out_file = os.path.join(save_dir, f"{batch_id}.jsonl")

    # ✅ すでにDL済みならスキップ
    if os.path.exists(out_file):
        print(f"✅ 既にダウンロード済みスキップ → {out_file}")
        continue

    # ✅ リトライ付きダウンロード
    for attempt in range(5):
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(download_url, headers=headers, timeout=120)
            if response.status_code == 200:
                with open(out_file, "wb") as f:
                    f.write(response.content)
                print(f"✅ {batch_id} ダウンロード完了 → {out_file}")
                break
            elif response.status_code == 429:
                print(f"⚠️ レート制限 429 → 30秒待機 (Attempt {attempt+1}/5)")
                time.sleep(30)
            else:
                print(f"❌ {batch_id} ダウンロード失敗: {response.status_code} - {response.text}")
                break
        except requests.exceptions.Timeout:
            print(f"⚠️ タイムアウト発生 → 30秒待機 (Attempt {attempt+1}/5)")
            time.sleep(30)
    else:
        print(f"❌ {batch_id} リトライ限界、スキップ")