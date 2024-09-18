import pygame
import math
import random as rd

# Hardcoded variables here

WIDTH, HEIGHT = 500, 300
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 153, 51)
GREY = (160, 160, 160)
DG = (96, 96, 96)
gridL = 30
gridT = 10
SEED = 0
solution_path = []

MAX_L = 20

ph, pw = gridL, gridL
VEL = gridL
PATH = []
PATHS = []
inp = ""
while inp != "1" and inp != "2":
    inp = input("DFS or Hunt and Kill(1 or 2): ")
inp = int(inp)

RES = input("Dimension (10x10): ").split("x")
while len(RES) != 2:
    while len(RES) != 2 or not RES[0].isnumeric() or not RES[1].isnumeric():
        RES = input("Dimension (10x10): ").split("x")

RES = ((int(RES[0])+2)*gridL, (int(RES[1])+2)*gridL)
WIDTH = RES[0]
HEIGHT = RES[1]


ROW = int(WIDTH/gridL - 2)
COL = int(HEIGHT/gridL - 2)


xw = True
yw = True


class Wall:
    def __init__(self, cords, erected, rect):
        self.cords = cords
        self.erected = erected
        self.rect = rect


class Grid:

    def __init__(self, val, cords, rect, visited, color, neighbors):
        self.val = val
        self.cords = cords
        self.rect = rect
        self.visited = visited
        self.color = color
        self.neighbors = neighbors


class Cords:
    def __init__(self, row, col):
        self.row = row
        self.col = col


# checks if there is any possible not visited grid from the chosen grid0 and returning them, if there are any
# (the visited grids are marked to not cause any looping pathways inside the maze)
def check_moves(grid0, grids):
    gs = []
    if grid0.val <= (ROW*COL) - ROW:
        down = grids[int(grid0.val + ROW - 1)]
        if not down.visited:
            gs.append(down)

    if grid0.val >= 1 + ROW:
        # print(grid0.cords.row-2)
        up = grids[int(grid0.val - ROW - 1)]
        # print("up: " + str(up.val))
        if not up.visited:
            gs.append(up)

    if grid0.cords.col < ROW:
        right = grids[int(grid0.val)]

        if not right.visited:
            gs.append(right)

    if grid0.cords.col > 1:
        left = grids[int(grid0.val - 2)]

        if not left.visited:
            gs.append(left)

    return gs


# removes the walls between two grids
# (by the algorithm all walls are erected at first)
def build_paths(choice, grid0, walls):
    global PATH
    new_p = 0
    grid0.neighbors.append(choice)

    if grid0.cords.row == choice.cords.row:
        if grid0.val < choice.val:
            new_p = walls[1][int(choice.val + (choice.cords.row - 1) - 1)]

        else:
            new_p = walls[1][int(grid0.val + (grid0.cords.row - 1) - 1)]
    else:
        if grid0.val > choice.val:
            new_p = walls[0][int(choice.val) - 1 + ROW]
        else:
            new_p = walls[0][int(grid0.val) - 1 + ROW]

    new_p.erected = False


# generates a corridor until a dead end forms
# or the maximum corridor length(MAX_L) is reached if you uncomment the 159. line
def generate_corridor(grid0, grids, walls, path, color):
    global PATH
    n = 0
    p = []
    while True:

        p = path
        gs = []
        grid0.visited = True
        PATH.append(grid0)
        if n >= MAX_L:
            break
        # print(f"grid {grid0.val} is visited")

        gs = check_moves(grid0, grids)

        if len(gs) != 0:
            choice = rd.choice(gs)
            build_paths(choice, grid0, walls)
            grid0 = choice
            p.append((grid0.cords.row, grid0.cords.col))
            grid0.color = color

        else:
            break

        #n += 1

    return p


def draw_window(p1, keys_pressed, grids, walls, WIN):
    global x, y
    show_pathways = False
    WIN.fill(GREY)
    if keys_pressed[pygame.K_x]:
        show_pathways = True
    for g in grids:
        if show_pathways:
            pygame.draw.rect(WIN, g.color, g.rect)
        else:
            pygame.draw.rect(WIN, DG, g.rect)
    if keys_pressed[pygame.K_p]:
        for g in solution_path:
            pygame.draw.rect(WIN, GREEN, g.rect)

    for y in range(gridL, HEIGHT-gridL+1, gridL):
        for x in range(gridL, WIDTH-gridL+1, gridL):
            c = pygame.Rect(x-5, y-5, 10, 10)
            pygame.draw.rect(WIN, BLACK, c)

    for ws in walls:
        for w in ws:
            if w.erected:
                pygame.draw.rect(WIN, BLACK, w.rect)

    pygame.draw.rect(WIN, BLUE, p1)


# generates according do Depth First Search
# (after reaching a dead end, backtracks along the current corridor until an unvisited grid is found)
def DFS(colors, grids, walls, grid0, path):
    nc = 0
    complete = False
    while not complete:

        color = colors[nc]
        nc = (nc + 1) % len(colors)
        path = generate_corridor(grid0, grids, walls, path, color)
        print("new path: ", path)

        complete = True
        while len(PATH) != 0:
            g = PATH.pop()

            if len(check_moves(g, grids)) != 0:
                path = []
                print("found unvisited path: " + "(" + str(g.cords.row) + ", " + str(g.cords.col) + ")")
                grid0 = g
                complete = False
                break


# generates according to Hunt-and-Kill algorithm
# (after reaching a dead end, starts scanning from the first grids(top left) until it finds an unvisited grid)
def Hunt_and_Kill(colors, grids, walls, grid0, path):
    global PATHS
    p = []
    nc = 0
    complete = False
    while not complete:

        color = colors[nc]
        nc = (nc + 1) % len(colors)
        path = generate_corridor(grid0, grids, walls, path, color)
        print(path)
        PATHS.append(path)
        complete = True

        for g in grids:
            if not g.visited:
                complete = False
                path = []

                next_grid = grids[int(g.val-2)]
                print(f"found unvisited grid: ({g.cords.row}, {g.cords.col}), next path begins: ({next_grid.cords.row}, {next_grid.cords.col})")
                if next_grid.cords.row == g.cords.row:
                    grid0 = next_grid
                else:
                    grid0 = grids[int(g.val-1-ROW)]
                break


def generate_seed():
    return rd.randint(1, 100000)


# follows all possible paths recursively and stops if the exit grid(bottom right) is reached
def solve(grid0, grids):
    if grid0.val == ROW*COL:

        return str(grid0.val) + ""
    else:
        if len(grid0.neighbors) == 0:
            # print(f"grid at {grid0.cords.row}, {grid0.cords.col} is a dead end")
            return ""
        result = ""
        for g in grid0.neighbors:
            result += ", " + solve(g, grids)
        st = ""
        for s in result.split(", "):
            st += s
        if st == "":
            return ""
        else:
            return str(grid0.val) + result


def main():

    global PATH, solution_path
    seed = 0
    e = " "
    while not e.isnumeric() and e != "":
        e = input("seed(empty for random): ")
    if e == "":
        seed = generate_seed()
        print("seed: ", seed)
    else:
        seed = int(e)
    rd.seed(seed)

    WIN = pygame.display.set_mode(RES)
    pygame.display.set_caption("Maze")

    grids = []
    walls_x = []
    walls_y = []
    walls = []

    for y in range(gridL, HEIGHT-2*gridL+1, gridL):
        for x in range(gridL, WIDTH-2*gridL+1, gridL):
            gridr = pygame.Rect(x+1, y+1, gridL-2, gridL-2)
            grid = Grid(((y / gridL)-1) * ROW + x / gridL, Cords(y / gridL, x / gridL), gridr, False, WHITE, [])
            grids.append(grid)

    # walls on y-axis
    for y in range(gridL, HEIGHT - 2*gridL+1, gridL):
        for x in range(gridL, WIDTH - gridL+1, gridL):
            w = pygame.Rect(x-5, y+5, gridT, gridL-gridT)
            wall = Wall(Cords(y/gridL, x/gridL), True, w)
            walls_y.append(wall)

    # walls on y-axis
    for y in range(gridL, HEIGHT - gridL+1, gridL):
        for x in range(gridL, WIDTH - 2*gridL+1, gridL):
            w = pygame.Rect(x+5, y-5, gridL-gridT, gridT)
            wall = Wall(Cords(y / gridL, x / gridL), True, w)
            walls_x.append(wall)

    walls.append(walls_x)
    walls.append(walls_y)

    grid0 = grids[0]
    path = [(1.0, 1.0)]
    grid0.color = GREEN
    colors = (GREEN, YELLOW, MAGENTA, ORANGE, BLUE)

    if inp == 1:
        DFS(colors, grids, walls, grid0, path)
    else:
        Hunt_and_Kill(colors, grids, walls, grid0, path)

    solution_grids = solve(grids[0], grids).split(", ")
    for grid in solution_grids:
        if grid != "":
            solution_path.append(grids[int(float(grid))-1])
    print("\nPress p for solution")
    print("\nPress x for branch view\n(shows you how the corridors formed)")
    p1 = pygame.Rect(0, 0, pw, ph)
    walls[0][0].erected = walls[0][-1].erected = False


    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        # basic movement
        if keys_pressed[pygame.K_w] and p1.y - VEL >= 0:
            p1.y -= VEL
        if keys_pressed[pygame.K_a] and p1.x - VEL >= 0:
            p1.x -= VEL
        if keys_pressed[pygame.K_s] and p1.y + VEL + ph <= HEIGHT:
            p1.y += VEL
        if keys_pressed[pygame.K_d] and p1.x + VEL + pw <= WIDTH:
            p1.x += VEL

        draw_window(p1, keys_pressed, grids, walls, WIN)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()