results = {
    1: "Попал",
    2: "Убил",
    0: "Промах"
}

coords_dict = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
}


def get_coord(data):
    char = data[0]
    num = int(data[1])
    return num, coords_dict.get(char)