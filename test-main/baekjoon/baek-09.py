##일반 수학 1

##백준 2745
a, b = input().rstrip().split()  ##rstrip() = 오른쪽 공백 삭제
print(
    int(a, int(b))
)  ##int 함수를 활용해 n진법을 10진법으로 변환이 된다. 형식은 int(변환할 String, n진법)으로 사용, n진법은 int형으로 입력한다


##백준 11005
a, b = map(int, input().split())
c = ""
array = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"  ##진법의 인덱스를 정의 하기위한 array문자열 정의(36진법 이하)
while a:
    c += str(array[a % b])  ##a가 0이 될때까지 c라는 문자에 array[a % b]가 의미하는 나머지 문자를 추가
    a //= b  ##a를 a//b로 초기화
print(c[::-1])  ##뒤집어 출력


##백준 2720
c = [25, 10, 5, 1]  ##쿼터 다임, 니켈, 페니
t = int(input())
for _ in range(t):
    c = int(input())
    res = []  ##개수를 담음
    for i in c:
        res.append(c // i)  ##몫
        c = c % i  ##나머지 다시 c에 할당
    print(*res)  ##한줄 출력


##백준 2903
print((2 ** int(input()) + 1) ** 2)  ##한변에 놓일 점의 개수를 구한 뒤 제곱, (2^n + 1)^2


##백준 2292
n = int(input())
b = 1  ##벌집의 개수 1개부터 시작
c = 1
while n > b:
    b += 6 * c  ##벌집이 6의 배수로 증가
    c += 1  ##반복문을 반복하는 횟수
print(c)


##백준 1193
n = int(input())
line = 1
while n > line:
    n -= line  ##각 line에서 n이 몇번째에 위치하는지 알 수 있다.
    line += 1  ## line이 짝수일때와 홀수일때 분모 분자의 증감 양상이 다르다.
if line % 2 == 0:  ##짝수 라인, 짝수일때는 분모 -1씩 분자 +1씩, 홀수일때는 분모 +1씩 분자 -1씩 증감한다.
    a = n
    b = line - n + 1
else:
    a = line - n + 1
    b = n
print(a, "/", b, sep="")  ##출력시 sep=""를 써서 구분자를 변경해준다.


##백준 2869
import math

a, b, c = map(int, input().split())  ##a = 올라가는 길이, b = 떨어지는 길이, c = 나무 높이
day = math.ceil(c - a) / (a - b) + 1
print(day)


##백준 10757
a, b = map(int, input().split())
print(a + b)
