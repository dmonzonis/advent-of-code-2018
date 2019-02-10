import copy


def cell_power(x, y, serial):
    """Compute the cell power of the cell at (x, y)."""
    rack_id = x + 10
    result = rack_id * y + serial
    result *= rack_id
    # Get the hundreds digit
    result = str(result)
    if len(result) < 3:
        result = -5
    else:
        result = int(result[-3]) - 5
    return result


def total_power_square(x, y, serial, size):
    """
    Compute the total power of the 3x3 cell with top-left
    coordinates (x, y).
    """
    result = 0
    for i in range(x, x + size):
        for j in range(y, y + size):
            result += cell_power(i, j, serial)
    return result


def find_largest_square_fixed_size(serial, size=3):
    max_square = None
    max_power = -float('inf')
    x = y = 1
    while x + size <= 300:
        while y + size <= 300:
            power = total_power_square(x, y, serial, size)
            if power > max_power:
                max_power = power
                max_square = (x, y)
            y += 1
        x += 1
        y = 1
    return max_square


def find_largest_square(serial):
    """
    Find the nxn square in the grid with the largest total cell power,
    and return its top-left coordinates and its size.
    """
    max_size = 1
    max_square = None
    max_power = -float('inf')

    # Precompute all single cell powers
    powers = []
    for y in range(300):
        powers.append([])
        for x in range(300):
            powers[y].append(cell_power(x+1, y+1, serial))

    # Memoize the total powers of squares of previous steps
    previous_power = copy.deepcopy(powers)

    for size in range(1, 300):
        x = y = 1
        while x + size <= 300:
            while y + size <= 300:
                power = previous_power[y-1][x-1]
                if size != 1:
                    # Add the new row/column
                    for i in range(x, x + size):
                        power += powers[y+size-2][i-1]
                    # Do not add the corner twice
                    for j in range(y, y + size - 1):
                        power += powers[j-1][x+size-2]
                    # Update the map
                    previous_power[y-1][x-1] = power

                if power > max_power:
                    max_power = power
                    max_square = (x, y)
                    max_size = size
                y += 1
            x += 1
            y = 1

    return max_square, max_size


def main():
    serial = 5468
    # Part 1
    x, y = find_largest_square_fixed_size(serial)
    print("Part 1:", x, y)

    # Part 2
    max_square, size = find_largest_square(serial)
    x, y = max_square
    print("Part 2:", x, y, size)


if __name__ == "__main__":
    main()
