import os
import pandas as pd
from bs4 import BeautifulSoup

html_dir = "data/html_detail"
output_path = "data/onsen_detail_info.csv"
all_rows = []

def parse_onsen_detail_info(html_path, onsen_id):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 역사/소개 텍스트
    history = None
    history_tag = soup.select_one("p.feature_contents_txt")
    if history_tag:
        history = history_tag.get_text(strip=True)

    # 효능
    effects = None
    dd_tags = soup.select("dd.feature_contents_dl_dd")
    if len(dd_tags) >= 2:
        effects = dd_tags[1].get_text(strip=True)

    return {
        "id": onsen_id,
        "description_text": history,
        "effects": effects
    }

# 전체 HTML 반복 수집
for idx, filename in enumerate(os.listdir(html_dir)):
    if filename.endswith(".html"):
        onsen_id = filename.replace(".html", "")
        file_path = os.path.join(html_dir, filename)

        try:
            parsed = parse_onsen_detail_info(file_path, onsen_id)
            all_rows.append(parsed)
            print(f"[{idx}] {onsen_id} → 완료")
        except Exception as e:
            print(f"[{idx}] {onsen_id} 실패: {e}")

# 저장
df = pd.DataFrame(all_rows)
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"✅ 완료: {len(df)}건 저장 → {output_path}")
