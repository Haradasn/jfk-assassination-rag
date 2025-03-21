import os
import fitz
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def vision_ocr_with_completion(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        image_bytes = pix.tobytes("png")
        b64_img = base64.b64encode(image_bytes).decode('utf-8')

        print(f"📄 GPT Vision OCR中... Page {i+1}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 最新Visionモデル
            messages=[
                {"role": "system", "content": "You are a professional English editor. Extract the text from the image, fix any OCR errors, and rewrite it as clean, readable English."},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                ]}
            ],
            max_tokens=2000
        )
        full_text += f"\n\n=== Page {i+1} ===\n" + response.choices[0].message.content
    return full_text

def pipeline(pdf_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(pdf_dir):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, file)
            output_txt = os.path.join(output_dir, file.replace('.pdf', '.txt'))

            if os.path.exists(output_txt):
                print(f"✅ 既に処理済みスキップ: {file}")
                continue

            try:
                result = vision_ocr_with_completion(pdf_path)
                with open(output_txt, "w") as f:
                    f.write(result)
                print(f"✅ GPT OCR完了: {file}")
            except Exception as e:
                print(f"❌ GPT OCR失敗: {file} - {e}")

if __name__ == "__main__":
    pipeline("data", "gpt_ocr_results")