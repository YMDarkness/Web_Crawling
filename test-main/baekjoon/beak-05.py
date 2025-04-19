##함수

##백준 15596
## sum 이용
## def solver(a):
##     return sum(a)

## for문 이용
## def solver(a):
##     total = 0
##     for i in a:
##         total += 1
##     return total0


##백준 4673
##list에서 사용
num = list(range(1, 10_001))
remove_list = [] #이후에 삭제할 숫자 리스트
for n in num:
    for i in str(n):
        n += int(i) #생성자가 있는 수
    if n <= 10_000: #10,000보다 작거나 같을때만
        remove_list.append(n) #append > 리스트에 요소를 추가할 때
for remove_num in set(remove_list): #set으로 중복값 제거
    num.remove(remove_num)
for self_num in num: #생성자가 있는 수를 삭제한 리스트
    print(self_num)

##set에서 사용    
num = set(range(1, 10000))
remove_set = set() #생성자가 있는 수 set
for n in num:
    for i in str(n):
        n += int(i)
    remove_set.add(n) #add : 집합에 요소 추가할 때
self_num = num - remove_set #set의 '-' 연산자로 차집합 구함
for self_n in sorted(self_num): #sorted 함수로 정렬
    print(self_n)


##백준 1065
##def 함수 사용
def hansu(num):
    hansu_cnt = 0
    for i in range(1, num + 1):
        num_list = list(map(int, str(i)))
        if i < 100:
            hansu_cnt += 1 #100보다 작으면 모두 한수
        elif num_list[0] - num_list[1] == num_list[1] - num_list[2]:
            hansu_cnt += 1 #x의 각 자리가 등차수열이면 함수
    return hansu_cnt
num = int(input())
print(hansu(num))

##함수 사용 안함
num = int(input())
hansu = 0
for i in range(1, num + 1):
    num_list = list(map(int, str(i)))
    if i < 100:
        hansu += 1 #100보다 작으면 모두 한수 
    elif num_list[0] - num_list[1] == num_list[1] - num_list[2]:
        hansu += 1 #x의 각 자리가 등차수열이면 함수
print(hansu)