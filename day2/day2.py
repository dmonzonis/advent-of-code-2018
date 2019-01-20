from collections import Counter


def checksum(wordlist):
    two_times = three_times = 0
    for word in wordlist:
        repetitions = Counter(word).values()
        two_times += 2 in repetitions
        three_times += 3 in repetitions
    return two_times * three_times


def main():
    with open("input") as f:
        wordlist = f.read().splitlines()
    print(checksum(wordlist))


if __name__ == "__main__":
    main()
