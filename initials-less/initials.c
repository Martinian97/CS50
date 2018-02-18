#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>

int main(void)
{
    //input string from user
    string s = get_string();
    int c=0;
    for(int i=0, n=strlen(s) ; i<=n ; i++)
    {
        //if terminated by space or \0 to check for end of word and string respectively
        if(s[i]==' ' || s[i]=='\0')
        {
            //print the first letter of the word in upper case
            printf("%c" , toupper(s[c]));
            c=i+1;
        }
    }
    printf("\n");
}