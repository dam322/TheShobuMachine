import pygame

from models.board import Board


def main():
    pygame.init()
    pygame.display.set_caption("The Shobu Machine")
    piece_size = 64
    space_between_boards = 40
    padding = 30
    temp_to_center = 20

    screen = pygame.display.set_mode((8 * piece_size + space_between_boards + 2 * padding,
                                      8 * piece_size + space_between_boards + 2 * padding))
    clock = pygame.time.Clock()

    board1 = Board(padding,
                   padding,
                   piece_size, temp_to_center)
    board2 = Board(padding + piece_size * 4 + space_between_boards,
                   padding,
                   piece_size, temp_to_center)
    board3 = Board(padding,
                   padding + piece_size * 4 + space_between_boards,
                   piece_size, temp_to_center)
    board4 = Board(padding + piece_size * 4 + space_between_boards,
                   padding + piece_size * 4 + space_between_boards,
                   piece_size, temp_to_center)

    boards = [board1, board2, board3, board4]
    running = True
    turn = True

    while running:
        # Capturar eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click derecho
                    mx, my = pygame.mouse.get_pos()
                    mouse_rect = pygame.Rect(mx, my, 1, 1)
                    board = mouse_collide(mouse_rect, boards)
                    if board is not None:
                        player = 1 if turn else 2

                        x, y = get_first_click_mouse(mouse_rect, board, player)

                        if x == -1:
                            break
                        print("fuera ", x, y)
                        clicked = False
                        while not clicked:
                            event = pygame.event.wait()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mx, my = pygame.mouse.get_pos()
                                mouse_rect = pygame.Rect(mx, my, 1, 1)

                                x_1, y_1 = get_move_mouse(mouse_rect, board)
                                if x_1 == -2:
                                    continue

                                print("dentro ", x_1, y_1)
                                if x_1 == x and y_1 == y:
                                    print("son las mismas")
                                else:
                                    print("no son las mismas")
                                    clicked = True
                                    turn = not turn
        update(boards)
        draw(screen, boards, piece_size, turn)
        clock.tick(60)


def get_first_click_mouse(mouse_rect, board, player):
    for y in range(4):
        for x in range(4):
            if mouse_rect.colliderect(board.map[y][x].rect) and board.map[y][x].value == player:
                return x, y
    return -1, -1


def get_move_mouse(mouse_rect, board):
    for y in range(4):
        for x in range(4):
            if mouse_rect.colliderect(board.map[y][x].rect):
                return x, y
    return -2, -2


def mouse_collide(mouse_rect, boards):
    for x in boards:
        if mouse_rect.colliderect(x):
            return x
    return None


def draw(screen, boards, piece_size, turn):
    # Fondo
    # screen.fill((38, 163, 144))
    if turn:
        screen.fill((255, 255, 255))
    else:
        screen.fill((0, 0, 0))

    for board in boards:
        draw_board(screen, piece_size, board)


def draw_board(screen, piece_size, board):
    temp_line = 4
    board.draw(screen, piece_size, temp_line)


def update(boards):
    for board in boards:
        board.update()

    pygame.display.update()


if __name__ == "__main__":
    main()
