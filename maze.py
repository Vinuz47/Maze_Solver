import pygame
import random
import time
from heapq import heappop, heappush

# Initialize Pygame
pygame.init()

# Grid parameters
CELL_SIZE = 30
GRID_WIDTH = 16  # Number of cells horizontally
GRID_HEIGHT = 16  # Number of cells vertically
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Showing Maze")

# Initialize grid with walls as edges
maze = [
    [{"N": True, "S": True, "E": True, "W": True} for _ in range(GRID_WIDTH)]
    for _ in range(GRID_HEIGHT)
]


# Draw the maze
def draw_maze():
    screen.fill(WHITE)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = maze[y][x]

            # Top wall
            if cell["N"]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x * CELL_SIZE, y * CELL_SIZE),
                    ((x + 1) * CELL_SIZE, y * CELL_SIZE),
                    2,
                )
            # Bottom wall
            if cell["S"]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x * CELL_SIZE, (y + 1) * CELL_SIZE),
                    ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE),
                    2,
                )
            # Left wall
            if cell["W"]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    (x * CELL_SIZE, y * CELL_SIZE),
                    (x * CELL_SIZE, (y + 1) * CELL_SIZE),
                    2,
                )
            # Right wall
            if cell["E"]:
                pygame.draw.line(
                    screen,
                    BLACK,
                    ((x + 1) * CELL_SIZE, y * CELL_SIZE),
                    ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE),
                    2,
                )


# Maze generation using recursive backtracking
def generate_maze():
    directions = {
        "N": (-1, 0, "S"),
        "S": (1, 0, "N"),
        "E": (0, 1, "W"),
        "W": (0, -1, "E"),
    }
    visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def is_valid(nx, ny):
        return 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and not visited[nx][ny]

    def carve_path(x, y):
        visited[x][y] = True
        dir_keys = list(directions.keys())
        random.shuffle(dir_keys)

        for direction in dir_keys:
            dx, dy, opposite = directions[direction]
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                maze[x][y][direction] = False
                maze[nx][ny][opposite] = False
                carve_path(nx, ny)

    carve_path(0, 0)

# Dijkstra's Algorithm
def dijkstra_visualized(start, end):
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
    priority_queue = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while priority_queue:
        current_cost, current = heappop(priority_queue)
        x, y = current
        pygame.draw.circle(screen, BLUE, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), 5)
        pygame.display.update()
        time.sleep(0.1)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and not maze[x][y][direction]:
                new_cost = current_cost + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    heappush(priority_queue, (new_cost, (nx, ny)))
                    came_from[(nx, ny)] = current

    return []

# Breadth-First Search (BFS)
def bfs_visualized(start, end):
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
    queue = [start]
    came_from = {start: None}

    while queue:
        current = queue.pop(0)
        x, y = current
        pygame.draw.circle(screen, BLUE, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), 5)
        pygame.display.update()
        time.sleep(0.1)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and not maze[x][y][direction] and (nx, ny) not in came_from:
                queue.append((nx, ny))
                came_from[(nx, ny)] = current

    return []

# A* Algorithm with step-by-step visualization
def a_star_visualized(start, end):
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current_cost, current = heappop(open_set)
        x, y = current

        # Highlight the node being explored
        pygame.draw.circle(
            screen,
            BLUE,
            (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2),
            5
        )
        pygame.display.update()
        time.sleep(0.1)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for direction, (dx, dy) in directions.items():
            nx, ny = x + dx, y + dy

            # Check if the move is valid
            if (
                0 <= nx < GRID_HEIGHT
                and 0 <= ny < GRID_WIDTH
                and not maze[x][y][direction]
            ):
                new_cost = current_cost + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), end)
                    heappush(open_set, (priority, new_cost, (nx, ny)))
                    came_from[(nx, ny)] = current

    return []


# Main loop
generate_maze()
running = True
start = (0, 0)
end = (GRID_HEIGHT - 1, GRID_WIDTH - 1)

while running:
    draw_maze()

    # Highlight start and end points
    pygame.draw.circle(
        screen,
        GREEN,
        (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2),
        10,
    )
    pygame.draw.circle(
        screen,
        RED,
        (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2),
        10,
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: # Press 'A' for A*
                pygame.display.set_caption("A* Algorithm Visualization")
                path = a_star_visualized(start, end)
            elif event.key == pygame.K_2:  # Press 'B' for BFS
                pygame.display.set_caption("BFS Algorithm Visualization")
                path = bfs_visualized(start, end)
            elif event.key == pygame.K_3:  # Press 'D' for Dijkstra
                pygame.display.set_caption("Dijkstra Algorithm Visualization")
                path = dijkstra_visualized(start, end)
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit() # Press 'Q' or 'ESC' to quit

            # Highlight the final path
            # for px, py in path:
            #         pygame.draw.circle(
            #             screen,
            #             YELLOW,
            #             (
            #                 py * CELL_SIZE + CELL_SIZE // 2,
            #                 px * CELL_SIZE + CELL_SIZE // 2,
            #             ),
            #             5,
            #         )
            #         pygame.display.update()
            #         time.sleep(0.1)

            # Visualize the path on the maze using lines
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]
                pygame.draw.line(
                    screen,
                    GREEN,  # Path color
                    (y1 * CELL_SIZE + CELL_SIZE // 2, x1 * CELL_SIZE + CELL_SIZE // 2),
                    (y2 * CELL_SIZE + CELL_SIZE // 2, x2 * CELL_SIZE + CELL_SIZE // 2),
                    3,  # Line thickness
                )
                pygame.display.update()
                time.sleep(0.05)  # Delay for gradual visualization

    pygame.display.update()

pygame.quit()