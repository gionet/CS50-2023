#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool validity(string key);
string encipher(string input, string index);

int main(int argc, string argv[])
{
    //only takes 2 command-line argument
    if (argc != 2)
    {
        printf("./substitution key\n");
        return 1;
    }

    //Function to test key validity
    if (!validity(argv[1]))
    {
        return 1;
    }
    //Gets input from user
    string input = get_string("Plaintext: ");

    //key = second command-line argument
    string key = argv[1];

    //printf("Ciphertext: ");
    {
        string output = encipher(input, key);
    }
}

//Checks validity of key(second command-line argument)
bool validity(string key)
{
    //if key is not = 26, do not proceed
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }
    //1st for loop to make sure that all key are alphabet
    for (int i = 0; i < strlen(key); i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabatic characters\n");
            return false;
        }
        //2nd for loop to check for alphabet duplications in key
        for (int j = i + 1; j < strlen(key); j++)
        {
            if (key[j] == key[i])
            {
                printf("Key must not contain repeated characters.\n");
                return false;
            }
        }
    }
    return true;
}

string encipher(string input, string key)
{
    int length = strlen(input);
    int index;
    char ciphertext[length + 1];

    //Loop to prioritise plaintext's uppercase/lowercase
    for (int i = 0; i < strlen(input); i++)
    {
        if (isupper(input[i]))
        {
            //printf("%c\n",(key[input[i] - 65]));
            index = ((input[i]) - 65);
            ciphertext[i] = key[index];
            if (islower(ciphertext[i]))
            {
                ciphertext[i] -= 32;
            }
        }
        else if (islower(input[i]))
        {
            //printf("%c", tolower(key[input[i] - 97]));
            index = ((input[i]) - 97);
            ciphertext[i] = key[index];
            if (isupper(ciphertext[i]))
            {
                ciphertext[i] += 32;
            }
        }
        else
        {
            //printf("%c", input[i]);
            ciphertext[i] = input[i];
        }
    }
    //print nul = ciphertext has come to an end
    ciphertext[length] = '\0';

    printf("ciphertext: %s\n", ciphertext);

    return 0;
}