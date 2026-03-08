from grid import Grid
from player import Player
import pickups

score = 0
inventory = []
moves = 0

# 1. Skapa grid
g = Grid(width=20, height=15)

# 2. Skapa väggar
g.make_walls()

# 3. Räkna ut mitten
start_x = g.width // 2
start_y = g.height // 2

# 4. Skapa spelaren
player = Player(start_x, start_y)

# 5. Placera spelaren
g.set_player(player)

# 6. Lägg ut pickups
pickups.randomize(g)
# --- RÄKNA TOTALA PICKUPS ---
total_pickups = len([cell for row in g.data for cell in row if hasattr(cell, "value")])

# --- PLACERA EXIT ---
exit_x, exit_y = g.place_exit()

# 7. Skriv ut kartan
print("--------------------------------------")
print(f"You have {score} points.")
print(g)

# 8. SPEL-LOOPEN
while True:
    cmd = input("Move (WASD, Q to quit, I for inventory): ").lower()
    # --- JUMP-LOGIK ---
    jump = False
    if len(cmd) == 2 and cmd[0] == "j" and cmd[1] in "wasd":
        jump = True
        cmd = cmd[1]  # ta riktningen (w/a/s/d)

    if cmd == "q":
        break

    if cmd == "i":
        print("--------------------------------------")
        print(f"You have {score} points.")
        print("Inventory:")
        if not inventory:
            print("  (empty)")
        else:
            for item in inventory:
                print(f" - {item.symbol}({item.value})")
        print("--------------------------------------")
        continue

    dx = dy = 0

    if cmd == "w":
        dy = -1
    elif cmd == "s":
        dy = 1
    elif cmd == "a":
        dx = -1
    elif cmd == "d":
        dx = 1
    else:
        print("Unknown command.")
        continue
    step = 2 if jump else 1
    new_x = player.pos_x + dx * step
    new_y = player.pos_y + dy * step

    # --- EXIT-LOGIK ---
    if new_x == exit_x and new_y == exit_y:
        if len(inventory) == total_pickups:
            print("🎉 Du har samlat alla föremål och nått exit! Du vinner spelet!")
            break
        else:
            print("Exit är låst! Samla alla föremål först.")
            continue

    # Väggkollision med spade-logik
    if g.get(new_x, new_y) == "#":
        # Har spelaren en spade?
        shovel_index = None
        for i, item in enumerate(inventory):
            if isinstance(item, pickups.Shovel):
                shovel_index = i
                break

        if shovel_index is not None:
            print("You used a shovel to break the wall!")
            inventory.pop(shovel_index)  # spaden förbrukas
            g.clear(new_x, new_y)  # väggen tas bort
        else:
            print("You hit a wall!")
            continue

    # Pickup?
    cell = g.get(new_x, new_y)

    # --- FÄLLA ---
    if isinstance(cell, pickups.Trap):
        score += cell.value   # -10
        print("You stepped on a trap! -10 points!")
        # Fällan ligger kvar → ingen clear()

    # --- FRUKT ---
    elif isinstance(cell, pickups.Item):
        score += cell.value
        inventory.append(cell)
        print(f"You picked up a fruit worth {cell.value} points!")
        g.clear(new_x, new_y)  # frukten försvinner

    # Spade
    elif isinstance(cell, pickups.Shovel):
        inventory.append(cell)
        print("You picked up a shovel!")
        g.clear(new_x, new_y)

    # Flytta spelaren
    old_x = player.pos_x
    old_y = player.pos_y

    player.move(dx, dy)
    g.move_player_marker(old_x, old_y, player.pos_x, player.pos_y)

    # The floor is lava – varje steg kostar 1 poäng
    score -= 1

    # Räkna drag
    moves += 1

    # Bördig jord – var 25:e drag skapas en ny frukt
    if moves % 25 == 0:
        x = g.get_random_x()
        y = g.get_random_y()
        if g.is_empty(x, y):
            new_fruit = pickups.Item(20, "F")
            g.set(x, y, new_fruit)
            print("🌱 Fertile soil! A new fruit has grown somewhere on the map.")

    # Rita om kartan
    print("--------------------------------------")
    print(f"You have {score} points.")
    print("Inventory:", [f"{item.symbol}({item.value})" for item in inventory])
    print(g)