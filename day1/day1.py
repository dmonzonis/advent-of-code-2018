def apply_changes(change_list):
    result = 0
    for c in change_list:
        result += c
    return result


def main():
    with open("input") as f:
        change_list = [int(c) for c in f.readlines()]

    print(apply_changes(change_list))


if __name__ == "__main__":
    main()
