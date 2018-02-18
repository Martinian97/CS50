/**
 * Implements a dictionary's functionality with a TRIE data structure.
 */

#include <stdbool.h>
#include <string.h>
#include "dictionary.h"
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    bool is_word;
    struct node *children[27];
}
node;

//root for the start of a word set to NULL initially
node root = {false , {NULL}};
//to keep the dictionary count
int count = 0;

/**
* Calculates a number for a character.
*/

int char_to_number(char c)
{
    if (c == '\'')
        return 26;
    
    if(c >= 'A' && c <= 'Z')
        c += 32;
    
    return (int)(c-'a');
}

/**
 * Returns true if word is in dictionary else false.
 */
 
bool check(const char *word)
{
    node *ptr = &root;
    for(int i=0;i<strlen(word);i++)
    {
        //if node doesn't exist means there is no word
        if(ptr->children[char_to_number(word[i])] == NULL)
            return false;
        ptr = ptr->children[char_to_number(word[i])];
    }
    //after reaching the last node, check if it is actually end of a word
    if(ptr->is_word)
        return true;
    else
        return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */

bool load(const char *dictionary)
{
    FILE *inp = fopen(dictionary , "r");
    if(inp == NULL)
        return false;
    
    while(!feof(inp))
    {
        char word[LENGTH+1] = {};
        fscanf(inp , "%s\n" , word);
        count++;
        node *ptr = &root;
        
        for(int i=0;i<strlen(word);i++)
        {
            //if node is NULL then malloc a new node
            if(ptr->children[char_to_number(word[i])] == NULL)
            {
                node *new = malloc(sizeof(node));
                //initialise to NULL
                *new = (node) {false , {NULL}};
                ptr->children[char_to_number(word[i])] = new;
                ptr = new;
            }
    
            else
            {
                //just point to th next node
                ptr = ptr->children[char_to_number(word[i])];
            }
        }
    
        //after last node, set "is_word" to true.
        ptr->is_word = true;
    }
    
    //close file
    fclose(inp);
    
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */

unsigned int size(void)
{
    return count;
}

/**
 * Recursive function to free a node
 */
 
void Free(node *node)
{
    for(int i=0;i<27;i++)
    {
        //reach the last node, as we have to free from bottom to top
        if(node->children[i] != NULL)
            Free(node->children[i]);
    }
    
    free(node);
    return;
}


/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */

bool unload(void)
{
    for(int i=0;i<27;i++)
    {
        //if children exists, then free them
        if(root.children[i] != NULL)
            Free(root.children[i]);
    }
    return true;
}