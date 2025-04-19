##약수, 배수와 소수

##백준 5086
while True:
    x, y = map(int, input().split())
    if x == 0 and y == 0:
        break
    if y % x == 0:  ##약수인 경우
        print("Factor")
    elif x % y == 0:  ##배수인 경우
        print("Multiple")
    else:  ##둘다 아님
        print("Neither")


##백준 2501
a, b = map(int, input().split())
list = []
for i in range(1, a + 1, 1):  ##for문을 돌며, 약수일 경우 리스트에 추가
    if a % i == 0:
        list.append(i)
if len(list) >= b:  ##약수의 개수가 b보다 크거나 같으면 값을 출력
    print(list[b - 1])
else:
    print(0)


##백준 9506
while True:
    list = []
    total = 0  ##약수의 합 저장
    a = int(input())
    if a == -1:  ##-1이 입력되기 전까지 무한반복하며 숫자 입력, 자기 자신을 제외한 약수를 리스트에 저장
        break
    for i in range(1, a // 2 + 1):
        if a % i == 0:
            list.append(i)
            total += i
    if total == a:
        temp = "+".join(str(i) for i in list)
        print(a, "=", temp)
    else:
        print("{} is NOT perfect".format(a))


##백준 1978
a = int(input())
n = map(int, input().split())
s = 0
for i in n:
    error = 0
    if i > 1:
        for j in range(2, i):  ##2부터 a - 1까지
            if i % 1 == 0:
                error += 1  ##2부터 a - 1까지 나눈 몫이 0이면 error가 증가
        if error == 0:
            s += 1  ##error가 없으면 소수
print(s)


##백준 2581
sn = int(input())
ln = int(input())
sl = []
for i in range(sn, ln + 1):
    error = 0
    if n > 1:
        for i in range(2, n):  ##2부터ㅓ n - 1까지
            if n % i == 0:
                error += 1
                break  ##2부터 n - 1까지 나눈 몫이 0이면 error가 증가하고 for문 종료
            if error == 0:
                sl.append(n)  ##error가 없으면 소수 리스트에 추가
if len(sl) > 0:
    print(sum(sl))
    print(min(sl))
else:
    print(-1)


##백준 11653
n = int(input())
i = 2
while n > 1:
    if n % i == 0:
        n = n / i
        print(i)
        i = 2
    else:
        i += 1
##수를 입력 받고 n이 1보다 클 동안 2 이상의 작은 수로 반복해 나누면 됨
