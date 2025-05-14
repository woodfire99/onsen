import pandas as pd
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CSV 파일 로드
df_location = pd.read_csv("data/onsen_with_location - original.csv")
df_url = pd.read_csv("data/onsen_result.csv")

# lat 또는 lng가 결측인 행 필터
df_to_update = df_location[~(df_location["lat"].isna() | df_location["lng"].isna())].copy()


# name 기준으로 url 붙이기
df_to_update = df_to_update.merge(df_url[["name", "url"]], on="name", how="left")

# 드라이버 설정
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

def extract_latlng_from_href(href):
    match = re.search(r"ll=([\d.]+),([\d.]+)", href)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

def fetch_latlng(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pageBlock.googlemap a[href*="maps.google.com"]'))
        )
        a_tag = driver.find_element(By.CSS_SELECTOR, 'div.pageBlock.googlemap a[href*="maps.google.com"]')
        href = a_tag.get_attribute("href")
        latlng = extract_latlng_from_href(href)
        if latlng != (None, None):
            print(f"✅ 좌표 추출 성공: {latlng}")
        else:
            print(f"⚠️ 좌표 없음: {url}")
        return latlng
    except Exception as e:
        print(f"❌ 예외 발생: {url} → {e}")
        return None, None

# 추출 및 반영
for i, row in df_to_update.iterrows():
    lat, lng = fetch_latlng(row["url"])
    df_location.loc[df_location["name"] == row["name"], "lat"] = lat
    df_location.loc[df_location["name"] == row["name"], "lng"] = lng
    print(f"✅ {row['name']} → {lat}, {lng}")
    time.sleep(1.5)

# 저장
driver.quit()
df_location.to_csv("data/onsen_with_location - original.csv", index=False, encoding="utf-8-sig")
print("✅ 완료: 좌표 갱신 완료 및 저장됨")
