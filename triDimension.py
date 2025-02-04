import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Função para contar vizinhos vivos
def count_neighbors(grid, x, y, z):
    neighbors = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue  # Ignorar a célula central
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and 0 <= nz < grid.shape[2]:
                    neighbors += grid[nx, ny, nz]
    return neighbors

# Função para atualizar o estado do autômato
def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            for z in range(grid.shape[2]):
                neighbors = count_neighbors(grid, x, y, z)
                if grid[x, y, z] == 1:
                    # Célula viva: sobrevive com 2 ou 3 vizinhos
                    if neighbors in [2, 3]:
                        new_grid[x, y, z] = 1
                else:
                    # Célula morta: nasce com exatamente 3 vizinhos
                    if neighbors == 3:
                        new_grid[x, y, z] = 1
    return new_grid

# Função para visualizar o autômato em 3D
def plot_automaton(grid):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = np.where(grid == 1)  # Coordenadas das células vivas
    ax.scatter(x, y, z, c='blue', label='Células Vivas')

    ax.set_xlim(0, grid.shape[0])
    ax.set_ylim(0, grid.shape[1])
    ax.set_zlim(0, grid.shape[2])
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Jogo da Vida 3D')
    plt.show()

# Configuração inicial
def run_game_of_life_3d(size=10, generations=10):
    # Criar uma grade inicial aleatória
    grid = np.random.choice([0, 1], size=(size, size, size), p=[0.8, 0.2])

    for gen in range(generations):
        print(f"Generation {gen + 1}")
        plot_automaton(grid)
        grid = update_grid(grid)

# Executar o jogo da vida em 3D
run_game_of_life_3d(size=10, generations=5)