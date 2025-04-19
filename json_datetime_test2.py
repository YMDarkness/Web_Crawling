import json
import pandas as pd

#csv 파일 읽기
df = pd.read_csv("pay_date_time.csv", encoding="utf-8-sig")

#json 변환
df.to_json("pay_date_time.json", force_ascii=False, indent=4, orient="records")
print(f"pay_date_time.csv를(을) pay_date_time.json으로 변환 완료")
