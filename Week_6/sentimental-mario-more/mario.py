# TODO

from cs50 import get_int

while True:
    n = get_int("Height: ")

    if n in range(1, 9):
        break

for i in range(0, n, 1):
    for j in range(0, n + i + 3, 1):
        if (i + j < n - 1 or j == n or j == n + 1):
            print(" ", end="")

        else:
            print("#", end="")

    print()