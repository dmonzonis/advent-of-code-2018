def apply_changes(change_list):
    result = 0
    for c in change_list:
        result += c
    return result


def find_first_duplicate(change_list):
    seen = {0}
    current = 0
    while True:
        for c in change_list:
            current += c
            if current in seen:
                return current
            seen.add(current)


def main():
    with open("input") as f:
        change_list = [int(c) for c in f.readlines()]

    # Part 1
    print(apply_changes(change_list))

    # Part 2
    print(find_first_duplicate(change_list))


if __name__ == "__main__":
    main()
