##문자열

##백준 11654
print(ord(input())) #아스키코드 반환 함수 ord()
print(chr(100)) #chr()은 ord()의 반대 기능, 아스키코드의 해당하는 수를 입력하면 그에 해당하는 문자열 출력
print(chr(map(int, input())))


##백준 11720
##sum() 사용
a = input()
print(sum(map(int, input())))

##for문 사용
a = input()
b = input()
c = 0
for i in b:
    c += int(i) #c = c + int(i)
print(c)

##for문 사용 2
a = input()
b = input()
c = 0
for i in range(a): #0 ~ a-1까지
    c += int(b[i])
print(c)


##백준 10809
