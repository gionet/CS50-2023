#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

int count_letters(string text);
int count_word(string text);
int count_sentences(string text);

int main(void)
{
    //Gets an input text from User
    string input = get_string("Text: ");

    //To calculate the average number of *letters per 100 words in the text
    //(float) to untruncate the decimals
    double L = count_letters(input) / (float)count_word(input) * 100;

    //To calculate the average number of *sentences per 100 words in the text
    //(float) to untruncate the decimals
    double S = count_sentences(input) / (float)count_word(input) * 100;

    //readability test - Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", index);
    }
}

//Go through every letter to count the number of letters in the input text
int count_letters(string text)
{
    int text_count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        //Letters count increases 1 for every alphabet identified
        if (isalpha(text[i]))
        {
            text_count++;
        }
    }
    return text_count;
}

//To count the total number of words from input text
int count_word(string text)
{
    int word_count = 1;

    for (int i = 0; i < strlen(text); i++)
    {
        //Word count increases 1 by every "whitespace" identified
        if (text[i] == ' ')
        {
            word_count++;
        }
    }
    return word_count;
}

//To count the total number of sentences from input text
int count_sentences(string text)
{
    int sentences_count = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        //Sentences count increases 1 by every "." , "!" and "?" identified
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences_count++;
        }
    }
    return sentences_count;
}
