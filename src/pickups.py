import random

class Item:
    def __init__(self, value, symbol="?"):
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class Trap(Item):
    def __init__(self):
        super().__init__(value=-10, symbol="X")   # -10 poäng, symbol X
class Shovel(Item):
    def __init__(self):
        super().__init__(value=0, symbol="S")   # 0 poäng, symbol S

class Key(Item):
    def __init__(self):
        super().__init__(value=0, symbol="K")   # 0 poäng, symbol K


class Chest(Item):
    def __init__(self):
        super().__init__(value=0, symbol="C")   # 0 poäng, symbol C


class Treasure(Item):
    def __init__(self):
        super().__init__(value=100, symbol="T")  # 100 poäng, symbol T


def randomize(grid):
    # Slumpa frukter (värde 20)
    for _ in range(10):
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            fruit = Item(20, "F")
            grid.set(x, y, fruit)

    # Slumpa fällor (värde -10)
    for _ in range(5):
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            trap = Trap()
            grid.set(x, y, trap)
    # Slumpa spade
    for _ in range(1):
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            shovel = Shovel()
            grid.set(x, y, shovel)
    # Slumpa 2 nycklar
    for _ in range(2):
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            key = Key()
            grid.set(x, y, key)

    # Slumpa 2 kistor
    for _ in range(2):
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            chest = Chest()
            grid.set(x, y, chest)