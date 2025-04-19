##1차원 배열

##백준 10807
## a = int(input("정수의 개수 : ")) ##정수 개수
## b = list(map(int, input("정수 입력(정수 사이 공백 처리) : ").split())) #리스트에 정수 입력
## c = int(input("찾으려는 정수 : ")) ##찾으려는 정수
## print(b.count(c))


##백준 10871
## a, b = map(int, input("정수 a개로 이루어진 수열과 찾으려는 정수 b 입력 : ").split())
## c = list(map(int, input("정수 입력(정수 사이 공백 처리) : ").split()))
## for i in range(a):
##     if c[i] < b:
##         print(c[i], end=" ")


##백준 10818
## a = int(input())
## b = list(map(int, input().split()))
## print(min(b), max(b))


##백준 2562
## a = [int(input()) for _ in range(9)]
## print("최댓값", max(a))
## print("위치", a.index(max(a)) + 1)


##백준 5597
## a = [i for i in range(1, 31)]
## for _ in  range(28):
##     b = int(input())
##     a.remove(b)
## print("과제 미제출 인원", min(a), max(a))


##백준 3052
## a = []
## for i in range(10):
##     b = int(input())
##     a.append(b % 42)
## a = set(a)
## print(len(a))


##백준 1546
## a = int(input())
## b = list(map(int, input().split()))
## max_s = max(b)
## list = []
## for sco in b:
##     list.append(sco/max_s*100)
## avg = sum(list)/a
## print(avg)


##백준 8958
## a = int(input())
## for _ in range(a):
##     li = list(input())
##     sc = 0
##     sum_sc = 0
##     for i in li:
##         if i == 'o':
##             sc += 1
##             sum_sc += sc
##         else:
##             sc = 0
##     print(sum_sc)


##백준 4344
## a = int(input())
## for _ in range(a):
##     li = list(map(int, input().split()))
##     avg = sum(li[1:])/li[0]
##     b = 0
##     for s in li[1:]:
##         if s > avg:
##             b += 1
##     rate = b/li[0]*100
##     print(f'{rate: .3f}%')