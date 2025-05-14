import geopandas as gpd

# 1. 파일 경로 설정 (.shx, .dbf, .prj 등도 동일 폴더에 있어야 함)
shp_path = "data/N03-20240101_01_GML/N03-20240101_01.shp"

# 2. Shapefile 읽기
gdf = gpd.read_file(shp_path)

# 3. 홋카이도 데이터만 필터링
hokkaido = gdf[gdf["N03_001"] == "北海道"].copy()

# 4. 시정촌 이름(N03_004) 기준으로 병합하여 정확히 179개로 정리
simplified = hokkaido.dissolve(by="N03_004", as_index=False).copy()

# 5. 중심점 좌표 계산
simplified["centroid"] = simplified.geometry.centroid
simplified["lat"] = simplified.centroid.y
simplified["lng"] = simplified.centroid.x

# 6. 결과 저장
output_path = "hokkaido_179_municipalities.csv"
simplified[["N03_004", "lat", "lng"]].to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 저장 완료: {output_path}")
