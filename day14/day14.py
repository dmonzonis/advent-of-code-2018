class Recipes:
    def __init__(self, first, second):
        self.recipes = [first, second]
        # Indexes currently being worked with
        self.elf1 = 0
        self.elf2 = 1

    def advance_elves(self):
        self.elf1 = (self.elf1 + 1 +
                     self.recipes[self.elf1]) % len(self.recipes)
        self.elf2 = (self.elf2 + 1 +
                     self.recipes[self.elf2]) % len(self.recipes)

    def combine_step(self):
        first = self.recipes[self.elf1]
        second = self.recipes[self.elf2]
        self.recipes += Recipes.combine_recipes(first, second)
        self.advance_elves()

    def get_subset(self, start, count=10):
        return self.recipes[start:start + count]

    def find_pattern(self, pattern, start=0):
        string = ''.join(str(c) for c in self.recipes[start:])
        return string.find(pattern)

    @staticmethod
    def combine_recipes(first, second):
        return [int(x) for x in list(str(first + second))]

    def __len__(self):
        return len(self.recipes)


def find_recipes_before_pattern(recipes, pattern):
    found = recipes.find_pattern(pattern)
    while found == -1:
        recipes.combine_step()
        # Search from -len(pattern) - 1 in case 2 nums were added
        found = recipes.find_pattern(pattern, -len(pattern) - 1)
    return found + len(recipes) - len(pattern) - 1


def main():
    inp = 793031
    recipes = Recipes(3, 7)

    # Part 1
    # Combine until we have enough results
    while len(recipes) < inp + 10:
        recipes.combine_step()

    print(''.join(str(c) for c in recipes.get_subset(inp)))

    # Part 2
    pattern = str(inp)
    print(find_recipes_before_pattern(recipes, pattern))  # 172962059


if __name__ == "__main__":
    main()
