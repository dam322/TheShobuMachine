import pygame

from models.board import Board
from models.Player import Player
from models.piece import Piece


class Game:
    def __init__(self):
        # Tamaño de las piezas
        self.piece_size = 64
        # Espacio entre los trableros
        self.space_between_boards = 40
        # Distancia entre el borde la pantalla y los tableros
        self.padding = 30
        # Distancia para centrar las piezas y que no ocupen el espacio del tablero
        self.temp_to_center = 20

        # Calcular el tamaño de la pantalla
        self.screen = pygame.display.set_mode((8 * self.piece_size + self.space_between_boards + 2 * self.padding,
                                               8 * self.piece_size + self.space_between_boards + 2 * self.padding))
        # Reloj auxiliar
        self.clock = pygame.time.Clock()

        # Iniciar los 4 tableros
        self.board1 = Board(self.padding,
                            self.padding,
                            self.piece_size, self.temp_to_center, lado_agresivo="IZQUIERDA", lado_pasivo="SUPERIOR")
        self.board2 = Board(self.padding + self.piece_size * 4 + self.space_between_boards,
                            self.padding,
                            self.piece_size, self.temp_to_center, lado_agresivo="DERECHA", lado_pasivo="SUPERIOR")
        self.board3 = Board(self.padding,
                            self.padding + self.piece_size * 4 + self.space_between_boards,
                            self.piece_size, self.temp_to_center, lado_agresivo="IZQUIERDA", lado_pasivo="INFERIOR")
        self.board4 = Board(self.padding + self.piece_size * 4 + self.space_between_boards,
                            self.padding + self.piece_size * 4 + self.space_between_boards,
                            self.piece_size, self.temp_to_center, lado_agresivo="DERECHA", lado_pasivo="INFERIOR")

        self.boards = [self.board1, self.board2, self.board3, self.board4]
        self.running = True
        pygame.font.init()  # you have to call this at the start,
        # Turno del jugador blanco
        self.pieces_to_highligth = []
        self.player_aux = 2

        self.player1 = Player(0, False, lado_pasivo="SUPERIOR")
        self.player2 = Player(otro_player=self.player1, lado_pasivo="INFERIOR")

        self.player1.otro_player = self.player2
        self.player = self.player1 if self.player1.is_playing() else self.player2
        self.game_loop()

    def game_loop(self):
        while self.running:
            # Capturar eventos
            self.capture_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def capture_events(self):
        for event in pygame.event.get():
            # Terminar el proceso cuando se cierre la ventana
            if event.type == pygame.QUIT:
                self.running = False
            # Evento del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click izquierdo
                if event.button == 1:
                    print(self)
                    self.passive_move()

    def __str__(self):
        return f""

        # Obtiene el tablero donde dió click el jugador

    def get_selected_board(self, mouse_rect):
        for board in self.boards:
            if self.player.movimiento_pasivo:
                if mouse_rect.colliderect(board) and self.player.lado_pasivo == board.lado_pasivo:
                    return board
            else:
                if mouse_rect.colliderect(board) and self.player.lado_agresivo == board.lado_agresivo:
                    return board
        return None

        # Obtiene la coordenada del primer movimiento

    def get_selected_piece(self, mouse_rect, selected_board):
        for y in range(4):
            for x in range(4):
                if mouse_rect.colliderect(selected_board.map[y][x].rect) and \
                        selected_board.map[y][x].value == self.player_aux:
                    return selected_board.map[y][x]
        return None

    # Obtiene la coordenada del movimiento hacia donde quiere moverse
    def get_selected_next_piece(self, mouse_rect, selected_board: Board):

        for y in range(4):
            for x in range(4):
                if mouse_rect.colliderect(selected_board.map[y][x].rect):
                    return selected_board.map[y][x]
        return None

    def passive_move(self):
        # Capturar la posición del mouse, crear un rectangulo y verificar en cual tablero hizo click
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx, my, 1, 1)
        board = self.get_selected_board(mouse_rect)

        if board is None:
            print("Ningún tablero ha sido seleccionado")
            return False

        self.player_aux, self.player = (1, self.player1) if self.player1.is_playing() else (2, self.player2)

        piece_to_move = self.get_selected_piece(mouse_rect, board)
        # Si clickeó en una ficha que no sea del jugador actual no debe hacer nada
        if piece_to_move is None:
            print("Ficha incorrecta")
            return False
        available_coordinates = self.get_available_coordinates(board, piece_to_move)
        if available_coordinates:
            return self.validate_second_click(piece_to_move, board, available_coordinates)

    def validate_second_click(self, piece_to_move: Piece, board: Board, available_coordinates):
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
            piece_where_is_moved = self.get_selected_next_piece(mouse_rect, board)
            if self.player.movimiento_pasivo:
                self.player.new_x, self.player.new_y = piece_to_move.x - piece_where_is_moved.x, piece_to_move.y - piece_where_is_moved.y
            # else:
            #    self.player.new_x, self.player.new_y = None, None
            # Verificar que clickee en una ficha del mismo tablero
            if piece_where_is_moved is None:
                print("Click en ficha equivocada")
                continue
            # Verificar que la ficha clickeada no sea la misma que esocgió al principio
            if piece_to_move.get_coordinates() == piece_where_is_moved.get_coordinates():
                print("Es la misma ficha")
                self.pieces_to_highligth = []
                self.update_highlight()
                return False

            # Si la posición no está en los movimientos disponibles entonces no haga nada
            if piece_where_is_moved.get_coordinates() not in available_coordinates:
                print("Coordenada incorrecta: ", piece_where_is_moved.get_coordinates(),
                      available_coordinates)
                continue
            if self.player.movimiento_pasivo:
                print("Movimiento pasivo concretado")
            else:
                print("Movimiento agresivo concretado")
            # Mover la ficha
            piece_to_move.move(piece_where_is_moved, self.player.movimiento_pasivo)
            # Terminar el bucle
            # Limpiar las fichas a las que hay que mostrar highlight
            self.pieces_to_highligth = []
            # Cambiar el turno
            self.player.move(board.lado_agresivo)
            print(self)
            self.player_aux, self.player = (1, self.player1) if self.player1.is_playing() else (2, self.player2)
            return True

    # TODO Verificar correctamente cuales movimientos son válidos teniendo en cuenta el valor y de que no se pueden
    #  saltar fichas
    # Obtiene las coordendas disponibles donde puede hacer un movimiento
    def get_available_coordinates(self, board, piece_to_move: Piece):
        available_coordinates = []
        for line in board.map:
            for piece in line:
                if self.player.movimiento_pasivo:
                    if (piece.x, piece.y) in piece_to_move.valid_moves and (piece.value != self.player_aux):
                        self.pieces_to_highligth.append(piece)
                        available_coordinates.append((piece.x, piece.y))
                else:
                    new_x = piece_to_move.x - piece.x
                    new_y = piece_to_move.y - piece.y
                    codicion_posicion = self.player.new_x == new_x and self.player.new_y == new_y
                    if ((piece.x, piece.y) in piece_to_move.valid_moves and (
                            piece.value != self.player_aux) and codicion_posicion):
                        self.pieces_to_highligth.append(piece)
                        available_coordinates.append((piece.x, piece.y))

        self.update_highlight()
        return available_coordinates

    def update_highlight(self):
        self.draw_highlights()
        pygame.display.update()

    # Dibujar todos los elementos del mapa
    def draw(self):
        # Fondo
        # screen.fill((38, 163, 144))
        if self.player1.is_playing():
            self.screen.fill((255, 255, 255))
        else:
            self.screen.fill((0, 0, 0))

        for board in self.boards:
            self.draw_board(self.piece_size, board)

        self.draw_highlights()

    # Dibujar el tablero y sus elementos
    def draw_board(self, piece_size, board):
        temp_line = 4
        board.draw(self.screen, piece_size, temp_line)

    # Dibujar por las posiciones hacia las cuáles se podrá desplazar
    def draw_highlights(self):
        for piece in self.pieces_to_highligth:
            piece.draw_highlight(self.screen)

    # Actualiza el tablero y sus elementos
    def update(self):
        for board in self.boards:
            board.update()

        pygame.display.update()
