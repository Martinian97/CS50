#include<stdio.h>
#include<cs50.h>

int main(void)
{
    printf("Height: ");
    int n = get_int();
    while(n<0 || n>23)
    {
        printf("Height: ");
        n = get_int();
    }
    
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n-1-i;j++)
        {
            printf(" ");
        }
        for(int k=0;k<1+i;k++)
        {
            printf("#");
        }
        printf("  ");
        for(int k=0;k<1+i;k++)
        {
            printf("#");
        }
        printf("\n");
    }
}