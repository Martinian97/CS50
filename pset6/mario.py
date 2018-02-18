import cs50

print("Height: " , end="")
n = cs50.get_int()

while n<0 or n>23:
    print("Height: " , end="")
    n = cs50.get_int()

for i in range(n):
    for j in range(n-1-i):
        print(" " , end="")
    for k in range(1+i):
        print("#" , end="")
    print(" " , end="")
    for k in range(1+i):
        print("#" , end="")
    print()    
        