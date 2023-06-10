# TODO
from cs50 import get_int

while True:
    n = get_int("Height: ")

    # C++ : while (n < 1 || n > 8);
    if n in range(1, 9):
        break

# C++ : for (int i = 0; i < n; i++)
for i in range(0, n, 1):
    for j in range(0, n, 1):
        if (i + j < n - 1):
            print(" ", end="")

        else:
            print("#", end="")

    print()

