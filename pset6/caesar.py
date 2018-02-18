import sys
import cs50
import math

#ensure proper usage
if len(sys.argv)!=2:
    print("Usage: ./caesar k")
    exit(1)
    
count=1
k=0
n=len(sys.argv[1])
for j in range(n):
    #coversion of the string into an integer
    k = k + (ord(sys.argv[1][j]) - 48)*math.pow(10,n-count)
    count=count+1
    
print("plaintext: " , end="") 
#get string from user
s=cs50.get_string()
print("ciphertext: " , end="")    

for i in range(len(s)):
    #if it is an alphabet
    if s[i].isalpha():
        #cipher the character according to the key value
        c = (ord(s[i]) + (k%26))
        if s[i].isupper():
            #so that if value runs out of Z, it circles back to A
            while c<65 or c>90:
                c = c-26
        else:
            #similarly for smaller case
            while c<97 or c>122:
                c = c-26
        print(chr(int(c)) , end="")
    else:
        #if not an alphabet
        print(s[i] , end="")
        
print()
exit(0)