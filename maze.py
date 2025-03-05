import pygame
import cv2
import numpy as np
from heapq import heappop, heappush
import time

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20  # Adjust according to maze image resolution
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load maze image and preprocess
def load_maze(image_path):
    # Load the image and convert it to grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binary (0 for walls, 1 for paths)
    _, binary_maze = cv2.threshold(img, 128, 1, cv2.THRESH_BINARY_INV)

    # Resize the binary maze for visualization
    binary_maze = cv2.resize(binary_maze, (binary_maze.shape[0]//10, binary_maze.shape[1]//10))

    return binary_maze

# Draw the maze on Pygame screen
def draw_maze(maze, screen):
    rows, cols = maze.shape
    for x in range(rows):
        for y in range(cols):
            color = WHITE if maze[x, y] == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# A* Pathfinding
def a_star(maze, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        _, current_cost, current = heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 1:
                new_cost = current_cost + 1
                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    priority = new_cost + heuristic((nx, ny), end)
                    heappush(open_set, (priority, new_cost, (nx, ny)))
                    came_from[(nx, ny)] = current

    return []

# Visualize the path
def visualize_path(path, screen):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        pygame.draw.line(
            screen,
            GREEN,
            (y1 * CELL_SIZE + CELL_SIZE // 2, x1 * CELL_SIZE + CELL_SIZE // 2),
            (y2 * CELL_SIZE + CELL_SIZE // 2, x2 * CELL_SIZE + CELL_SIZE // 2),
            3,
        )
        pygame.display.update()
        time.sleep(0.05)

# Main Function
def main():
    # Load maze and initialize screen
    maze = load_maze("maze3.jpg")  # Replace with your maze image path
    rows, cols = maze.shape
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Maze Pathfinding")

    start = (0, 0)
    end = (rows - 1, cols - 1)

    running = True
    while running:
        draw_maze(maze, screen)

        # Draw start and end points
        pygame.draw.circle(screen, GREEN, (start[1] * CELL_SIZE + CELL_SIZE // 2, start[0] * CELL_SIZE + CELL_SIZE // 2), 10)
        pygame.draw.circle(screen, RED, (end[1] * CELL_SIZE + CELL_SIZE // 2, end[0] * CELL_SIZE + CELL_SIZE // 2), 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to find path
                    path = a_star(maze, start, end)
                    visualize_path(path, screen)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
