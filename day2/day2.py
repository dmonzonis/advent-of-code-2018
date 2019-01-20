from collections import Counter
from itertools import combinations


def checksum(wordlist):
    two_times = three_times = 0
    for word in wordlist:
        repetitions = Counter(word).values()
        two_times += 2 in repetitions
        three_times += 3 in repetitions
    return two_times * three_times


def get_match(first, second):
    """Return the matching characters if strings differ by only 1 char, or False otherwise."""
    match = ""
    fails = 0
    # Assume len(first) == len(second)
    for i in range(len(first)):
        if first[i] == second[i]:
            match += first[i]
        else:
            fails += 1

        # If the IDs have more than 1 different character, it's not a match
        if fails > 1:
            return False
    return match


def find_match(wordlist):
    pairs = combinations(wordlist, 2)
    for pair in pairs:
        match = get_match(pair[0], pair[1])
        if match:
            return match


def main():
    with open("input") as f:
        wordlist = f.read().splitlines()

    # Part 1
    print(checksum(wordlist))

    # Part 2
    print(find_match(wordlist))


if __name__ == "__main__":
    main()
