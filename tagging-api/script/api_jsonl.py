import pandas as pd
import requests

csv_data = "data/onsen_p_5.csv"

def summarize_onsen(row):
    prompt = f"""以下の情報をもとに、自然な温泉紹介文を1〜2文で生成してください。

名前: {row['name']}
説明: {row['lead']} {row['text']}
効能: {row['effects']}
泉質: {row['water_trait']}
アクセス: {row['near_region_station']}から{row['near_region_station_minute']}分
"""

    payload = {
        "model": "elyza-7b",  # text-generation-webui에서 설정한 모델명
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 128,
        "stop": ["</s>", "ユーザー:", "システム:"]
    }

    try:
        response = requests.post("http://host.docker.internal:5000/v1/chat/completions", json=payload, timeout=30)
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ 요약 실패: {row['name']} → {e}")
        return "エラー"

# 🔄 CSV 로드 & 5개만 처리
df = pd.read_csv(csv_data)
df_sample = df.head(5).copy()

# ✅ 요약 생성
df_sample["summary"] = df_sample.apply(summarize_onsen, axis=1)

# 💾 저장
df_sample.to_csv("data/onsen_p_5_summary.csv", index=False, encoding="utf-8-sig")
print("✅ 저장 완료: data/onsen_p_5_summary.csv")
