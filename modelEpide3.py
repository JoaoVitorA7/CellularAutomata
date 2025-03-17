import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros da simulação
grid_size = 100
beta_0 = 0.1
gamma = 0.02
mu = 0.01
mobility = 0.02
vaccination_prob = 0.01
steps = 200
risk_factor = 2.0  # Aumento da taxa de infecção em zonas de risco
num_risk_zones = 3  # Número de zonas de risco
zone_radius = 10  # Raio das zonas de risco

# Inicializa a grade e zonas de risco
grid = np.zeros((grid_size, grid_size), dtype=int)
risk_zones = np.zeros((grid_size, grid_size), dtype=bool)  # Agora é uma matriz booleana

# Define zonas de risco aleatórias
for _ in range(num_risk_zones):
    center_x, center_y = np.random.randint(zone_radius, grid_size - zone_radius, size=2)
    for x in range(grid_size):
        for y in range(grid_size):
            if np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) <= zone_radius:
                risk_zones[x, y] = True  # Marca como zona de risco

# Define o local inicial da infecção
origin_x, origin_y = np.random.randint(0, grid_size, size=2)
grid[origin_x, origin_y] = 1

def fractal_density(x, y, grid):
    scales = np.array([1, 2, 4])
    infected_counts = np.array([np.count_nonzero(grid[max(0, x - r):min(grid_size, x + r + 1), max(0, y - r):min(grid_size, y + r + 1)] == 1) for r in scales])
    valid = infected_counts > 0
    if np.sum(valid) > 1:
        D = np.polyfit(np.log(scales[valid]), np.log(infected_counts[valid]), 1)[0]
        return max(D, 0.1)
    return 0.1

def update(grid):
    new_grid = grid.copy()
    for x in range(grid_size):
        for y in range(grid_size):
            if new_grid[x, y] in [0, 4]:  # Suscetível ou Vacinado
                beta = beta_0 * fractal_density(x, y, new_grid)
                if risk_zones[x, y]:  # Usa a matriz booleana para evitar conflito
                    beta *= risk_factor  # Aumenta beta nas zonas de risco
                if new_grid[x, y] == 4:
                    beta *= 0.2  # Reduz risco para vacinados
                if np.any(new_grid[max(0, x-1):min(grid_size, x+2), max(0, y-1):min(grid_size, y+2)] == 1):
                    if np.random.rand() < beta:
                        new_grid[x, y] = 1
                elif new_grid[x, y] == 0 and np.random.rand() < vaccination_prob:
                    new_grid[x, y] = 4  # Vacinação
            elif new_grid[x, y] == 1:
                if np.random.rand() < mu:
                    new_grid[x, y] = 3
                elif np.random.rand() < gamma:
                    new_grid[x, y] = 2
    for _ in range(int(grid_size * grid_size * mobility)):
        x1, y1, x2, y2 = np.random.randint(0, grid_size, size=4)
        if new_grid[x1, y1] in [0, 1, 2, 4] and new_grid[x2, y2] in [0, 1, 2, 4]:
            new_grid[x1, y1], new_grid[x2, y2] = new_grid[x2, y2], new_grid[x1, y1]
    return new_grid

fig, ax = plt.subplots()
cmap = plt.cm.colors.ListedColormap(["green", "red", "blue", "black", "yellow"])
def update_func(frame):
    global grid
    grid = update(grid)
    ax.clear()
    ax.imshow(grid, cmap=cmap, interpolation='none')
    ax.set_title(f"Iteração: {frame+1}")
    ax.axis('off')
ani = FuncAnimation(fig, update_func, frames=steps, interval=100, repeat=False)
plt.show()
