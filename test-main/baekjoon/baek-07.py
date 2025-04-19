##심화 1

##백준 25083
## print("         ,r'\"7")
## print("r`-_   ,'  ,/")
## print(" \\. \". L_r'")
## print("   `~\\/")
## print("      |")
## print("      |")


##백준 3003
## chess = [1, 1, 2, 2, 2, 8]
## a = list(map(int, input("현재 체스 말 수 (킹 퀸 룩 비숍 나이트 폰): ").split()))
## print("부족한 체스 말 : ")
## for i in range(6):
##     print(chess[i] - a[i], end = " ")


##백준 2444
## a = int(input())
## for i in range(1, a):
##     print(' ' * (a - i) + "*" * (2 * i - 1)) #입력받은 숫자가 n일 때, 줄의 개수와 가운데 줄 별의 개수가 n*2-1 임에 유의
## for i in range(a, 0, -1):
##     print(' ' * (a - i) + "*" * (2 * i - 1))


##백준 10812
## a, b = map(int, input().split())
## box = [i + 1 for i in range(a)]
## for _ in range(b):
##     i, j, k = map(int, input().split())
##     box = box[:i - 1] + box[k - 1:j] + box[i - 1:k - 1] + box[j:]
## for c in box:
##     print(c, end=' ')


##백준 10988
## word = list(str(input()))
## if list(reversed(word)) == word: #reversed() 역방향 함수
##     print(1)
## else:
##     print(0)


##백준 1157
## word = input().upper()
## word_list = list(set(word))
## cnt = []
## for i in word_list():
##     count = word.count
##     cnt.append(count(i))
## if cnt.count(max(cnt)) > 1:
##     print("?")
## else:
##     print(word_list[cnt.index(max(cnt))])


##백준 4344
## a = int(input())
## for _ in range(a):
##     nums = list(map(int, input().split()))
##     avg = sum(nums[1:]) / nums[0] #평균을 구한다 (nums[0] : 학생수, nums[1:] : 점수)
##     cnt = 0
##     for score in nums[1:]:
##         if score > avg:
##             cnt += 1 #평균 이상인 학생 수
##         rate = cnt / nums[0] * 100
##         print(f'{rate:.3f}%') #f-string 표기법을 이용, 소수점 자릿수 지정


##백준 2941
## croatia = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]
## word = input()
## for i in croatia:
##     word = word.replace(i, "*")  #input 변수와 동일한 이름의 변수, replace() 함수를 사용한 문자열 원형을 변형시키지 않는 비파괴적 함수
## print(len(word))


##백준 1316
a = int(input())
group_wrod = 0
for _ in range(a):
    word = input()
    error = 0
    for index in range(len(word) - 1):  # 인덱스 범위 생성 : 0부터 단어개수 -1까지
        if word[index] != word[index + 1]:  # 연달은 두 문자가 다를 경우
            new_word = word[index + 1 :]  # 현재글자 이후 문자열을 새로운 단어로 생성
            if new_word.count(word[index]) > 0:  # 남은 문자열에서 현재글자가 있었다면
                error += 1  # error에 1씩 증가
    if error == 0:
        group_wrod += 1  # error가 0이면 group_word
print(group_wrod)


##백준 25206
import sys

data_dict = {
    "A+ : 4.5",
    "A0 : 4.0",
    "B+ : 3.5",
    "B0 : 3.0",
    "C+ : 2.5",
    "C0 : 2.0",
    "D+ : 1.5",
    "D0 : 1.0",
    "F : 0.0",
}  # 딕셔너리로 성적과 학점을 키와 값으로 등록해준다
result = 0
total = 0
for _ in range(0, 20, 1):
    input_data = sys.stdin.readline().split()
    if (
        input_data[2] == "P"
    ):  # P/F는 하나씩 있으며, P는 패스 F는 0을 입력할 수 있도록 한다. -> 위 딕셔너리 값에서 F를 지정하고 input_data [2] 번째 위치에 P가 입력되면 건너뛴다.
        continue
    total += float(input_data[1])
    result += float(input_data[1]) * data_dict[input_data[2]]
GPA = result / total
conversion = format(GPA, ".6f")
print(conversion)
