import numpy as np
import matplotlib.pyplot as plt
import time

def create_grid(rows, cols):
    return np.random.randint(2, size=(rows, cols))

def count_neighbors(grid, x, y):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
            count += grid[nx, ny]
    return count

def update_grid(grid):
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and neighbors == 3:
                new_grid[x, y] = 1
    return new_grid

# Inicialização
rows, cols = 20, 20
grid = create_grid(rows, cols)

# Simulação
for _ in range(30):
    plt.imshow(grid, cmap='binary')
    plt.pause(0.1)
    grid = update_grid(grid)
