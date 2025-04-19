import json
import pandas as pd

#csv 파일을 pandas의 데이터 프레임으로 읽기
df = pd.read_csv("pay_to.csv", encoding="utf-8-sig")

#키워드 선정
search_keyword = "인상"

#키워드가 포함된 내용 필터링
filters = df[df["제목"].str.contains(search_keyword, na=False)]

#필터링 데이터를 json으로 저장
filters.to_json("keyword_filter.json", force_ascii=False, orient="records", indent=4)
print(f"특정 키워드 '{search_keyword}'를 포함한 'keyword_filter.json'파일이 생성되었습니다")

'''
filters = df.to_json("keyword_filter.json", force_ascii=False, orient="records", indent=4)
#filters 변수에 필터링된 데이터프레임을 저장했지만, 
#JSON 파일로 저장할 때 df.to_json(...)을 사용하면서 
#필터링된 데이터가 아닌 전체 데이터(df)를 저장하고 있어 문제가 발생하였다.

filters.to_json("keyword_filter.json", force_ascii=False, orient="records", indent=4)
#filters = df.to_json를 filters.to_json 변환하니 정상 출력됨
'''
