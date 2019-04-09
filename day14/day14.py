class Recipes:
    def __init__(self, first, second):
        self.recipes = [first, second]
        # Indexes currently being worked with
        self.elf1 = 0
        self.elf2 = 1
    
    def advance_elves(self):
        self.elf1 = (self.elf1 + 1 + self.recipes[self.elf1]) % len(self.recipes)
        self.elf2 = (self.elf2 + 1 + self.recipes[self.elf2]) % len(self.recipes)

    def combine_step(self):
        first = self.recipes[self.elf1]
        second = self.recipes[self.elf2]
        self.recipes += combine_recipes(first, second)
        self.advance_elves()

    def get_subset(self, start, count=10):
        return self.recipes[start:start + count]

    def __repr__(self):
        return ",".join(str(x) for x in self.recipes)


def combine_recipes(first, second):
    return [int(x) for x in list(str(first + second))]


def main():
    inp = 793031
    recipes = Recipes(3, 7)

    # Part 1
    # Combine until we have enough results
    while len(recipes.recipes) < inp + 10:
        recipes.combine_step()
    
    print("".join(str(x) for x in recipes.get_subset(inp)))


if __name__ == "__main__":
    main()
