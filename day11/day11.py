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


def total_power_square(x, y, serial):
    """
    Compute the total power of the 3x3 cell with top-left
    coordinates (x, y).
    """
    result = 0
    for i in range(x, x + 3):
        for j in range(y, y + 3):
            result += cell_power(i, j, serial)
    return result


def find_largest_square(serial):
    """Find the 3x3 square in the grid with the largest total cell power."""
    max_square = None
    max_power = -float('inf')
    for x in range(1, 299):
        for y in range(1, 299):
            power = total_power_square(x, y, serial)
            if power > max_power:
                max_power = power
                max_square = (x, y)
    return max_square


def main():
    serial = 5468
    # Part 1
    x, y = find_largest_square(serial)
    print(f"({x}, {y})")


if __name__ == "__main__":
    main()
