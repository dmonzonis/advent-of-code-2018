class Tree:
    def __init__(self):
        self._node = 0
        self._tree = {}

    def build_tree(self, data):
        self._parse_node(data)
        return self._tree

    def _parse_node(self, data):
        num_children = data.pop(0)
        num_metadata = data.pop(0)
        current_node = self._node
        self._tree[current_node] = [[], []]
        # Add to children list
        for n in range(num_children):
            self._tree[current_node][0].append(current_node + n + 1)
        # Parse children nodes
        for n in range(num_children):
            self._node += 1
            self._parse_node(data)
        for n in range(num_metadata):
            metadata = data.pop(0)
            self._tree[current_node][1].append(metadata)

    def sum_metadata(self):
        result = 0
        for node_data in self._tree.values():
            metadata = node_data[1]
            result += sum(metadata)
        return result


def main():
    with open("input") as f:
        nums = [int(x) for x in f.read().strip().split()]

    # Part 1
    tree = Tree()
    tree.build_tree(nums)
    print(tree.sum_metadata())


if __name__ == "__main__":
    main()
