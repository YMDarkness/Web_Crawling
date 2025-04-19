import csv

#키워드 선택
search_keyword = "미국"

with open("pay.csv", mode="r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    #헤더 건너뛰기
    next(reader)

    for idx, row in enumerate(reader, 1):
        if search_keyword in row[1]:
            if len(row) > 1 and search_keyword in row[1]:
                #strip("[]").replace("'", "")로 []와 '을 제거해 리스트 표시 없앰
                text = row[1].strip("[]").replace("'", "")
                #리스트 형태로 된 단어들을 합치면서 띄어쓰기 추가
                #join(text.split(", "))으로 ,와 공백을 기준으로 단어들을 다시 하나의 문자열로 합침
                text = " ".join(text.split(", "))
            print(f"{idx}. {text}")
