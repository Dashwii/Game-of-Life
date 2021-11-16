import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
BLUE = (0, 14, 71)
cell_size = 13
cell_number = 100
FPS = 60
SCREEN = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))




def draw_grid(grid, grid_overlay):
    SCREEN.fill(WHITE)
    for y in range(cell_number):
        for x in range(cell_number):
            # Flip y and x to give correct filled square
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            if grid[x][y] == 1:
                pygame.draw.rect(SCREEN, BLUE, rect, 0)
    # Grid
    if grid_overlay:
        for y in range(cell_number):
            for x in range(cell_number):
                # Flip y and x to give correct filled square
                rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
    pygame.display.update()


def get_neighbors(curr_cell, grid):
    row_x, col_y = curr_cell[0], curr_cell[1]
    neighbor_count = 0
    neighbors = ([row_x - 1, col_y - 1], [row_x - 1, col_y], [row_x - 1, col_y + 1],
                 [row_x, col_y - 1],                           [row_x, col_y + 1],
                 [row_x + 1, col_y - 1], [row_x + 1, col_y], [row_x + 1, col_y + 1])
    for neighbor in neighbors:
        if neighbor[0] < 0:
            neighbor[0] = len(grid) - 1
        elif neighbor[0] >= len(grid):
            neighbor[0] = 0
        if neighbor[1] < 0:
            neighbor[1] = len(grid) - 1
        elif neighbor[1] >= len(grid):
            neighbor[1] = 0
        if grid[neighbor[0]][neighbor[1]] == 1:
            neighbor_count += 1
    return neighbor_count


def conway(cell_state, neighbor_count):
    # Will return 1 or 0 based on conway game of life rules if the cell is alive or dead respectively
    if cell_state == 1 and neighbor_count in (2, 3):
        return 1
    elif cell_state == 0 and neighbor_count == 3:
        return 1
    else:
        return 0


def return_new_grid(grid):
    new_grid = [[0] * len(row) for row in grid]
    for ix, row in enumerate(grid):
        for iy, column in enumerate(row):
            neighbor_count = get_neighbors((ix, iy), grid)
            alive_or_dead = conway(grid[ix][iy], neighbor_count)
            new_grid[ix][iy] = alive_or_dead
    return new_grid


def main():
    generation_speed = 150
    NEXT_GENERATION = pygame.USEREVENT
    pygame.time.set_timer(NEXT_GENERATION, generation_speed)

    clock = pygame.time.Clock()
    grid = [[random.randint(0, 1) for _ in range(cell_number)] for _ in range(cell_number)]
    draw_mode = False
    grid_overlay = False
    left_mb_held = False
    right_mb_held = False
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == NEXT_GENERATION and not draw_mode:
                grid = return_new_grid(grid)

            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_g]:
                    if not grid_overlay:
                        grid_overlay = True
                        print("Grid overlay on")
                    else:
                        grid_overlay = False
                        print("Grid overlay off")

                if keys[pygame.K_d]:
                    if not draw_mode:
                        draw_mode = True
                        print("Draw mode enabled")
                    else:
                        draw_mode = False
                        print("Draw mode disabled")

                if keys[pygame.K_c] and draw_mode:
                    grid = [[0 for _ in range(cell_number)] for _ in range(cell_number)]
                    print("Board cleared")

                if keys[pygame.K_r]:
                    grid = [[random.randint(0, 1) for _ in range(cell_number)] for _ in range(cell_number)]
                    print("Randomized")

                if keys[pygame.K_LEFT]:
                    if generation_speed - 50 != 0:
                        generation_speed -= 50
                        pygame.time.set_timer(NEXT_GENERATION, generation_speed)
                        print(f"Speed: New gen every {generation_speed}ms")

                if keys[pygame.K_RIGHT]:
                    generation_speed += 50
                    pygame.time.set_timer(NEXT_GENERATION, generation_speed)
                    print(f"Speed: New gen every {generation_speed}ms")

            if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is pressed and continuously held the game will draw until the mouse is released
                if event.button == 1:
                    left_mb_held = True
                elif event.button == 3:
                    right_mb_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_mb_held = False
                elif event.button == 3:
                    right_mb_held = False

        if left_mb_held and draw_mode:  # Left click add square
            mouse = pygame.mouse.get_pos()
            square = mouse[0] // cell_size, mouse[1] // cell_size
            grid[square[1]][square[0]] = 1
        elif right_mb_held and draw_mode:  # Right click remove square
            mouse = pygame.mouse.get_pos()
            square = mouse[0] // cell_size, mouse[1] // cell_size
            grid[square[1]][square[0]] = 0

        draw_grid(grid, grid_overlay)


main()
