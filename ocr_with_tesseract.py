import os
import fitz  # PyMuPDF
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
from PIL import Image
import io

def ocr_pdf_with_tesseract(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)  # 高解像度で画像化
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))

        # ✅ OCR実行（英語特化）
        text = pytesseract.image_to_string(image, lang='eng')
        full_text += f"\n\n=== Page {i+1} ===\n{text}"

    return full_text

def pipeline(pdf_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(pdf_dir):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, file)
            output_txt_path = os.path.join(output_dir, file.replace('.pdf', '.txt'))

            # 既にあるならスキップ（再実行耐性）
            if os.path.exists(output_txt_path):
                print(f"✅ 既に処理済みスキップ: {file}")
                continue

            try:
                print(f"📖 OCR実行中: {file}")
                ocr_text = ocr_pdf_with_tesseract(pdf_path)

                with open(output_txt_path, 'w') as f:
                    f.write(ocr_text)

                print(f"✅ 完了: {file}")
            except Exception as e:
                print(f"❌ エラー: {file} - {e}")

if __name__ == "__main__":
    pipeline("data", "ocr_results_tesseract")