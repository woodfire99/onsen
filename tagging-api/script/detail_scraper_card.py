import os
import pandas as pd
from bs4 import BeautifulSoup

html_dir = "data/html_detail"
output_path = "data/hotel_card_all.csv"
all_rows = []

def parse_hotel_cards(file_path, onsen_id):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    cards = soup.select("div.pickup-card")
    rows = []

    for card in cards:
        name_tag = card.select_one(".c-cardItem_title")
        name = name_tag.get_text(strip=True) if name_tag else None

        rating_tag = card.select_one(".c-cardItem_review_star")
        rating = float(rating_tag.get("data-points")) if rating_tag and rating_tag.has_attr("data-points") else None

        price_tag = card.select_one("p.value")
        price = price_tag.get_text(strip=True) if price_tag else None

        desc_tag = card.select_one("p.feature-text")
        description = desc_tag.get_text(strip=True) if desc_tag else None

        icons = card.select("ul.feature-iconArea li.feature-iconItem")
        icon_classes = [li.get("class")[1] for li in icons if "is-active" in li.get("class", [])]

        rows.append({
            "id": onsen_id,
            "name": name,
            "rating": rating,
            "price": price,
            "description": description,
            "hot_spring": "ability-hot_spring" in icon_classes,
            "kakenagashi": "ability-kakenagashi" in icon_classes,
            "open_air_bath": "ability-open_air_bath" in icon_classes,
            "private_bath": "ability-private_bath" in icon_classes,
            "pickup_service": "ability-pickup_service" in icon_classes,
        })

    return rows

# 전체 HTML 반복 수집
for idx, filename in enumerate(os.listdir(html_dir)):
    if filename.endswith(".html"):
        onsen_id = filename.replace(".html", "")
        file_path = os.path.join(html_dir, filename)

        try:
            parsed = parse_hotel_cards(file_path, onsen_id)
            if parsed:
                print(f"[{idx}] {onsen_id} → {len(parsed)}개 숙소")
                all_rows.extend(parsed)
            else:
                print(f"[{idx}] {onsen_id} → 숙소 없음")
        except Exception as e:
            print(f"[{idx}] {onsen_id} 실패: {e}")


# 저장
df = pd.DataFrame(all_rows)
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"✅ 완료: {len(df)}건 저장 → {output_path}")
