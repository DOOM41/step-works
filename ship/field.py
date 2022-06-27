import check
import ships
import tools


class Field:
    def __init__(self, n=10):
        self.field = [["0"]*n for _ in range(n)]
        self.ships = {}
        self.ship_count = {
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }

    def __str__(self):
        resoult_row = '  A B C D E F G H I J\n'
        for i, row in enumerate(self.field):
            str_row = ' '.join(map(str, row))
            resoult_row += f'{i} {str_row}\n'
        return resoult_row

    def add_ship(self, ship):
        self.check_to_put(ship)
        for part in ship.parts:
            self.field[part.x][part.y] = part
            self.ships[(part.x, part.y)] = ship

        self.ship_count[ship.type] -= 1

    def is_alive(self):
        for ship in self.ships:
            if ship.is_alive:
                return True
        return False

    def shoot(self, x, y):
        part = self.field[x][y]
        if not isinstance(part, str):
            part.is_alive = False
            if not self.ships[(part.x, part.y)].is_alive():
                return 2
            return 1
        else:
            self.field[x][y] = "."
            return 0

    def manual_placement(self):
        max_len = 4
        while max_len > 0:
            ship_len = self.ship_count[max_len]
            while self.ship_count[max_len] > 0:
                print(self.field)
                ship = ships.Ship(ships.Part(*tools.get_coord(input(f"Введите корабль длинной {ship_len}")),type=ship_len))
                self.add_ship(ship)
            max_len -= 1

    def random_placement(self):
        max_len = 4
        while max_len > 0:
            while self.ship_count[max_len] > 0:
                try:
                    coords = check.get_random_coords(max_len)
                    ship = check.create_ship_for_random(coords)
                    self.add_ship(ship)
                except Exception:
                    continue
            max_len -= 1

    def check_to_put(self, ship):
        if ship.type not in self.ship_count.keys():
            raise KeyError(f"Такого коробля не существует")
        elif self.ship_count[ship.type] == 0:
            raise Exception(f"Вы достигнули максимума")
        my_check = [
            (1, 1),
            (-1, 1),
            (1, -1),
            (0, 0),
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            (-1, -1)
        ]
        for part in ship.parts:
            for delta_x, delta_y in my_check:
                try:
                    if self.field[part.x+delta_x][part.y+delta_y] != "0":
                        raise Exception(
                            f"{self.field[part.x+delta_x][part.y+delta_y]} \
                                корабль мешается ")
                except IndexError:
                    pass
