print("Grid loaded from:", __file__)

import random

class Grid:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.empty = "."
        self.player = None

        # Skapa tom spelplan
        self.data = [
            [self.empty for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def place_exit(self):
        import random
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            # Placera bara på tom ruta
            if self.data[y][x] == self.empty:
                self.data[y][x] = "E"
                return x, y

    # -----------------------------
    # Väggar runt hela kartan
    # -----------------------------
    def make_walls(self):
        for x in range(self.width):
            self.data[0][x] = "#"
            self.data[self.height - 1][x] = "#"
        for y in range(self.height):
            self.data[y][0] = "#"
            self.data[y][self.width - 1] = "#"
            # -----------------------------
            # Inre väggar (sammanhängande, med öppningar)
            # -----------------------------

            # Horisontell vägg 1 (rad 4)
            for x in range(2, self.width - 2):
                if x != 10:
                    self.data[4][x] = "#"

            # Horisontell vägg 2 (rad 8)
            for x in range(3, self.width - 3):
                if x != 7:
                    self.data[8][x] = "#"

            # Vertikal vägg 1 (kolumn 6)
            for y in range(2, self.height - 2):
                if y != 6:
                    self.data[y][6] = "#"

            # Vertikal vägg 2 (kolumn 14)
            for y in range(3, self.height - 3):
                if y != 10:
                    self.data[y][14] = "#"

    # -----------------------------
    # Placera spelaren
    # -----------------------------
    def set_player(self, player):
        self.player = player
        self.data[player.pos_y][player.pos_x] = "P"

    # -----------------------------
    # Flytta spelaren grafiskt
    # -----------------------------
    def move_player_marker(self, old_x, old_y, new_x, new_y):
        self.data[old_y][old_x] = self.empty
        self.data[new_y][new_x] = "P"

    # -----------------------------
    # Hjälpmetoder
    # -----------------------------
    def get(self, x, y):
        return self.data[y][x]

    def set(self, x, y, value):
        self.data[y][x] = value

    def clear(self, x, y):
        self.data[y][x] = self.empty

    def is_empty(self, x, y):
        return self.data[y][x] == self.empty

    def get_random_x(self):
        return random.randint(1, self.width - 2)

    def get_random_y(self):
        return random.randint(1, self.height - 2)

    # -----------------------------
    # Snygg utskrift av spelplanen
    # -----------------------------
    def __str__(self):
        lines = []

        # Kolumnnummer
        lines.append("   " + " ".join(str(i % 10) for i in range(self.width)))

        # Rader med radnummer
        for y, row in enumerate(self.data):
            line = f"{y:2} " + " ".join(str(cell) for cell in row)
            lines.append(line)

        return "\n".join(lines)