import copy


class Railmap:
    cart_icons_to_dir = {
        '<': (-1, 0),
        '>': (1, 0),
        '^': (0, -1),
        'v': (0, 1)
    }

    def __init__(self, railmap):
        self.carts = []
        self.initial_railmap = copy.deepcopy(railmap)
        self.collision = False
        self.railmap = railmap
        self.build_railmap()

    def reset(self):
        self.railmap = copy.deepcopy(self.initial_railmap)
        self.build_railmap()

    def build_railmap(self):
        cart_num = 0
        for y in range(len(self.railmap)):
            line = self.railmap[y]
            for x in range(len(line)):
                tile = line[x]
                if tile in self.cart_icons_to_dir:
                    cart = Cart(cart_num, (x, y), self.cart_icons_to_dir[tile])
                    self.carts.append(cart)
                    if tile == '<' or tile == '>':
                        self.railmap[y][x] = '-'
                    else:
                        self.railmap[y][x] = '|'
                    cart_num += 1

    def find_first_collision(self):
        while not self.collision:
            result = self.tick(stop_on_collision=True)
        return result[0], result[1]

    def tick(self, stop_on_collision=False, remove_on_collision=False):
        # Move all carts
        for i in range(len(self.carts)):
            cart = self.carts[i]
            cart.tick()

            # Check if cart has to turn
            x, y = cart.pos
            tile = self.railmap[y][x]
            if tile == '+':
                cart.turn_free()
            elif tile == '\\' or tile == '/':
                cart.turn(tile)

            # Check for collisions
            self.collision = self.check_collision(cart)
            if self.collision and stop_on_collision:
                return x, y

            if self.collision and remove_on_collision:
                # Remove the current cart
                self.carts.remove(cart)
                i -= 1
                # Remove the cart with which it collided
                for other in self.carts:
                    if other.pos == (x, y):
                        if self.carts.index(other) <= i:
                            i -= 1
                        self.carts.remove(other)

        # Sort the cart list by their coordinates
        sorted(self.carts, key=lambda c: (c.pos[1], c.pos[0]))

    def check_collision(self, cart):
        for other in self.carts:
            if cart.pos == other.pos and cart.id != other.id:
                return True
        return False


class Cart:
    def __init__(self, id, pos, direction):
        self.id = id
        self.pos = pos
        self.direction = direction
        self.next_turn = 0  # Left

    def turn_free(self):
        if self.next_turn == 0:
            self.turn_left()
        elif self.next_turn == 2:
            self.turn_right()
        self.next_turn = (self.next_turn + 1) % 3

    def turn(self, icon):
        dx, dy = self.direction
        if icon == '\\':
            if dx == 0:
                self.turn_left()
            else:
                self.turn_right()
        elif icon == '/':
            if dx == 0:
                self.turn_right()
            else:
                self.turn_left()

    def turn_left(self):
        self.direction = (self.direction[1], -self.direction[0])

    def turn_right(self):
        self.direction = (-self.direction[1], self.direction[0])

    def tick(self):
        x, y = self.pos
        x += self.direction[0]
        y += self.direction[1]
        self.pos = (x, y)


def main():
    with open("input") as f:
        railmap = [list(s) for s in f.read().splitlines()]

    railmap = Railmap(railmap)

    # Part 1
    x, y = railmap.find_first_collision()
    print(f"First collision: {x}, {y}")


if __name__ == "__main__":
    main()
