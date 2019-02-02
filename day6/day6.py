from collections import namedtuple


Coord = namedtuple('Coord', ['x', 'y'])


def manhattan_distance(coord1, coord2):
    return abs(coord1.x - coord2.x) + abs(coord1.y - coord2.y)


def find_closest(coord, node_list):
    """Return the coordinates of the node closest to the given coord."""
    return min(node_list, key=lambda n: manhattan_distance(coord, n))


def neighbours(node):
    """Return nodes in horizontal and vertical vicinity."""
    return [
        Coord(node.x + 1, node.y),
        Coord(node.x - 1, node.y),
        Coord(node.x, node.y + 1),
        Coord(node.x, node.y - 1)
    ]


def bfs_expansion(node, node_dict, max_nodes=5000):
    """
    Returns the set of closest nodes to the given node in the node dict,
    including the node itself.

    If we reach max_nodes of nodes explored, we consider the area to be
    infinite and return an empty set.
    """
    if node not in node_dict:
        raise KeyError("Node not in dictionary.")
    queue = [node]
    count = 0
    examined = set()
    valid = set()

    while queue:
        current = queue.pop(0)
        if current in examined:
            continue
        examined.add(current)

        if find_closest(current, node_dict) == node:
            count += 1
            if count >= max_nodes:
                return set()

            valid.add(current)
            for neighbour in neighbours(current):
                if neighbour not in examined:
                    queue.append(neighbour)

    return valid


def compute_areas(node_dict):
    """
    Finds the closest node for all nodes in the bounding rect of the list of
    nodes in the dict, and updates each of the node's list of closer coords.
    """
    for node in node_dict.keys():
        node_dict[node] = bfs_expansion(node, node_dict)


def find_largest_area(node_dict):
    """Finds the node with the largest area that is not infinity."""
    return max(node_dict.keys(), key=lambda n: len(node_dict[n]))


def main():
    with open("input") as f:
        inp = f.read().splitlines()

    node_dict = {}
    for s in inp:
        x, y = [int(x) for x in s.split(', ')]
        coord = Coord(x, y)
        node_dict[coord] = set()

    # Part 1
    compute_areas(node_dict)
    largest_node = find_largest_area(node_dict)
    # Print the area
    print(len(node_dict[largest_node]))


if __name__ == "__main__":
    main()
