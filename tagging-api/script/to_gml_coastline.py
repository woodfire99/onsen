import geopandas as gpd
import os
from glob import glob
import pandas as pd

# 1. 해안선 .shp 파일이 들어있는 폴더
shp_folder = "data/coastline_gml"  # 여기에 39개 파일이 있다고 가정

# 2. 모든 .shp 파일 찾기
shp_files = glob(os.path.join(shp_folder, "*.shp"))

# 3. GeoDataFrame으로 병합
gdf_list = [gpd.read_file(shp) for shp in shp_files]
merged_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True), crs=gdf_list[0].crs)

# 4. 하나의 .shp 파일로 저장
merged_path = "data/merged_coastlines.shp"
merged_gdf.to_file(merged_path, encoding="utf-8")

print(f"✅ 병합 완료: {merged_path}")
