import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros da simulação
grid_size = 100  # Tamanho da grade
infection_time = 30  # Tempo médio de infecção antes da recuperação
beta_0 = 0.05  # Taxa de infecção base
gamma = 0.02  # Taxa de recuperação
mu = 0.01  # Taxa de mortalidade
steps = 300  # Número de iterações

# Estados: 0 = Suscetível, 1 = Infectado, 2 = Recuperado, 3 = Morto
grid = np.zeros((grid_size, grid_size), dtype=int)

# Inicializa um infectado no centro
grid[grid_size // 2, grid_size // 2] = 1

def fractal_density(x, y, grid):
    """ Calcula a densidade fractal local de infectados """
    scales = [1, 2, 4]
    infected_counts = []
    for r in scales:
        x_min, x_max = max(0, x - r), min(grid_size, x + r + 1)
        y_min, y_max = max(0, y - r), min(grid_size, y + r + 1)
        neighborhood = grid[x_min:x_max, y_min:y_max]
        infected_counts.append(np.count_nonzero(neighborhood == 1))
    
    infected_counts = np.array(infected_counts)
    scales = np.array(scales)
    
    valid = infected_counts > 0
    if np.sum(valid) > 1:
        D = np.polyfit(np.log(scales[valid]), np.log(infected_counts[valid]), 1)[0]
        return max(D, 0.1)  # Evita D = 0
    return 0.1  # Valor mínimo para evitar beta = 0

def update(grid):
    """ Atualiza a grade conforme as regras do modelo """
    new_grid = grid.copy()
    
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x, y] == 0:  # Suscetível
                D = fractal_density(x, y, grid)
                beta = beta_0 * D
                if np.any(grid[max(0, x-1):min(grid_size, x+2), max(0, y-1):min(grid_size, y+2)] == 1):
                    if np.random.rand() < beta:
                        new_grid[x, y] = 1  # Infecta a célula
            elif grid[x, y] == 1:  # Infectado
                if np.random.rand() < mu:
                    new_grid[x, y] = 3  # Morte da célula
                elif np.random.rand() < gamma:
                    new_grid[x, y] = 2  # Recupera a célula
    
    return new_grid

# Animação da simulação
fig, ax = plt.subplots()
ims = []
cmap = plt.cm.colors.ListedColormap(["green", "red", "blue", "black"])
for _ in range(steps):
    im = ax.imshow(grid, cmap=cmap, animated=True)
    ims.append([im])
    grid = update(grid)

ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True)
plt.show()
