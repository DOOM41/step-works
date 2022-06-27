import random
from ships import Part, Ship


def check_coords(x, y, side, length):
    if side == 0:
        return x - length >= 0
    elif side == 1:
        return y + length <= 9
    elif side == 2:
        return x + length <= 9
    elif side == 3:
        return y - length >= 0
    return True


def get_random_cell():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return x, y


def get_random_side():
    return random.randint(0, 3)


def get_random_coords(length):
    x, y = get_random_cell()
    side = get_random_side()
    while not check_coords(x, y, side, length):
        x, y = get_random_cell()
        side = get_random_side()
    coords = []
    for i in range(length):
        if side == 0:
            coords.append((x - i, y))
        elif side == 1:
            coords.append((x, y + i))
        elif side == 2:
            coords.append((x + i, y))
        elif side == 3:
            coords.append((x, y - i))
    return coords


def create_ship_for_random(coords):
    parts = []
    for coord in coords:
        coord = coord
        parts.append(Part(*coord, len(coords)))
    return Ship(parts)
