# TODO
from cs50 import get_string

text = get_string("Text: ")

# Letter counts
letters = 0

# Sentence counts
sentences = 0

# Words = 1 because including last word that does not have *whitespace*
words = 1

for i in text:
    if i.isalpha():
        letters += 1
    elif i == " ":
        words += 1
    elif i == "." or i == "!" or i == "?":
        sentences += 1
    else:
        continue

L = (letters / words) * 100
S = (sentences / words) * 100

index = 0.0588 * L - 0.296 * S - 15.8
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
