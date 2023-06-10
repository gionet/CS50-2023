import csv
import sys


def main():

    # TODO: Check for command-line usage
    if (len(sys.argv) != 3):
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    csv_file = open(f"{sys.argv[1]}", "r")
    reader = csv.DictReader(csv_file)

    database = []
    for row in reader:
        database.append(row)

    # TODO: Read DNA sequence file into a variable
    sequence_file = open(f"{sys.argv[2]}", "r")
    dna_sequence = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence

    # "TypeError: 'dict_keys' object is not subscriptable" occurs when we try to access a dict_keys object at a specific index
    # it is not possible to iterate over an integer or set of numbers
    subsequences = list(database[0].keys())[1:]

    results = {}
    # List down STR's in rows
    for subsequence in subsequences:
        results[subsequence] = longest_match(dna_sequence, subsequence)

    # TODO: Check database for matching profiles

    for person in database:
        match = 0
        print(person)
        for subsequence in subsequences:
            print(subsequence)
            if int(person[subsequence]) == results[subsequence]:
                match += 1

        if match == len(subsequences):
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
