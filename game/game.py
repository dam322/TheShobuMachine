import pygame

from models.board import Board


def main():
    pygame.init()
    pygame.display.set_caption("The Shobu Machine")
    pieces_size = 64
    space_between_boards = 40
    padding = 30
    screen = pygame.display.set_mode((8 * pieces_size + space_between_boards + 2 * padding,
                                      8 * pieces_size + space_between_boards + 2 * padding))
    clock = pygame.time.Clock()
    board1 = Board()
    board2 = Board()
    board3 = Board()
    board4 = Board()
    running = True

    while running:
        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update(clock)
        draw(screen, board1, board2, board3, board4, padding, space_between_boards, pieces_size)
        clock.tick(3)


def draw(screen, board1, board2, board3, board4, padding, space_between_boards, pieces_size):
    # Fondo
    screen.fill((38, 163, 144))

    # Dibujar tablero 1
    draw_board(padding, padding, screen, pieces_size, board1)
    # Dibujar tablero 2
    draw_board(padding + pieces_size * 4 + space_between_boards, padding, screen, pieces_size, board2)
    # Dibujar tablero 3
    draw_board(padding, padding + pieces_size * 4 + space_between_boards, screen, pieces_size, board3)
    # Dibujar tablero 4
    draw_board(padding + pieces_size * 4 + space_between_boards, padding + pieces_size * 4 + space_between_boards,
               screen, pieces_size, board4)


def draw_board(init_x, init_y, screen, pieces_size, board):
    pygame.draw.rect(screen, (0, 0, 155), pygame.Rect(init_x, init_y, pieces_size * 4, pieces_size * 4))

    temp_to_center = 20
    for y in range(4):
        for x in range(4):
            if board.map[y][x] == 1:
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(init_x + x * pieces_size + temp_to_center / 2,
                                                                      init_y + y * pieces_size + temp_to_center / 2,
                                                                      pieces_size - temp_to_center,
                                                                      pieces_size - temp_to_center))
            elif board.map[y][x] == 2:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(init_x + x * pieces_size + temp_to_center / 2,
                                                                init_y + y * pieces_size + temp_to_center / 2,
                                                                pieces_size - temp_to_center,
                                                                pieces_size - temp_to_center))


def update(clock):
    pygame.display.update()


if __name__ == "__main__":
    main()
