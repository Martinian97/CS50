/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    int low=0, mid, high=n-1;
    while(low <= high)
    {
        mid = (low + high) / 2;
        if (value < values[mid])
            high = mid - 1;
        else if (value > values[mid])
            low = mid + 1;
        else
            return true;
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int temp;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<n-i-1;j++)
        {
            if(values[j]>values[j+1])
            {
                temp=values[j];
                values[j]=values[j+1];
                values[j+1]=temp;
            }
        }
    }
    return;
}
