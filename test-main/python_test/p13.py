import random

people=['현석','도남','일민','혜원','성원','정원']

print(random.choice(people))
print(random.sample(people,3))

#################################################################

import random

choice=input("가위 바위 보 게임 : ")
r=random.random()
if r < 1/3:
    print("컴퓨터는 바위")
    if choice=="보":
        print("you winner")
    elif choice=="가위":
        print("you lose")
    else:
        print("비김")

elif 1/3 <= r < 2/3:
    print("컴퓨터는 보")
    if choice=="보":
        print("비김")
    elif choice=="가위":
        print("you winner")
    else:
        print("you lose")

else:
    print("컴퓨터는 가위")
    if choice=="보":
        print("you lose")
    elif choice=="가위":
        print("비김")
    else:
        print("you winner")

####################################################

import random

h=0
t=0

for i in range(100):
    r=random.random()
    if r < 0.5:
        h+=1
    else:
        t+=1

print("앞",h)
print("뒤",t)

############################

import random

coin=input("코인 앞면과 뒷면 : ")

r=random.random()

if r < 1/2:
    print("컴퓨터는 앞")
    if coin == "앞":
        print("같다")
    else:
        print("다르다")
else:
    print("컴퓨터는 뒤")
    if coin == "뒤":
        print("같다")
    else:
        print("다르다")
