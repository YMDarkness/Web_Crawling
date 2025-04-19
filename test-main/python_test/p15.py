import time 
import random

def roll_dice():
    r = str(random.randint(1,6))
    dice=" _ \n|"+r+"|\n _"

    print(dice)
    return r

start=time.perf_counter()

p="r"
while p=="r":
    print("유저가 주사위를 던진다")
    userroll=roll_dice()
    print("컴퓨터가 주사위를 던진다")
    comroll=roll_dice()
    time.sleep(2)

    if userroll > comroll:
        print("플레이어 승리")
    elif userroll == comroll:
        print("비김")
    else:
        print("플레이어 패배")
    
    p=input("계속 하기 =  r, 종료하려면 아무키나 누르시오")
end=time.perf_counter()
print("총",end-start,"초 동안 플레이")
