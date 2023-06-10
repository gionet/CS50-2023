#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    //only take 2 argument counts
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 0;
    }

    //Loop through 2nd argument, making sure all character is digit
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        //if 2nd argument is not digit, print usage instruction
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: /caesar key\n");
            return 1;
        }
    }

    //Get input from user - plaintext
    string plaintext = get_string("plaintext:  ");
    //Print ciphertext
    printf("Ciphertext: ");

    //convert string into int with "atoi"
    int k = atoi(argv[1]);

    //Loop function to go through every character
    for (int j = 0; j < strlen(plaintext); j++)
    {
        //if uppercase character, print uppercase + key (character movement)
        if (isupper(plaintext[j]))
        {
            printf("%c", (plaintext[j] - 65 + k) % 26 + 65);
        }
        //if uppercase character, print lowercase + key (character movement)
        else if (islower(plaintext[j]))
        {
            printf("%c", (plaintext[j] - 97 + k) % 26 + 97);
        }

        //if not character, print plaintext (no character movement)
        else
        {
            printf("%c", plaintext[j]);
        }
    }
    printf("\n");

}

