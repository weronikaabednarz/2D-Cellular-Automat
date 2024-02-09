import pygame
import numpy as np
import random

# Parametry planszy
board_height = 20  # Wysokość planszy (liczba wierszy)
board_width = 30  # Szerokość planszy (liczba kolumn)
cell_size = 20    # Rozmiar komórki w pikselach

# Kolory
white = (255, 255, 255)  # Kolor biały (RGB)
black = (0, 0, 0)        # Kolor czarny (RGB)

def create_empty_board():
    return np.zeros((board_height, board_width), dtype=int)     #pusta uzupelniana nowymi stanami po krokach czasowych
    
def calculate_neighbors(matrix, x, y, boundary_type):
    alive = 0
    ROWS = len(matrix)
    COLS = len(matrix[0])

    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i == 0 and j == 0:
                continue

            if boundary_type == "periodic":
                neighbor_row = (y + i) % ROWS
                neighbor_col = (x + j) % COLS
                alive += matrix[neighbor_row][neighbor_col]
            elif boundary_type == "reflecting":
                neighbor_row = max(0, min(y + i, ROWS - 1))
                neighbor_col = max(0, min(x + j, COLS - 1))
                alive += matrix[neighbor_row][neighbor_col]
            elif boundary_type == "absorbing":
                neighbor_row = y + i
                neighbor_col = x + j
                if neighbor_row >= 0 and neighbor_row < ROWS and neighbor_col >= 0 and neighbor_col < COLS:
                    alive += matrix[neighbor_row][neighbor_col]


    return alive


def apply_rules(matrix, new_matrix, boundary_type):
    for i in range(board_width):
        for j in range(board_height):
            alive_neighbors = calculate_neighbors(matrix, i, j, boundary_type)
            if matrix[j][i] == 1:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    new_matrix[j][i] = 1
            elif matrix[j][i] == 0:
                if alive_neighbors == 3:
                    new_matrix[j][i] = 1
                    
def glider(matrix, x, y):
    matrix[0 + y][1 + x] = 1
    matrix[0 + y][2 + x] = 1
    matrix[1 + y][0 + x] = 1
    matrix[1 + y][1 + x] = 1
    matrix[2 + y][2 + x] = 1
    
def oscilator(matrix, x, y):
    matrix[0 + y][1 + x] = 1
    matrix[1 + y][1 + x] = 1
    matrix[2 + y][1 + x] = 1
    
def stationary(matrix, x, y):
    matrix[0 + y][1 + x] = 1
    matrix[0 + y][2 + x] = 1
    matrix[1 + y][0 + x] = 1
    matrix[1 + y][3 + x] = 1
    matrix[2 + y][1 + x] = 1
    matrix[2 + y][2 + x] = 1
    
def random_state(matrix, x, y):
    for i in range(5):
        for j in range(5):
            matrix[j + y][i + x] = random.randint(0, 2)
            
def display_board(matrix, screen):
    for i in range(board_width):
        for j in range(board_height):
            if matrix[j][i] == 1:
                pygame.draw.rect(screen, black, (i * cell_size, j * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, white, (i * cell_size, j * cell_size, cell_size, cell_size))
    pygame.display.update()
    
def main():
    pygame.init()               #służy do zainicjowania zaimportowanych modułów gry z naszej biblioteki
    screen = pygame.display.set_mode((board_width * cell_size, board_height * cell_size))       # definiowanie okna gry
    pygame.display.set_caption("Gra w życie?")      # wyświetlenie okna gry

    board = create_empty_board()
    new_board = create_empty_board()
    boundary_type = "periodic"  # Warunek graniczny - periodyczny

    # Stan początkowy: Glider
    #glider(board, 5, 5)

    # Stan początkowy: Oscylator
    oscilator(board, 0, 0)

    # Stan początkowy: Niezmienny
    #stationary(board, 10, 0)

    # Stan początkowy: Losowy
    #random_state(board, 0, 0)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        apply_rules(board, new_board, boundary_type)
        board = new_board  # zamiana tablic

        display_board(board, screen)
        new_board = create_empty_board()
        pygame.time.delay(100)  
        clock.tick(10)  # Aktualizacja planszy co 10 klatek na sekundę
        
    pygame.quit()

if __name__ == "__main__":
    main()
