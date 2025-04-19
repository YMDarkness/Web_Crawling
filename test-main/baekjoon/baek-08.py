##2차원 배열

##백준 2738
## a, b = [], []
## n, m = map(int, input().split())  # 행렬 크기 입력
## for row in range(n):
##     row = list(map(int, input().split()))
##     a.append(row)  # a에 행렬 원소를 입력 받음
## for row in range(n):
##     row = list(map(int, input().split()))
##     b.append(row)  # b에 행렬 원소를 입력 받음
## for row in range(n):
##     for col in range(m):
##         print(a[row][col] + b[row][col], end=" ")  # 반복문을 통해 행렬 A, B 의 동일 행, 동일 열에 위치한 원소를 더한 값을 출력하고, end = ' ' 를 통해 띄어쓰기로 열을 구분하여 출력한다.
##     print()  # 하나의 열을 출력한다음, 다음 행으로 넘어가기 전에 print() 를 통해 줄바꿈을 해주어 행을 구분한다.

# map 함수는 맵 객체(map object)를 반환하므로, row에는 list 형태로 받아주어야 한다.
# 맵 객체는 이터레이터이기 때문에 다대다 관계에서는 list가 생략이 가능하지만, 일대다 관계에서 map 함수는 list 를 통해 값을 확인할 수 있다.


##백준 2566
## table = [list(map(int, input().split())) for _ in range(9)]  # 값 하나씩 탐색하며 최댓값을 찾는다
## max_num = 0
## max_row, max_col = 0, 0
## for row in range(9):
##     for col in range(9):
##         if max_num <= table[row][col]:
##             max_row = row + 1
##             max_col = col + 1
##             max_num = table[row][col]
## print(max_num)
## print(max_row, max_col)


##백준 10798
## words = [input() for i in range(5)]  ##5줄 입력
## for j in range(15):  ##최대 단어 길이 15
##     for i in range(5):
##         if j < len(words[i]):  ##j가 단어 길이보다 작으면 인덱스 범위 안에 있으므로 출력할 수 있다
##             print(words[i][j], end="")  ##위에서 아래로 읽기에 첫번째 단어는 words[0][0], 두번쨰 단어는 words[1][0]....


##백준 2563
import sys

array = [[0 for _ in range(101)] for _ in range(101)]  ##전부 0을 가지는 2차원 배열 선언
n = int(input())
for _ in range(n):  ##n번만큼 위치를 입력받음
    x, y = list(map(int, input().split()))
    for row in range(
        x, x + 10
    ):  ##가로, 세로 크기가 10인 정사각형이고 첫번쨰 자연수는 색종이의 왼쪽 벽과 도화지의 왼쪽 벽 사이의 거리 > 시작점이기 떄문에 시작점 x에서 크기인 10만큼의 범위 지정
        for col in range(y, y + 10):
            array[row][col] = 1  ##0으로 도배된 101 X 101 크기의 도화지에서 색종이를 붙인 위치를 1로 칠함
resutl = 0
for i in array:  ##1을 카운트
    resutl += i.count(1)
print(resutl)
