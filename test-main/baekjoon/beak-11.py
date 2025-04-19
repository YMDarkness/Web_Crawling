##기하: 직사각형과 삼각형

##백준 27323
a = int(input())
b = int(input())
print(a * b)


##백준 1085
a, b, x, y = map(int, input().split())
print(min(a, b, x - a, y - b))


##백준 3009
x = []
y = []
for _ in range(3):
    a, b = map(int, input().split())
    x.append(a)  ##x좌표 3개 추가
    y.append(b)  ##y좌표 3개 추가
for i in range(3):
    if x.count(x[i]) == 1:  ##x좌표 중 1개인것을 발견
        a4 = x[i]
    if x.count(y[i]) == 1:  ##y좌표 중 1개인것을 발견
        b4 = y[i]
print(a4, b4)


##백준 15894
a = int(input())
print(a * 4)
##등차수열의 합 문제


##백준 9063
a = int(input())
x, y = [], []
for i in range(a):
    x1, y1 = map(int, input().split())
    x.append(x1)
    y.append(y1)
w = max(x) - min(x)  ##대지의 가로 = 입력된 모든 점들의 x좌표 중 가장 큰 값 - 가장 작은 값
h = max(y) - min(y)  ##대지의 세로 = 입력된 모든 점들의 y좌표 중 가장 큰 값 - 가장 작은 값
print(w * h)


##백준 10101
a = int(input())
b = int(input())
c = int(input())
if a + b + c == 180:
    if a == b == c == 60:
        print("Equilateral")
    elif a == b or a == c or b == c:
        print("Isosceles")
    else:
        print("Scalene")
else:
    print("Error")


##백준 5073
while True:
    a, b, c = map(int, input().split())
    if a == b == c == 0:
        break
    if sum((a, b, c)) - min((a, b, c)) <= max((a, b, c)):
        print("Invalid")
    elif a == b == c:
        print("Equilateral")
    elif a == b or a == c or b == c:
        print("Isosceles")
    else:
        print("Scalene")


##백준 14215
list = sorted(map(int, input().split()))
res = list[0] + list[1] + min(list[2], list[0] + list[1] - 1)
print(res)
##작은 두 변의 길이의 합이 제일 긴 변의 길이보다 커야 된다는 점을 사용
