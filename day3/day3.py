import re
import numpy as np


MAX_WIDTH = 1000
MAX_HEIGHT = 1000


class Fabric:

    def __init__(self):
        # Array that stores the coincidences
        self._fabric = np.zeros((MAX_WIDTH, MAX_HEIGHT))
        # Stores all claims
        self._claims = []

    def add_claim(self, params):
        x, y = params['x'], params['y']
        width, height = params['width'], params['height']
        self._fabric[x:x + width, y:y + height] += 1
        self._claims.append(params)

    def count_overlaps(self):
        return (self._fabric > 1).sum()

    def find_non_overlapping_claim(self):
        for claim in self._claims:
            x, y = claim['x'], claim['y']
            width, height = claim['width'], claim['height']
            if (self._fabric[x:x + width, y:y + height] < 2).all():
                return claim['id']


def get_claim_params(s):
    matches = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', s)
    params = {
        'id': int(matches.group(1)),
        'x': int(matches.group(2)),
        'y': int(matches.group(3)),
        'width': int(matches.group(4)),
        'height': int(matches.group(5)),
    }
    return params


def main():
    with open("input") as f:
        claim_strings = f.read().splitlines()

    fabric = Fabric()

    for s in claim_strings:
        params = get_claim_params(s)
        fabric.add_claim(params)

    # Part 1
    print(fabric.count_overlaps())

    # Part 2
    print(fabric.find_non_overlapping_claim())


if __name__ == "__main__":
    main()
