#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

typedef uint8_t BYTE;

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./volume input.wav output.wav.\n");
        return 1;
    }

    // Open input file for reading
    // TODO #2
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, inptr);

    // Use check_format to ensure WAV format
    // TODO #4
    if (check_format(header) == 0)
    {
        printf("Not a Wave File.\n");
        return 1;
    }

    if (header.audioFormat != 1)
    {
        printf("Not a Wave File.\n");
        return 1;
    }

    // Open output file for writing
    // TODO #5
    FILE *outptr = fopen(argv[2], "w");
    if (outptr == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&header, sizeof(WAVHEADER), 1, outptr);


    // Use get_block_size to calculate size of block
    // TODO #7
    int size = get_block_size(header);

    // Write reversed audio to file
    // TODO #8
    (fseek(inptr, size, SEEK_END));

    BYTE buffer[size];
    while (ftell(inptr) - size > sizeof(header))
    {
        fseek(inptr, - 2 * size, SEEK_CUR);
        fread(buffer, size, 1, inptr);
        fwrite(buffer, size, 1, outptr);
    }

    fclose(inptr);
    fclose(outptr);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 1;
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    int size = header.numChannels * header.bitsPerSample / 8;

    return size;
}