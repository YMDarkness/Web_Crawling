F=75
C=(F - 32) /1.8
c1=int((F - 32) /1.8)
print('섭씨',C)
print('섭씨(정수)',c1)

a=5
k=5/0.62137
k2=(int(5/0.621370))
m=1000*k
m2=int((1000*k))

print(a,'마일')
print(k,'킬로미터')
print(k2,'킬로미터(정수)')
print(m,'미터')
print(m2,'미터(정수)')

a = 3
b = 4
r = a * b
r2 = (float(a*b))
c = 3.14*a**2
c2 = (int(3.14*a**2))
print(r)
print(r2)
print(c)
print(c2)

time = int(input('time : '))

hour = time /60
hours = int(hour)

min = time % 60

sec = min % 3600

print(hours,'h',min,'m',sec,'s')