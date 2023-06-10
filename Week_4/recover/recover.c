#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Sets 2 arguments
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE.\n");
        return 1;
    }

    //Open input file (forensic image)
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 2;
    }

    //output file sets to NULL by default
    FILE *outptr = NULL;

    //array of 512 elements to store 512 bytes
    BYTE buffer[512];

    //stores filename
    char filename[8];

    //count amount of jpeg files found
    int jpeg = 0;

    //read memory until end of file
    while (fread(buffer, sizeof(BYTE) * 512, 1, inptr) == 1)
    {
        //finding jpeg file, if jpeg memory is met
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //close outptr if jpeg was found before and written into ###.jpg
            if (outptr != NULL)
            {
                fclose(outptr);
            }
            //create a file starting with 001.jpg and ++
            sprintf(filename, "%03i.jpg", jpeg);
            //opens file for writing the new found jpeg
            outptr = fopen(filename, "w");
            jpeg++;
        }

        //keeps writting to jpeg file if new jpeg is not found
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, outptr);
        }
    }

    fclose(outptr);
    fclose(inptr);



}