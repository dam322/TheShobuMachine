import pygame

from models.board import Board


def main():
    pygame.init()
    pygame.display.set_caption("The Shobu Machine")
    # Tamaño de las piezas
    piece_size = 64
    # Espacio entre los trableros
    space_between_boards = 40
    # Distancia entre el borde la pantalla y los tableros
    padding = 30
    # Distancia para centrar las piezas y que no ocupen el espacio del tablero
    temp_to_center = 20

    # Calcular el tamaño de la pantalla
    screen = pygame.display.set_mode((8 * piece_size + space_between_boards + 2 * padding,
                                      8 * piece_size + space_between_boards + 2 * padding))
    # Reloj auxiliar
    clock = pygame.time.Clock()

    # Iniciar los 4 tableros
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

    # Turno del jugador blano
    turn = True
    pieces_to_highligth = []
    # Bucle del juego
    while running:
        # Capturar eventos
        for event in pygame.event.get():
            # Terminar el proceso cuando se cierre la ventana
            if event.type == pygame.QUIT:
                running = False
            # Evento del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click izquierdo
                if event.button == 1:
                    # Capturar la posición del mouse, crear un rectangulo y verificar en cual tablero hizo click
                    mx, my = pygame.mouse.get_pos()
                    mouse_rect = pygame.Rect(mx, my, 1, 1)
                    board = mouse_collide(mouse_rect, boards)

                    if board is None:
                        continue

                    player = 1 if turn else 2
                    piece_to_move = get_piece_coordinates_clicked(mouse_rect, board, player)
                    # Si clickeó en una ficha que no sea del jugador actual no debe hacer nada
                    if piece_to_move is None:
                        break
                    coordinates = []

                    for line in board.map:
                        for piece in line:
                            if (piece.x, piece.y) in piece_to_move.valid_moves \
                                    and (piece.value != player):
                                pieces_to_highligth.append(piece)
                                coordinates.append((piece.x, piece.y))

                    draw_highlights(screen, pieces_to_highligth)
                    pygame.display.update()
                    clicked = False
                    while not clicked:
                        # Esperar al siguiente click para hacer el movimiento
                        event = pygame.event.wait()
                        # Si el evento no es un click entonces debe esperar al siguiente evento
                        if event.type != pygame.MOUSEBUTTONDOWN:
                            continue

                        mx, my = pygame.mouse.get_pos()
                        mouse_rect = pygame.Rect(mx, my, 1, 1)

                        # Verificar que sea un movimiento válido
                        piece_where_is_moved = get_next_piece_coordinates_clicked(mouse_rect, board)

                        # Verificar que clickee en una ficha del mismo tablero
                        if piece_where_is_moved is None:
                            print("Click en ficha equivocada")
                            continue
                        # Verificar que la ficha clickeada no sea la misma que esocgió al principio
                        if piece_to_move.get_coordinates() == piece_where_is_moved.get_coordinates():
                            print("Es la misma ficha")
                            continue

                        # Si la posición no está en los movimientos válidos entonces no haga nada
                        if piece_where_is_moved.get_coordinates() not in coordinates:
                            print("Coordenada incorrecta: ", piece_where_is_moved.get_coordinates(), coordinates)
                            continue

                        piece_to_move.move(piece_where_is_moved)
                        clicked = True
                        turn = not turn
                        pieces_to_highligth = []
        update(boards)
        draw(screen, boards, piece_size, turn, pieces_to_highligth)
        clock.tick(60)


# Obtiene la coordenada del primer movimiento
def get_piece_coordinates_clicked(mouse_rect, board, player):
    for y in range(4):
        for x in range(4):
            if mouse_rect.colliderect(board.map[y][x].rect) and board.map[y][x].value == player:
                return board.map[y][x]
    return None


# Obtiene la coordenada del movimiento hacia donde quiere moverse
def get_next_piece_coordinates_clicked(mouse_rect, board):
    for y in range(4):
        for x in range(4):
            if mouse_rect.colliderect(board.map[y][x].rect):
                return board.map[y][x]
    return None


# Obtiene el tablero donde dió click el jugador
def mouse_collide(mouse_rect, boards):
    for x in boards:
        if mouse_rect.colliderect(x):
            return x
    return None


# Dibujar todos los elementos del mapa
def draw(screen, boards, piece_size, turn, coordinates):
    # Fondo
    # screen.fill((38, 163, 144))
    if turn:
        screen.fill((255, 255, 255))
    else:
        screen.fill((0, 0, 0))

    for board in boards:
        draw_board(screen, piece_size, board)

    draw_highlights(screen, coordinates)


# Dibujar el tablero y sus elementos
def draw_board(screen, piece_size, board):
    temp_line = 4
    board.draw(screen, piece_size, temp_line)


# TODO Recfatorizar este comentario: Dibujar en gris las fichas que cumplan
def draw_highlights(screen, coordinates):
    for piece in coordinates:
        piece.draw_highlight(screen)


# Actualiza el tablero y sus elementos
def update(boards):
    for board in boards:
        board.update()

    pygame.display.update()


if __name__ == "__main__":
    main()
