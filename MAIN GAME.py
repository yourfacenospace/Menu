import tkinter as tk
import random
import math
from PIL import Image, ImageTk

# ─────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────
SIZE = 32        # grid size
TILE = 20        # tile size (pixels)

root = tk.Tk()
root.title("Grid Defense Advanced Combat")

canvas = tk.Canvas(root, width=SIZE*TILE, height=SIZE*TILE+120, bg="#111")
canvas.pack()

# ─────────────────────────────────────
# LOAD TEXTURES
# ─────────────────────────────────────

# base tile
tile_img_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\pngg tane.png")
tile_img_raw = tile_img_raw.resize((TILE, TILE))
tile_img = ImageTk.PhotoImage(tile_img_raw)

# room settings
ROOM_SIZE = 25
room_start_x = SIZE//2 - ROOM_SIZE//2
room_start_y = SIZE//2 - ROOM_SIZE//2
room_pixel_size = ROOM_SIZE * TILE

# room image
room_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\lvl1.png")
room_raw = room_raw.resize((room_pixel_size, room_pixel_size))
room_img = ImageTk.PhotoImage(room_raw)

# treasure image
TREASURE_SCALE = 2.0
treasure_size = int(TILE * TREASURE_SCALE)

# ─────────────────────────────────────
# PLACEMENT INDICATOR
# ─────────────────────────────────────
hover_x, hover_y = None, None

def motion(event):
    global hover_x, hover_y

    gx = event.x // TILE
    gy = (event.y - 120) // TILE

    # only show inside room area
    if 0 <= gx < SIZE and 0 <= gy < SIZE:
        hover_x, hover_y = gx, gy
    else:
        hover_x, hover_y = None, None

canvas.bind("<Motion>", motion)

# ─── DRAW PLACEMENT INDICATOR ───────
if hover_x is not None and hover_y is not None:
    px = hover_x * TILE
    py = hover_y * TILE + 120

    # don't draw if there's already a tower
    if grid[hover_y][hover_x] is None:
        canvas.create_rectangle(px + 2, py + 2,
                                px + TILE - 2, py + TILE - 2,
                                outline="yellow", width=2)

# ─────────────────────────────────────
# SCALE SETTINGS (change these to resize weapons and treasures)
# ─────────────────────────────────────
WEAPON_SCALE = 2      # 1.0 = original TILE size, 1.5 = 1.5x TILE
TREASURE_SCALE = 3    # 2.0 = double TILE size

# cannon / basic
cannon_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\truecanon.png")
cannon_raw = cannon_raw.resize((int(TILE*WEAPON_SCALE), int(TILE*WEAPON_SCALE)))
cannon_img = ImageTk.PhotoImage(cannon_raw)

# splash / balista
splash_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\balista.png")
splash_raw = splash_raw.resize((int(TILE*WEAPON_SCALE), int(TILE*WEAPON_SCALE)))
splash_img = ImageTk.PhotoImage(splash_raw)

# trap / punji
trap_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\punji.png")
trap_raw = trap_raw.resize((int(TILE*WEAPON_SCALE), int(TILE*WEAPON_SCALE)))
trap_img = ImageTk.PhotoImage(trap_raw)

# treasure
treasure_size = int(TILE * TREASURE_SCALE)
treasure_raw = Image.open("C:\\Users\\Dalya\\PycharmProjects\\PythonProject1\\.venv\\treasuree.png")
treasure_raw = treasure_raw.resize((treasure_size, treasure_size))
treasure_img = ImageTk.PhotoImage(treasure_raw)



# ─────────────────────────────────────
# GAME STATE
# ─────────────────────────────────────

grid = [[None]*SIZE for _ in range(SIZE)]
enemies = []
projectiles = []

money = 200
wave = 1

mode = "build"
selected_weapon = "basic"

game_over = False
game_win = False

spawn_count = 0
spawn_limit = 20

# tower settings
costs = {"basic": 10, "splash": 30, "trap": 15}
colors = {"basic": "#3fa7ff", "splash": "#ff9f43", "trap": "#2ecc71"}

# ─────────────────────────────────────
# TREASURES (OBJECTIVES)
# ─────────────────────────────────────
treasures = [
    {"pos": (room_start_x + 18, room_start_y + 10), "hp": 20}
]

# ─────────────────────────────────────
# ENEMY PATH (WAYPOINTS)
# ─────────────────────────────────────
path = [
    (room_start_x - 1, room_start_y + 12),
    (room_start_x + 4, room_start_y + 12),
    (room_start_x + 4, room_start_y + 4),
    (room_start_x + 18, room_start_y + 4),
    (room_start_x + 18, room_start_y + 20),
    (room_start_x + 6, room_start_y + 20),
    (room_start_x + 6, room_start_y + 9),
    (room_start_x + 18, room_start_y + 9)
]

# ─────────────────────────────────────
# STRUCTURE CLASS (TOWERS)
# ─────────────────────────────────────
class Structure:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_
        self.cooldown = 0

        if type_ == "basic":
            self.range = 6
        elif type_ == "splash":
            self.range = 5
        elif type_ == "trap":
            self.range = 0
            self.kills = 0


# ─────────────────────────────────────
# ENEMY CLASS
# ─────────────────────────────────────
class Enemy:
    def __init__(self):
        target = random.choice(treasures)["pos"]

        # random path variation
        nodes = random.sample(path[1:-1], random.randint(2, 4))
        self.route = [path[0]] + nodes + [target]

        self.path_index = 0
        self.x, self.y = self.route[0]

        self.speed = 0.10
        self.maxhp = 3
        self.hp = 3

    def move(self):
        if self.path_index >= len(self.route) - 1:
            return

        tx, ty = self.route[self.path_index + 1]
        dx, dy = tx - self.x, ty - self.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < 0.1:
            self.path_index += 1
        else:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed


# ─────────────────────────────────────
# DRAW FUNCTION (RENDER EVERYTHING)
# ─────────────────────────────────────
def draw():
    canvas.delete("all")

    # GAME STATES
    if game_over:
        canvas.create_text(320, 350, text="GAME OVER", fill="red", font=("Arial", 40))
        return

    if game_win:
        canvas.create_text(320, 350, text="LEVEL COMPLETED", fill="lime", font=("Arial", 40))
        return

    # UI PANEL
    canvas.create_rectangle(0, 0, SIZE*TILE, 120, fill="#222")

    canvas.create_text(10, 20, fill="white", anchor="w",
                       text=f"Money:{money} Wave:{wave}")

    canvas.create_text(10, 40, fill="white", anchor="w",
                       text=f"Selected: {selected_weapon.upper()}")

    # buttons
    canvas.create_rectangle(400, 20, 500, 50, fill="#3a3")
    canvas.create_text(450, 35, text="START", fill="white")

    canvas.create_rectangle(510, 20, 630, 50, fill="#a33")
    canvas.create_text(570, 35, text="SURRENDER", fill="white")

    # weapon selection
    for i, w in enumerate(["basic", "splash", "trap"]):
        x1 = 10 + i*110
        x2 = x1 + 100
        outline = "yellow" if selected_weapon == w else "black"

        canvas.create_rectangle(x1, 70, x2, 100,
                                fill=colors[w], outline=outline, width=3)

        canvas.create_text((x1+x2)//2, 85,
                           text=f"{w.upper()} (${costs[w]})")

    offset = 120

    # ─── DRAW MAP ─────────────────
    for y in range(SIZE):
        for x in range(SIZE):

            # skip room tiles (covered by big image)
            if (room_start_x <= x < room_start_x+ROOM_SIZE and
                room_start_y <= y < room_start_y+ROOM_SIZE):
                continue

            canvas.create_image(x*TILE, y*TILE+offset,
                                image=tile_img, anchor="nw")

    # draw room
    canvas.create_image(
        room_start_x*TILE,
        room_start_y*TILE+offset,
        image=room_img,
        anchor="nw"
    )

    # ─── DRAW TREASURES ───────────
    for t in treasures:
        tx, ty = t["pos"]

        px = tx*TILE + TILE//2
        py = ty*TILE + offset + TILE//2

        canvas.create_image(px - treasure_size//2,
                            py - treasure_size//2,
                            image=treasure_img, anchor="nw")

        # HP BAR
        bar_w = 40
        hp_ratio = t["hp"] / 20

        canvas.create_rectangle(px-bar_w//2, py-35,
                                px+bar_w//2, py-30, fill="black")

        canvas.create_rectangle(px-bar_w//2, py-35,
                                px-bar_w//2 + bar_w*hp_ratio,
                                py-30, fill="lime")

    # ─── DRAW STRUCTURES ──────────
    for row in grid:
        for s in row:
            if s:
                px = s.x * TILE
                py = s.y * TILE + offset

                # use images based on type
                if s.type == "basic":
                    canvas.create_image(px, py, image=cannon_img, anchor="nw")
                elif s.type == "splash":
                    canvas.create_image(px, py, image=splash_img, anchor="nw")
                elif s.type == "trap":
                    canvas.create_image(px, py, image=trap_img, anchor="nw")
                else:
                    canvas.create_rectangle(px + 4, py + 4,
                                            px + TILE - 4, py + TILE - 4,
                                            fill=colors[s.type])


    # ─── DRAW ENEMIES ─────────────
    for e in enemies:
        px = int(e.x*TILE)
        py = int(e.y*TILE) + offset

        canvas.create_oval(px+3, py+3,
                           px+TILE-3, py+TILE-3,
                           fill="red")

        # HP BAR
        hp_ratio = e.hp/e.maxhp

        canvas.create_rectangle(px, py-6,
                                px+TILE, py-3, fill="black")

        canvas.create_rectangle(px, py-6,
                                px+TILE*hp_ratio, py-3, fill="lime")

    # ─── DRAW PROJECTILES ─────────
    for p in projectiles:
        color = "white" if p["type"] == "basic" else "#ff0"

        canvas.create_oval(p["x"]-4, p["y"]-4,
                           p["x"]+4, p["y"]+4,
                           fill=color)


# ─────────────────────────────────────
# UPDATE LOGIC (GAME LOOP)
# ─────────────────────────────────────
def update():
    global spawn_count, wave, spawn_limit, game_over, game_win

    if mode == "battle" and not game_over:

        # spawn enemies
        if spawn_count < spawn_limit and random.random() < 0.05:
            enemies.append(Enemy())
            spawn_count += 1

        # move enemies
        for e in enemies[:]:
            # ─── MOVE ENEMY ─────────────────────────
            if not hasattr(e, "attacking"):  # initialize attack flags if missing
                e.attacking = False
                e.attack_cooldown = 0

            if not e.attacking:
                e.move()

            # ─── CHECK TREASURE HIT ─────────────────
            for t in treasures:
                tx, ty = t["pos"]

                # if enemy is close enough to treasure
                if math.hypot(e.x - tx, e.y - ty) < 0.5:
                    e.attacking = True

                    # attack cooldown
                    if e.attack_cooldown <= 0:
                        t["hp"] -= 1  # damage per hit
                        e.attack_cooldown = 20  # attack speed (frames)
                    else:
                        e.attack_cooldown -= 1

                    # treasure destroyed
                    if t["hp"] <= 0:
                        game_over = True

                    break

        # towers attack
        for row in grid:
            for s in row:
                if not s:
                    continue

                if s.cooldown > 0:
                    s.cooldown -= 1
                    continue

                # trap
                if s.type == "trap":
                    for e in enemies:
                        if math.hypot(e.x-s.x, e.y-s.y) <= 1.2:
                            e.hp = 0
                            s.kills += 1
                            if s.kills >= 5:
                                grid[s.y][s.x] = None
                            break

                # shooters
                elif s.type in ["basic", "splash"]:
                    for e in enemies:
                        if math.hypot(e.x-s.x, e.y-s.y) <= s.range:
                            projectiles.append({
                                "x": s.x*TILE + TILE//2,
                                "y": s.y*TILE + 120 + TILE//2,
                                "target": e,
                                "type": s.type
                            })
                            s.cooldown = 30 if s.type == "basic" else 45
                            break

        # projectile movement
        for p in projectiles[:]:
            if p["target"] not in enemies:
                projectiles.remove(p)
                continue

            tx = p["target"].x*TILE + TILE//2
            ty = p["target"].y*TILE + 120 + TILE//2

            p["x"] += (tx-p["x"]) * 0.2
            p["y"] += (ty-p["y"]) * 0.2

            if math.hypot(p["x"]-tx, p["y"]-ty) < 6:
                target = p["target"]

                if p["type"] == "basic":
                    target.hp -= 1
                else:
                    target.hp -= 2

                projectiles.remove(p)

        enemies[:] = [e for e in enemies if e.hp > 0]

        # wave progression
        if spawn_count >= spawn_limit and len(enemies) == 0:
            if wave == 1:
                wave = 2
                spawn_count = 0
                spawn_limit = 30

                treasures.append({"pos": (room_start_x+18, room_start_y+4), "hp": 20})
                treasures.append({"pos": (room_start_x+18, room_start_y+15), "hp": 20})
            else:
                game_win = True

    draw()
    root.after(50, update)


# ─────────────────────────────────────
# INPUT HANDLING
# ─────────────────────────────────────
def click(event):
    global mode, selected_weapon, money

    if event.y <= 120:

        # start
        if 20 <= event.y <= 50 and 400 <= event.x <= 500:
            mode = "battle"
            return

        # surrender
        if 20 <= event.y <= 50 and 510 <= event.x <= 630:
            root.destroy()
            return

        # weapon select
        for i, w in enumerate(["basic", "splash", "trap"]):
            x1 = 10 + i*110
            x2 = x1 + 100

            if 70 <= event.y <= 100 and x1 <= event.x <= x2:
                selected_weapon = w
                return

    # place structure
    gx = event.x // TILE
    gy = (event.y - 120) // TILE

    if (room_start_x <= gx < room_start_x+ROOM_SIZE and
        room_start_y <= gy < room_start_y+ROOM_SIZE):

        if grid[gy][gx] is None:
            cost = costs[selected_weapon]

            if money >= cost:
                grid[gy][gx] = Structure(gx, gy, selected_weapon)
                money -= cost


def double_click(event):
    global money

    if event.y > 120:
        gx = event.x // TILE
        gy = (event.y - 120) // TILE

        if grid[gy][gx]:
            money += costs[grid[gy][gx].type]
            grid[gy][gx] = None


# ─────────────────────────────────────
# BIND EVENTS + START LOOP
# ─────────────────────────────────────
canvas.bind("<Button-1>", click)
canvas.bind("<Double-Button-1>", double_click)

update()
root.mainloop()