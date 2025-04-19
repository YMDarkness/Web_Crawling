import json
import pandas as pd

#csv 파일을 pandas의 데이터 프레임으로 읽기
df = pd.read_csv("pay_to.csv", encoding="utf-8-sig")

#키워드 리스트 설정
search_list = ["미국", "ETF", "트럼프"]

#여러 키워드 중 하나라도 포함된 뉴스 필터링
#람다식
#any()
'''
any([False, False, True])  # 결과: True (하나라도 True면 True)
any([False, False, False]) # 결과: False (모두 False면 False)
'''

'''
lambda
df["새로운_컬럼"] = df["기존_컬럼"].apply(lambda x: 처리할_로직(x))

ex 1)
import pandas as pd

# 예제 데이터프레임
data = {"이름": ["철수", "영희", "민수"], "점수": [88, 76, 95]}
df = pd.DataFrame(data)

# 점수가 90 이상이면 'A', 80 이상이면 'B', 나머지는 'C'로 변환
df["학점"] = df["점수"].apply(lambda x: "A" if x >= 90 else "B" if x >= 80 else "C")

print(df)

ex 2)
import pandas as pd

# 예제 데이터
data = {"제목": ["오늘 코스피 급락", "환율 급등 영향", "금리 인상 가능성"]}
df = pd.DataFrame(data)

# 키워드 리스트
search_keywords = ["급락", "인상"]

# 키워드가 포함된 행 필터링
filtered_df = df[df["제목"].apply(lambda title: any(keyword in title for keyword in search_keywords))]

print(filtered_df)

'''
list_filter = df[df["제목"].apply(lambda title: any(keyword in title for keyword in search_list))]

#for문
'''
filtered_rows = []  # 키워드가 포함된 행을 저장할 리스트

for _, row in df.iterrows():  # 데이터프레임의 각 행을 순회
    title = row["제목"]  # 현재 행의 제목 가져오기
    for keyword in search_keywords:  # 키워드 리스트 순회
        if keyword in title:  # 제목에 키워드가 포함되면
            filtered_rows.append(row)  # 해당 행을 리스트에 추가
            break  # 한 키워드라도 찾으면 중복 체크 방지 위해 바로 종료

filtered_df = pd.DataFrame(filtered_rows)  # 리스트를 데이터프레임으로 변환
'''

#json으로 변환
list_filter.to_json("filter_list.json", indent=4, orient="records", force_ascii=False)
print(f"특정 키워드 리스트 '{search_list}'를 포함한 json 파일 생성 완료")
