import undetected_chromedriver as uc
import time
import os
import pandas as pd

# 설정
csv_main = "data/onsen_result.csv"
save_dir = "data/html_detail"
os.makedirs(save_dir, exist_ok=True)

# 드라이버 생성
options = uc.ChromeOptions()
options.add_argument("--headless")  # 안 보이게 실행 (필요 없으면 제거)
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

driver = uc.Chrome(options=options)

# CSV 읽기
df = pd.read_csv(csv_main)
urls = df["url"].dropna().unique()

# 저장 루프
for i, url in enumerate(urls):
    try:
        onsen_id = url.rstrip("/").split("/")[-1]
        save_path = os.path.join(save_dir, f"{onsen_id}.html")

        if os.path.exists(save_path):
            print(f"[{i}] 이미 존재: {onsen_id}")
            continue

        driver.get(url)
        time.sleep(3.0)  # 렌더링 대기

        html = driver.page_source
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[{i}] 저장 완료: {onsen_id}")

    except Exception as e:
        print(f"[{i}] 실패: {url} → {e}")

driver.quit()
