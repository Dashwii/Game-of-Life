import pygame

WIDTH, HEIGHT = 1000, 1000
ROWS, COLS, = 40, 40
FPS = 60
CELL_FPS = 8
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)


def main():
    matrix = [[0 for col in range(COLS)] for row in range(ROWS)]
    clock = pygame.time.Clock()
    mouse_down = False
    cells_moving = False

    while True:
        if cells_moving:
            clock.tick(CELL_FPS)
        else:
            clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        if mouse_down:
            square = (mouse_pos[0] // 25, mouse_pos[1] // 25)
            matrix[square[0]][square[1]] = 1
        if keys_pressed[pygame.K_SPACE]:
            print("Cells moving")
            cells_moving = True
        if keys_pressed[pygame.K_d]:
            print("Draw mode")
            cells_moving = False
        if keys_pressed[pygame.K_ESCAPE] and not cells_moving:
            print("Board erased")
            matrix = [[0 for col in range(COLS)] for row in range(ROWS)]
        if cells_moving:
            determine_alive_cell(matrix)

        draw_board(matrix)


def determine_alive_cell(matrix):
    # Any live cell with two or three live neighbors lives
    # Any dead cell with three live neighbors becomes a live cell.
    # All other live cells die on next generation. All other dead cells stay dead.

    for i_row, row in enumerate(matrix):
        for j_col, column in enumerate(matrix[i_row]):
            current_cell = matrix[i_row][j_col]
            surrounding = ((i_row - 1, j_col - 1), (i_row - 1, j_col), (i_row - 1, j_col + 1),
                           (i_row, j_col - 1),                          (i_row, j_col + 1),
                           (i_row + 1, j_col - 1), (i_row + 1, j_col), (i_row + 1, j_col + 1))
            neighbor_count = 0
            for neighbor in surrounding:
                if 0 <= neighbor[0] < len(matrix) and 0 <= neighbor[1] < len(matrix[0]):
                    if matrix[neighbor[0]][neighbor[1]] == 1:
                        neighbor_count += 1

            if current_cell == 1 and neighbor_count in (2, 3):
                continue
            elif current_cell == 0 and neighbor_count == 3:
                matrix[i_row][j_col] = 1
            else:
                matrix[i_row][j_col] = 0


def draw_board(matrix):
    WINDOW.fill(WHITE)
    for i, column in enumerate(matrix):
        pygame.draw.line(WINDOW, GRAY, ((i + 1) * 25, 0), ((i + 1) * 25, HEIGHT), width=1)
        for j, row in enumerate(column):
            pygame.draw.line(WINDOW, GRAY, (0, (j + 1) * 25), (WIDTH, (j + 1) * 25), width=1)
            # Draw alive cells
            if matrix[i][j] == 1:
                pygame.draw.rect(WINDOW, BLACK, (i * 25, j * 25, 25, 25))

    pygame.display.update()


main()
