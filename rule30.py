import numpy as np
import matplotlib.pyplot as plt

def rule_30(current_gen):
    """Aplica a regra 30 a uma geração atual."""
    next_gen = np.zeros_like(current_gen)
    for i in range(1, len(current_gen) - 1):
        left, center, right = current_gen[i - 1], current_gen[i], current_gen[i + 1]
        # Determinar o estado da próxima célula com base na regra 30
        next_gen[i] = 1 if (left == 1 and center == 0 and right == 0) or \
                          (left == 0 and center == 1 and right == 1) or \
                          (left == 0 and center == 1 and right == 0) or \
                          (left == 0 and center == 0 and right == 1) else 0
    return next_gen

def generate_rule_30(steps, size):
    """Gera uma matriz com as gerações da Rule 30."""
    grid = np.zeros((steps, size), dtype=int)
    grid[0, size // 2] = 1  # Ponto inicial no centro
    for step in range(1, steps):
        grid[step] = rule_30(grid[step - 1])
    return grid

def visualize_rule_30(grid):
    """Visualiza o autômato celular."""
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap="binary", interpolation="nearest")
    plt.title("Rule 30")
    plt.axis("off")
    plt.show()

# Configuração
steps = 50  # Número de gerações
size = 101  # Tamanho da linha

# Gerar e visualizar
grid = generate_rule_30(steps, size)
visualize_rule_30(grid)
