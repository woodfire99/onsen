import pandas as pd

# JP.txt를 탭으로 읽기
df = pd.read_csv("data/JP.txt", sep='\t', header=None, dtype=str)

# 컬럼 이름 지정
df.columns = [
    "geonameid", "name", "asciiname", "alternatenames",
    "latitude", "longitude", "feature_class", "feature_code",
    "country_code", "cc2", "admin1_code", "admin2_code",
    "admin3_code", "admin4_code", "population", "elevation",
    "dem", "timezone", "modification_date"
]

# 홋카이도 (admin1_code == '01') 필터링
df_hokkaido = df[df["admin1_code"] == '01']

# CSV로 저장
df_hokkaido.to_csv("data/hokkaido_cities.csv", index=False, encoding="utf-8-sig")
