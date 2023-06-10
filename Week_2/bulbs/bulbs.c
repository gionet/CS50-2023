#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Get input from user
    string input = get_string("Message: ");

    //To go through each character from left to right
    for (int i = 0; i < strlen(input); i++)
    {
        //Identify the ASCII value of the character
        int decimal = input[i];

        //Stores binary value into array BITS_IN_BYTE, 8 values
        int binary[BITS_IN_BYTE];

        //Loop to store binary value into array
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            //Stores into Array BITS_IN_BYTES, remainder 2
            binary[j] = decimal % 2;

            //Divides ASCII by 2
            decimal = decimal / 2;
        }

        //To reverse the array in BITS_IN_BYTE to get true binary value (BITS_IN_BYTES -1 to get 8 value.)
        for (int k = BITS_IN_BYTE - 1; k >= 0; k--)
        {
            //Print black emoji if bit 0 and print yellow emoji if bit is 1 from Array.
            print_bulb(binary[k]);
        }

        printf("\n");

    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
