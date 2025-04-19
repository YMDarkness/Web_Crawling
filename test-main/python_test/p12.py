import math

distance=float(input("input meter : "))
speed=float(input("input speed : "))
angle_d=float(input("input angle : "))

tolerance=2

angle_r=math.radians(angle_d)
reach=2*speed**2*math.sin(angle_r)*math.cos(angle_r)/9.8

if reach>distance-tolerance and reach < distance + tolerance:
    print("nice")
elif reach < distance - tolerance:
    print("false")
else:
    print("erorr")

###################################################################
import math

distance=float(input("input meter : "))
speed=float(input("input speed : "))

tolerance=2

for angle_d in range(0,91):
    angle_r=math.radians(angle_d)

angle_r=math.radians(angle_d)
reach=2*speed**2*math.sin(angle_r)*math.cos(angle_r)/9.8

if reach>distance-tolerance and reach < distance + tolerance:
    print("nice")
elif reach < distance - tolerance:
    print("false")
else:
    print("erorr")
