# TODO
import sys
# from cs50 import get_int

while True:
    card = input("Number: ")
    card_length = len(card)
    if card_length < 13 or card_length > 16:
        print("INVALID")
    elif card != card.isdigit():
        print("Only accept numbers")
        sys.exit(0)
    else:
        break

# Obtained from Youtuber: "CS50 Guide by Anvea" Channel
def luhn_algo(card):
    def digits(n):
        return [int(d) for d in str(n)]
    digits = digits(card)
    odd = digits[-1::-2]
    even = digits[-2::-2]
    checksum = 0

    checksum += sum(odd)

    for d in even:
        even_x2 = d * 2
        if even_x2 >= 10:
            checksum += (even_x2 % 10) + (even_x2 // 10)

        else:
            checksum += even_x2

    return checksum % 10


if luhn_algo(card) == 0:

    if card_length == 15 and (card.startswith('34') or card.startswith('37')):
        print("AMEX")
    elif card_length == 16 and card.startswith(('51', '52', '53', '54', '55')):
        print("MASTERCARD")
    elif (card_length == 13 or card_length == 16) and card.startswith('4'):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")