def fibo(a):
    if(a==0 or a==1):
        return 1
    return fibo(a-1) +fibo(a-2)

n = int(input())

print(fibo(n))