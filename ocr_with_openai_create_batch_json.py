import os
import fitz
import base64
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

os.makedirs("batch_payload", exist_ok=True)

with open("vision_batch_job.jsonl", "w") as batch_file:
    for pdf_file in os.listdir("data"):
        if not pdf_file.endswith(".pdf"):
            continue
        pdf_path = os.path.join("data", pdf_file)
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")
            b64_img = base64.b64encode(image_bytes).decode('utf-8')

            # ✅ JSONL形式でBatch用リクエストを作る
            payload = {
                "custom_id": f"{pdf_file}_page_{page_num+1}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are an OCR assistant. Extract clean English text from this image."},
                        {"role": "user", "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                        ]}
                    ],
                    "max_tokens": 2000
                }
            }
            batch_file.write(json.dumps(payload) + "\n")

print("✅ Batch用 JSONL 生成完了！")