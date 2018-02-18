#include<stdio.h>
#include<cs50.h>
#include <math.h>

int calculate(int f , int q , int c)
{
    while(f%q != 0)
    {
        if(f/q >=1)
        {
            c = c + f/q;
            f = f%q;
            if(f>=10)   return calculate(f , 10 ,c);
            else if(f>=5)   return calculate(f , 5 ,c);
            else return calculate(f , 1 ,c);
        }
        else
        {
            if(f>=10)   return calculate(f , 10 ,c);
            else if(f>=5)   return calculate(f , 5 ,c);
            else return calculate(f , 1 ,c);
        }
    }
    c = c + f/q;
    return c;
}

int main(void)
{
    printf("O hai! How much change is owed?\n");
    float n = get_float();
    while(n<0)
    {
        printf("O hai! How much change is owed?\n");
        n = get_float();
    }
    int cents = floor(n);
    int coins = cents/0.25;
    float fraction = (n - cents)*100;
    float check = (int)((n - cents)*100) + 0.5;
    if(check<fraction)  coins = calculate(ceil(fraction) , 25 , coins);
    else coins = calculate(floor(fraction) , 25 , coins);
    printf("%i\n" , coins);
}