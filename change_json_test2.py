import json
import csv
import pandas as pd

#csv 파일 읽어오기
csv_file = "pay_to.py"
json_file = "pay_to.json"

#csv 파일을 pandas 데이터 프레임으로 읽기
#df = pd.read_csv(csv_filename, encoding="utf-8-sig")
df = pd.read_csv("pay_to.csv")

#json 형식으로 변환 후 저장
df.to_json(json_file, force_ascii=False, orient="records", indent=4)
print(f"{json_file}이 생성되었습니다")
