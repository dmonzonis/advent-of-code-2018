class Tree:
    def __init__(self):
        self._max_node = 0
        self._tree = {}

    def build_tree(self, data):
        self._parse_node(data, 0)

    def _parse_node(self, data, node):
        num_children = data.pop(0)
        num_metadata = data.pop(0)
        self._tree[node] = [[], []]
        # Add to children list
        for n in range(num_children):
            self._max_node += 1
            self._tree[node][0].append(self._max_node)
        # Parse children nodes
        for child in self._tree[node][0]:
            self._parse_node(data, child)
        # Save metadata
        for n in range(num_metadata):
            metadata = data.pop(0)
            self._tree[node][1].append(metadata)

    def sum_metadata(self):
        result = 0
        for node_data in self._tree.values():
            metadata = node_data[1]
            result += sum(metadata)
        return result

    def is_leaf(self, node):
        if node not in self._tree:
            raise KeyError("Node not in tree.")
        return len(self._tree[node][0]) == 0

    def get_value(self, node):
        if self.is_leaf(node):
            # Value is the sum of its metadata
            return sum(self._tree[node][1])
        # Otherwise, metadata are indexes
        value = 0
        for index in self._tree[node][1]:
            index -= 1
            if 0 <= index < len(self._tree[node][0]):
                value += self.get_value(self._tree[node][0][index])
        return value


def main():
    with open("input") as f:
        nums = [int(x) for x in f.read().strip().split()]

    # Part 1
    tree = Tree()
    tree.build_tree(nums)
    print(tree.sum_metadata())

    # Part 2
    print(tree.get_value(0))


if __name__ == "__main__":
    main()
