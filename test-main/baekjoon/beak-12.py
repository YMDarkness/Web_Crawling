##시간 복잡도

##백준 24262
# MenOfPassion(A[], n) {
#    i = ⌊n / 2⌋;
#    return A[i]; # 코드1
# }
# n을 입력받아서 2로 나누고 버림 했을 때 나오는 정수를 Index로 한다. 이를 A[]라는 배열의 Indexing 값을 구하고 이를 Return하라
print(1)
print(0)


##백준 24263
# MenOfPassion(A[], n) {
#    sum <- 0;
#    for i <- 1 to n
#        sum <- sum + A[i]; # 코드1 for 문을 돌면서 리스트의 합을 구함, 실행 횟수는 n을 입력 받아 print한다.
#    return sum;
# }
# 수행 횟수를 다항식으로 나타나면 '선형' 복잡도이므로 1차식입니다. 따라서 1을 print 해줍니다.
n = int(input())
print(n)
print(1)


##백준 24264
# MenOfPassion(A[], n) {
#    sum <- 0;
#    for i <- 1 to n
#        for j <- 1 to n
#            sum <- sum + A[i] × A[j]; # 코드1
#    return sum;
# }
# Big-O 표기법으로는 2차 복잡도를 지닌 문제, 입력 n의 크기에 따라 n의 제곱 형태로 코드 #1이 실행되기 때문, 실행 횟수는 입력받은 n을 제곱하여 출력, 차수는 2를 출력하면 되는 문제
n = int(input())
print(n**2)
print(2)


##백준 24265
