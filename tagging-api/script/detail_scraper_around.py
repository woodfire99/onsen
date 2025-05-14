import os
import pandas as pd
from bs4 import BeautifulSoup

html_dir = "data/html_detail"
output_path = "data/onsen_related_info.csv"
rows = []

def extract_cards(soup, section_class, content_type, onsen_id):
    section = soup.select_one(f"section.{section_class}")
    if not section:
        return []

    cards = section.select("div.c-cardItem")
    result = []

    for card in cards:
        # 이름
        name_tag = card.select_one("p.c-cardItem_title span")
        name = name_tag.get_text(strip=True) if name_tag else None

        # 상세 타입 (아이콘)
        icon_tag = card.select_one("p.c-cardItem_title i")
        type_detail = icon_tag.get("title") if icon_tag and icon_tag.has_attr("title") else None

        # URL
        parent_a = card.find_parent("a")
        url = parent_a.get("href") if parent_a and parent_a.has_attr("href") else None

        # 이벤트 날짜만 추출
        date = None
        if content_type == "イベント":
            date_tag = card.select_one("p.c-cardItem_lead")
            date = date_tag.get_text(strip=True) if date_tag else None

        if name:
            result.append({
                "id": onsen_id,
                "type": content_type,
                "name": name,
                "type_detail": type_detail,
                "url": url,
                "date": date
            })

    return result


# 전체 HTML 반복
for idx, filename in enumerate(os.listdir(html_dir)):
    if filename.endswith(".html"):
        onsen_id = filename.split("_")[0]
        path = os.path.join(html_dir, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            rows.extend(extract_cards(soup, "pageBlock-spot", "観光", onsen_id))
            rows.extend(extract_cards(soup, "pageBlock-event", "イベント", onsen_id))
            rows.extend(extract_cards(soup, "pageBlock-onsen", "温泉地", onsen_id))

            print(f"[{idx}] {onsen_id} 처리 완료")
        except Exception as e:
            print(f"[{idx}] {onsen_id} 실패: {e}")

# 저장
df = pd.DataFrame(rows, columns=["id", "type", "name", "type_detail", "url", "date"])
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 총 {len(df)}건 저장 → {output_path}")
