// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

string replace(string input);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Incorrect Command-Line Argument\n");
        return 1;
    }

    printf("%s\n", replace(argv[1]));
}

string replace(string input)
{
    string output = input;

    for (int i = 0; i < strlen(input); i++)
    {
        char c = (input[i]);

        switch (c)
        {
            case '1':
                output[i] = '6';
                break;

            case 'e':
                output[i] = '3';
                break;

            case 'i':
                output[i] = '1';
                break;

            case 'o':
                output[i] = '0';
                break;

            default:
                output[i] = c;
                break;

        }
        //printf("%c\n", input[i]);

    }
    return output;
}



