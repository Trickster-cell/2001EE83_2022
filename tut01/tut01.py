import math
a = int(input("Enter the number: "))
ans = 1
x = a
while(x!=0):
    ans = ans*x
    x = x-1
print("The factorial of" ,a, "is:")
print(ans)
