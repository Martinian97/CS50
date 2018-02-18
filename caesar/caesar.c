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
        printf("Usage: ./caesar k\n");
        return 1;
    }
    int count=1,k=0,c;
    for(int j=0 , n=strlen(argv[1]) ; j<n ; j++)
    {
        //coversion of the string into an integer
        k=k+((int)argv[1][j] - 48)*pow(10,n-count);
        count++;
    }    
    printf("plaintext: ");
    //get string from user
    string s = get_string();
    printf("ciphertext: ");
    for(int i=0 , n=strlen(s); i<n; i++)
    {
        //if it is an alphabet
        if(isalpha(s[i]))
        {
            //cipher the character according to the key value
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
                //similarly for smaller case
                while(c<97 || c>122)
                {
                    c=c-26;
                }    
            }
            printf("%c" , (char)c);
        }
        //if not an alphabet, leave it as it is
        else
            printf("%c" , s[i]);
    }
    printf("\n");
    return 0;
}