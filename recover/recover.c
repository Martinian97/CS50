#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    
    //create buffer
    unsigned char buffer[512];
    
    //to count the filename
    int c=0; 
    
    //to check if we have found a JPEG or not
    int jpeg_found=0; 
    
    FILE *img=NULL;
    
    //read until there are no blocks left in file
    while(fread(buffer , 512 , 1 , inptr) == 1)
    {
        //check the first four bytes of buffer to check if JPEG as designed
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(jpeg_found == 1)
            {
                //new image found so we close the current one
                fclose(img);
            }
            
            else
            {
                //increment jpg to next
                jpeg_found++;
            }
            
            //making a new JPEG 
            char filename[8];
            sprintf(filename , "%03i.jpg" , c);
            img = fopen(filename , "w");
            c++;
        }
        
        if (jpeg_found == 1)
        {
            // write 512 bytes to file once we start finding JPEG's
            fwrite(&buffer, 512 , 1, img);
        }
    }
    
    //close the input file
    fclose(inptr);
    
    //close the image
    fclose(img);

    return 0;
}