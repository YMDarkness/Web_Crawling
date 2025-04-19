##입출력과 사칙연산

##백준 2557 
## print("Hello world!") 


##백준 사칙연산
## a = int(input("input number a : ")) 
## b = int(input("input number b : "))
##백준 1000 sum = a + b 
##백준 1001 min = a - b 
##백준 10998 mul = a * b 
##백준 1008 div = a / b 
##백준 10869 rem = a % b 
## print(sum) 
## print(min)
## print(mul)
## print(div)
## print(rem)


##백준 10926
## s = input("ID : ")
## print(s + "??!") 


##백준 18108
## a = int(input("불기년도 : "))
## b = a - 543
## print("서기", b, "년")


##백준 3003
## chess = [1, 1, 2, 2, 2, 8]
## a = list(map(int, input("현재 체스 말 수 (킹 퀸 룩 비숍 나이트 폰): ").split()))
## print("부족한 체스 말 : ")
## for i in range(6):
##     print(chess[i] - a[i], end = " ")


##백준 10430
## a = 5
## b = 8
## c = 4
## a = int(input("input number : "))
## b = int(input("input number : "))   # a,b,c = input().split() a = int(a), b = int(b), c = int(c)  or  a,b,c = map(int, input().split()) 
## c = int(input("input number : "))
## print((a+b)%c)
## print(((a%c)+(b%c))%c)
## print((a*b)%c)
## print(((a%c)*(b%c))%c)


##백준 2588
##문자열 이용, 반복문 x
## a = int(input("세자리 수 곱 : "))
## b = input("세자리 수 곱 : ") #문자열 b를 구성하는 각각의 문자에 접근할 수 있다
## print(a*int(b[2])) => 일
## print(a*int(b[1])) => 십
## print(a*int(b[0])) => 백
## print(a*int(b))

##문자열 이용, 반복문 o
## for i in range(3,0,-1):   # for i in range(2,-1,-1):
##     print(a*int(b[i-1]))  #     print(a*int(b[i]))
## print(a*int(b))

##산술연산자
## a = int(input("세자리 수 곱 : "))
## b = int(input("세자리 수 곱 : "))
## print(a*(b % 10)) # b를 10으로 나눈 나머지 값
## print(a*(b % 100 // 10)) # b를 100으로 나눈 나머지 값에 다시 10으로 나눈 몫
## print(a*(b // 100)) # b를 100으로 나눈 몫
## print(a*b)


##백준 10171
## print("\\   /\\")
## print(" )  ( ')")
## print("(  /   )")
## print(" \\(__)|")
## tip!  print() 안에 \를 나타낼 때 위에처럼 두번 써야 인식이 된다


##백준 10172
## print("|\_/|")
## print("|q p|   /}")
## print("( 0 )\"\"\"\\") => \"
## print("|\"^\"'    |")
## print("||_/=\\\__|")
## tip! ""를 나타내기 위해 앞에 \를 사용


##백준 25083
## print("         ,r'\"7")
## print("r`-_   ,'  ,/")
## print(" \\. \". L_r'")
## print("   `~\\/")
## print("      |")
## print("      |")