def is_reactive(first, second):
    """Return whether the units trigger a reaction with each other."""
    return first.lower() == second.lower() and first != second


def process_polymer(polymer):
    i = 0
    while i < len(polymer) - 1:
        if is_reactive(polymer[i], polymer[i + 1]):
            polymer = polymer[:i] + polymer[i + 2:]
            if i > 0:
                i -= 1
        else:
            i += 1
    return polymer


def best_reduced_polymer(polymer):
    best = polymer
    units = set(polymer.lower())

    for unit in units:
        # Remove unit from the polymer
        reduced_polymer = polymer.replace(unit, '').replace(unit.upper(), '')
        processed = process_polymer(reduced_polymer)
        if len(processed) < len(best):
            best = processed
    
    return best


def main():
    with open("input") as f:
        polymer = f.read().strip('\n')

    # Part 1
    processed = process_polymer(polymer)
    print(len(processed))

    # Part 2
    print(len(best_reduced_polymer(polymer)))


if __name__ == "__main__":
    main()
