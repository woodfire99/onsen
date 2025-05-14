from bs4 import BeautifulSoup
import pandas as pd

results = []

# 파일 번호별 지역 매핑 함수
def get_region(i):
    if 1 <= i <= 4:
        return "北海道"
    elif 5 <= i <= 10:
        return "東北"
    elif 11 <= i <= 13:
        return "東海"
    elif 14 <= i <= 19:
        return "甲信越"
    elif 20 <= i <= 21:
        return "北陸"
    elif 22 <= i <= 26:
        return "近畿（関西）"
    elif 27 <= i <= 29:
        return "中国・四国"
    elif 30 <= i <= 38:
        return "九州・沖縄"
    elif 39 <= i <= 42:
        return "伊豆・箱根"
    elif 43 <= i <= 49:
        return "関東"
    else:
        return "不明"

def extract_access(dd_tag):
    if not dd_tag:
        return []
    # 여러 줄인 경우에도 줄 단위로 나누기
    return [line.strip().replace("\u3000", "") for line in dd_tag.get_text("\n").split("\n") if line.strip()]


# 1~42.html 반복 처리
for i in range(1, 50):
    file_path = f"data/html_data/{i}.html"
    region = get_region(i)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        cards = soup.select("div.c-result_card")
            
        for card in cards:
            name = card.select_one(".result_card_name a")
            lead = card.select_one(".result_card_lead")
            text = card.select_one(".result_card_text")
            abilities = card.select(".result_card_info_ability li")
            onsen_td = card.select_one(".result_card_data td")
            access_dds = card.select(".result_card_accessInfo dd")
            access_car = card.select_one(".result_card_accessInfo .m-icon-car")
            access_train = card.select_one(".result_card_accessInfo .m-icon-train")
            car_info = extract_access(access_car.find_parent("dl").find("dd")) if access_car else []
            station_info = extract_access(access_train.find_parent("dl").find("dd")) if access_train else []

            region_detail = card.select_one(".c-result_card_breadcrumb ul li:last-child a")
            link_tag = card.select_one(".result_card_name a")
            href = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""

            # 절대 URL이면 그대로, 상대 URL이면 붙이기
            url = href if href.startswith("http") else f"https://www.yukoyuko.net{href}"

            data = {
                "name": name.get_text(strip=True) if name else "",
                "lead": lead.get_text(strip=True) if lead else "",
                "text": text.get_text(strip=True) if text else "",
                "ability": [ab.get_text(strip=True) for ab in abilities],
                "onsen_data": onsen_td.get_text(strip=True) if onsen_td else "",
                "access_car": car_info,
                "access_station": station_info,
                "region": region,  # ✅ 지역 추가
                "region_detail": region_detail.get_text(strip=True) if text else "",
                "url":url,
            }

            results.append(data)
        print(f"✅ {file_path} 처리 완료, 카드 수: {len(cards)}")

    except FileNotFoundError:
        print(f"❌ 파일 없음: {file_path}")
    except Exception as e:
        print(f"❌ 오류 발생 ({file_path}): {e}")

# CSV 저장
df = pd.DataFrame(results)
df.to_csv("onsen_result.csv", index=False, encoding="utf-8-sig")
print("✅ onsen_result.csv 저장 완료, 총 레코드 수:", len(results))
