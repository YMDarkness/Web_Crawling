##반복문

##백준 2739
## a = int(input("구구단 : "))
## for i in range(1,10,1):
##     print(a,"*",i,"=",a * i)
    
    
##백준 10950
## a = int(input("저장할 갯수 입력 : "))
## for i in range(a):
##     x, y = map(int, input().split())
##     print(x + y)


##백준 8393
## a = int(input("n : "))
## s = 0
## for i in range(a + 1):
##     s = s + i
## print("1 부터",a,"까지의 합 :",s)    


##백준 25304
## a = int(input("금액 : "))
## b = int(input("물건 수 : "))
## s = 0
## for i in range(b):
##     x, y = map(int, input().split())
##     s += x * y
## if s == a:
##     print("yes")
## else:
##     print("no")


##백준 15552
## import sys
## a = int(sys.stdin.readline())
## for i in range(a):
##     x, y = map(int, sys.stdin.readline().split())
##     print(x + y)
    
    
##백준 11021
## a = int(input("저장할 갯수 입력 : "))
## for i in range(a):
##     x, y = map(int, input().split())
##     print(f"Case #{i + 1} : {x + y}") #문자열 포매팅 중요 print("Case #",i + 1,":",x + y) => Case # 1 : n으로 나옴...
    
    
##백준  11022
## a = int(input("저장할 갯수 입력 : "))
## for i in range(a):
##     x, y = map(int, input().split())
##     print(f"Case #{i + 1} : {x} + {y} = {x + y}")
  
  
##백준 2438
## a = int(input())
## for i in range(1, a + 1):
##     print("*" * i)
    
    
##백준 2439
## a = int(input())
## for i in range(1, a + 1):
##     print(" " * (a - i), "*" * i)


##백준 10952
## while True:
##     a, b = map(int, input().split())
##     if a == 0 and b == 0:
##         break
##     print(a + b)
## 11021, 11022의 경우 입력값 갯수를 받아 for문을 돌리지만 10952은 무한 루프를 탄다는 차이가 있다


##백준 10951
## while True:
##     try:
##         a, b = map(int, input().split())
##         print(a + b)
##     except:
##         break
    
    
##백준 1110
## a = int(input("int input : "))
## num = a
## cin = 0
## while True:
##     x = num // 10
##     y = num % 10
##     z = (x + y) % 10
##     num = (y * 10) + z
##     cin += 1
##     if (num == a):
##         break 
## print(cin)    