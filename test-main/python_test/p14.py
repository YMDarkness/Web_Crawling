import time

start=time.perf_counter()

count=0
for i in range(1000000):
    count +=1

end=time.perf_counter()
print(end-start)

###############################

import time

print("로딩 중")
for i in range(10):
    print("[", i*"*" ,(10-i)*" " ,"]" ,i*10 ,"% 완료")
    time.sleep(0.5)

#########################################################

import random
import time

count=0
start=time.perf_counter()

for i in range(1000000):
    count += 1
    random.random()

end=time.perf_counter()
print(end-start)
