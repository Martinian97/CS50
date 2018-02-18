import cs50
import math

print("Number: " , end="")
n = cs50.get_int()
num=num1=num2=n
sum=0
count=0

#to count the number of digits
while num2>0:
    count=count+1
    num2=int(num2/10)

#to multiply every second number with 2 starting from second last and add the digits
while n>0:
    c = int((n%100)/10)
    if (c*2)>9:
        sum = sum + int(c/5) + (c*2)%10
    else:
        sum = sum + c*2
    n=int(n/100)
    
#to add the remaining numbers    
while num>0:
    c=num%10
    sum = sum + c
    num=int(num/100)
    
if sum%10==0:
    if count==15:
        #check the first two digits of number
        check = int(num1/(math.pow(10,13)))
        if  check==34 or check==37:
            print("AMEX")
            exit(0)
    if count==16:
        #check the first two digits of number
        check = int(num1/(math.pow(10,14)))
        #check the first digit of number
        check1 = int(num1/(math.pow(10,15)))
        if  check==51 or check==52 or check==53 or check==54 or check==55:
            print("MASTER CARD")
            exit(0)
        if check1==4:
            print("VISA")
            exit(0)
    if count==13:
        #check the first digit of number
        check = int(num1/(math.pow(10,12)))
        if check==4:
            print("VISA")
            exit(0)

print("INVALID")
exit(1)