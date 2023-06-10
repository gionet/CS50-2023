#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner.
    //if score 1 > score 2 - player 1 wins
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    //if score 2 > score 1 = player 2 wins
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        // if same score for both players, then print tie
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int score = 0;
    //initial i is 0, counts length of the string using loop)
    for (int i = 0; i < strlen(word); i++)
    {
        //isupper function checks whether C is uppercase letter 'A' to 'Z'. It checks whether the ASCII value is between 65 - 90.
        if (isupper(word[i]))
        {
            //if uppercase, stores the points in into score, and sums up all the points assigned to each respective character, minus ASCII value 65.
            score = score + POINTS[(word[i]) - 65];
        }
        //islower function checks wehther C is lowercase letter 'a' to 'z'. It checks whether the ASCII value is between 97 - 122.
        if (islower(word[i]))
        {
            //if lowercase, sums up all points assigned to each character, minus the ASCII value 97.
            score = score + POINTS [(word[i]) - 97];
        }
    }
    return score;
}

