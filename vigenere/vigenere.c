#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
#include<math.h>

int main(int argc , string argv[])
{
    //if not two arguments then wrong input
    if(argc!=2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    for(int j=0 , n=strlen(argv[1]) ; j<n ; j++)
    {
        //check if the second argument is not all aalphabets
        if(isalpha(argv[1][j])) continue;
        else 
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
    int k,c,j=0;
    string key=argv[1];
    printf("plaintext: ");
    //get string from user
    string s = get_string();
    printf("ciphertext: ");
    for(int i=0 , n=strlen(s); i<n; i++)
    {
        if(isalpha(s[i]))
        {
            //if j exceeds the length of key then circles back to the start
            if(j>=strlen(key))   
                j=0;
            if(isupper(key[j]))
            {
                //upper case so subtract the ASCII value of 'A'
                k=(int)(key[j]) - 65;
            }
            else
            {
                //lower case so subtract the ASCII value of 'a'
                k=(int)(key[j]) - 97;        
            }
            j++;
            //calculate the value to move ahead
            c=((int)(s[i]) + (k%26));
            
            if(isupper(s[i]))
            {
                //so that if value runs out of Z, it circles back to A
                while(c<65 || c>90)
                {
                    c=c-26;
                }    
            }
            else
            {
                //similarly for lower case
                while(c<97 || c>122)
                {
                    c=c-26;
                }    
            }
            printf("%c" , (char)c);
        }
        //if not an alphabet, print it as it is
        else
            printf("%c" , s[i]);
    }
    printf("\n");
    return 0;
}