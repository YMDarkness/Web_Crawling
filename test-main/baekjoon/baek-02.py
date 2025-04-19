##조건문

##백준 1330
## a, b = map(int, input("a,b 두 수 비교 : ").split())
## if a > b:
##     print("a > b")
## elif a < b:
##     print("a < b")
## else:
##     print("a == b")
    

##백준 9498
## a = int(input("시험 점수 : "))
## if 100 >= a >= 90:
##     print("A")
## elif 89 >= a >= 80:
##     print("B")
## elif 79 >= a >= 70:
##     print("C")
## elif 69 >= a >= 60:
##     print("D")
## else:
##     print("F")    


##백준 2753
## a = int(input("윤년 구하기 : "))
## if (a % 4 == 0 and a % 100 != 0) or a % 400 == 0:
##     print(1)
## else:
##     print(0)


##백준 14681
## a = int(input("x 좌표 : "))
## b = int(input("y 좌표 : "))
## if a > 0 and b > 0:
##     print("1 사분면")
## elif a > 0 and b < 0:
##     print("4 사분면")
## elif a < 0 and b > 0:
##     print("2 사분면")
## else:
##     print("3 사분면")
    
    
##백준 2884
## a, b = map(int, input("알람 설정 시간 분 입력 : ").split())
## if b >= 45:
##     print(a,"시", b - 45,"분")
## elif a > 0 and b < 45:
##     print(a - 1,"시",  b + 15,"분")
## else:
##     print(23,"시",  b + 15,"분")


##백준 2525
## a, b = map(int, input("오븐 시간(시 분) : ").split())
## c = int(input("타이머 : "))
## a += c // 60
## b += c % 60
## if b >= 60:
##     a += 1
##     b -= 60
## if a >= 24:
##     a -= 24
## print(a,"시",b,"분")


##백준 2480
## a, b, c = map(int, input("세 주사위 눈 : ").split())
## if a == b == c:
##     print(10000 + a * 1000)
## elif a == b:
##     print(1000 + a * 100)
## elif a == c:
##     print(1000 + a * 100)        
## else:
##     print(max(a, b, c) * 100)