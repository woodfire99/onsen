from bs4 import BeautifulSoup
import pandas as pd
import os
import requests

results = []
BASE_IMG_URL = "https://static.yukoyuko.net"
# 저장 디렉토리 생성
os.makedirs("data/onsen_images", exist_ok=True)

# 1~49.html 반복 처리
for i in range(1, 50):
    file_path = f"data/html_data/{i}.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        cards = soup.select("div.c-result_card")

        for card in cards:
            name_tag = card.select_one(".result_card_name a")
            img_tag = card.select_one(".result_card_left img")

            name = name_tag.get_text(strip=True) if name_tag else ""
            img_url = img_tag["src"] if img_tag else ""
            if img_url and img_url.startswith("./"):
                img_url = BASE_IMG_URL + img_url[1:]  # ./ 제거하고 붙이기
            elif img_url and img_url.startswith("/"):
                img_url = BASE_IMG_URL + img_url

            # 이미지 다운로드
            if name and img_url:
                safe_name = name.replace("/", "_").replace(" ", "_")  # 파일명 안전 처리
                img_ext = os.path.splitext(img_url)[-1].split("?")[0]  # 확장자 제거
                img_path = f"data/onsen_images/{safe_name}{img_ext}"

                try:
                    res = requests.get(img_url, timeout=10)
                    with open(img_path, "wb") as f_img:
                        f_img.write(res.content)
                    print(f"✅ 이미지 저장 완료: {img_path}")
                except Exception as e:
                    print(f"❌ 이미지 다운로드 실패: {img_url} → {e}")
                    img_path = ""

            else:
                img_path = ""

            results.append({
                "name": name,
                "img_url": img_url,
                "img_path": img_path
            })

        print(f"✅ {file_path} 처리 완료, 카드 수: {len(cards)}")

    except FileNotFoundError:
        print(f"❌ 파일 없음: {file_path}")
    except Exception as e:
        print(f"❌ 오류 발생 ({file_path}): {e}")

# CSV 저장
df = pd.DataFrame(results)
df.to_csv("onsen_result_with_images.csv", index=False, encoding="utf-8-sig")
print("✅ CSV 저장 완료, 총 레코드 수:", len(results))
