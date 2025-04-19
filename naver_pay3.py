import csv

#저장된 csv 파일 불러오기
filepath = "pay.csv"

#csv 파일 읽기
with open(filepath, mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    #첫 번째 행(헤더) 건너뛰기
    next(reader)

    for idx, row in enumerate(reader, 1):
        #빈 줄 방지
        if len(row) > 1:
            #strip("[]") + replace("'", "").replace(", ", "")로 불필요한 기호 제거
            title = row[1].strip("[]").replace("'", "").replace(", ", "")
            print(f"{idx}. {title}")
