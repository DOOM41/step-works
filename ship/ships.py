import tools


class Part:
    def __init__(self, x, y, type: str):
        self.x = x
        self.y = y
        self.is_alive = True
        self.type = type

    def __str__(self):
        return str(self.type) if self.is_alive else "x"


class Ship:
    def __init__(self, parts):
        self.parts = parts
        self.type = len(parts)

    def __getitem__(self, coords):
        x, y = coords
        for part in self.parts:
            if part.x == x and part.y == y:
                return part

    def __iter__(self):
        return iter(self.parts)

    def is_alive(self):
        for part in self.parts:
            if part.is_alive:
                return True
        return False



def create_ship(coords):
    parts = []
    for coord in coords:
        coord = tools.get_coord(coord)
        parts.append(Part(*coord, len(coords)))
    return Ship(parts)