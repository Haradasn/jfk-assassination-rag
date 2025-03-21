import requests
from bs4 import BeautifulSoup
import os
import re
import time
from tqdm import tqdm
from urllib.parse import urljoin

# 設定
url = 'https://www.archives.gov/research/jfk/release-2025'
save_dir = 'jfk_pdfs'
os.makedirs(save_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
}

# 取得関数（リトライ付き）
def download_file(pdf_url, save_path, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(pdf_url, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            else:
                print(f"⚠️ Status code {response.status_code}: {pdf_url}")
        except requests.exceptions.Timeout:
            print(f"⏳ Timeout: {pdf_url}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(2)  # リトライ前にちょっと休憩
    return False

# ページからPDFリンク抽出
print("🔎 PDFリンク抽出中...")
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

pdf_links = set()
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if re.search(r'\.pdf$', href, re.IGNORECASE):
        full_url = urljoin(url, href)
        pdf_links.add(full_url)

print(f"✅ 見つかったPDF数: {len(pdf_links)}")

# PDFダウンロード開始（進捗付き）
for pdf_url in tqdm(pdf_links, desc="📥 Downloading PDFs"):
    filename = os.path.join(save_dir, os.path.basename(pdf_url))
    success = download_file(pdf_url, filename)
    if not success:
        print(f"❌ ダウンロード失敗: {pdf_url}")
    time.sleep(1)  # サーバーに優しく1秒休憩

print("🎉 全PDFダウンロード完了！")