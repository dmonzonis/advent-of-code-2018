from collections import namedtuple
import re
from PIL import Image
import pytesseract


Vector = namedtuple('Vector', ['x', 'y'])


class Star:
    def __init__(self, position, velocity):
        self._position = position
        self._velocity = velocity

    def update(self):
        new_x = self._position.x + self._velocity.x
        new_y = self._position.y + self._velocity.y
        self._position = Vector(new_x, new_y)

    @property
    def position(self):
        return self._position


class StarMap:
    def __init__(self):
        self.stars = []

    def add_star(self, star):
        self.stars.append(star)

    def update(self):
        for star in self.stars:
            star.update()

    def get_rect(self, margin=10):
        """
        Get a rectangle slightly bigger than the bounding rectangle of the
        stars in the map.
        """
        min_x = min_y = float('inf')
        max_x = max_y = -float('inf')
        for star in self.stars:
            pos = star._position
            if pos.x < min_x:
                min_x = pos.x
            if pos.x > max_x:
                max_x = pos.x
            if pos.y < min_y:
                min_y = pos.y
            if pos.y > max_y:
                max_y = pos.y
        top_left = Vector(min_x - margin, min_y - margin)
        bottom_right = Vector(max_x + margin, max_y + margin)
        return top_left, bottom_right

    def draw(self):
        """
        Return a scaled up image with the star positions as black pixels on
        a white background.
        """
        top_left, bottom_right = self.get_rect()
        min_x, min_y = top_left
        max_x, max_y = bottom_right
        width = max_x - min_x
        height = max_y - min_y

        # There's no way the message is going to be that big
        if width > 100 or height > 100:
            return None

        img = Image.new('1', (width, height), color=1)  # White background
        for star in self.stars:
            pos = star._position
            x = pos.x - min_x
            y = pos.y - min_y
            img.putpixel((x, y), 0)  # Put black pixel on star position

        img = img.resize((width * 5, height * 5), Image.ANTIALIAS)
        return img


def fill_star_map(star_map, data):
    for line in data:
        match = re.match(
            r'position=<\s?(-?\d+), \s?(-?\d+)> velocity=<\s?(-?\d+), \s?(-?\d+)>',
            line
        )
        x, y, dx, dy = [int(n) for n in match.groups()]
        pos = Vector(x, y)
        velocity = Vector(dx, dy)
        star = Star(pos, velocity)
        star_map.add_star(star)


def find_messages(star_map, times=100000):
    for t in range(times):
        img = star_map.draw()
        if img is not None:
            message = pytesseract.image_to_string(img)
            if message:
                print(f"Message found at t={t} seconds")
                print(message)
                img.show()
        star_map.update()


def main():
    with open("input") as f:
        data = f.read().splitlines()

    star_map = StarMap()
    fill_star_map(star_map, data)
    find_messages(star_map)


if __name__ == "__main__":
    main()
