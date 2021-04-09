import math
from copy import deepcopy, copy
import time
import pygame

from models.board import Board
from models.player import Player
from models.piece import Piece


def draw_text(text: str, font, surface, x, y):
    textobj = font.render(text, 1, (0, 0, 0))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Game:
    player_playing: Player

    def __init__(self, player1, player2, max_depth):
        self.contador = 0
        # Tamaño de las piezas
        self.piece_size = 64
        # Espacio entre los trableros
        self.space_between_boards = 40
        # Distancia entre el borde la pantalla y los tableros
        self.padding = 30
        # Distancia para centrar las piezas y que no ocupen el espacio del tablero
        self.temp_to_center = 20
        self.debug_size = 150
        self.max_depth = max_depth
        # Calcular el tamaño de la pantalla
        self.screen = pygame.display.set_mode(
            (8 * self.piece_size + self.space_between_boards + 2 * self.padding + self.debug_size + 200,
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
        self.turno = 0
        # Turno del jugador blanco
        self.pieces_to_highligth = []
        self.player1 = Player(movimiento_pasivo=False, lado_pasivo="SUPERIOR", value=1, is_machine=player1)
        self.player2 = Player(movimiento_pasivo=True, lado_pasivo="INFERIOR", value=2, is_machine=player2)
        self.player1.enemy_player = self.player2
        self.player2.enemy_player = self.player1

    def __str__(self):
        return f""

    # Obtiene el tablero donde dió click el jugador
    def get_selected_board(self, mouse_rect):
        for board in self.boards:
            if self.player_playing.movimiento_pasivo:
                if not mouse_rect.colliderect(board):
                    continue
                if not self.player_playing.lado_pasivo == board.lado_pasivo:
                    continue
                return board
            else:
                if mouse_rect.colliderect(board) and self.player_playing.lado_agresivo == board.lado_agresivo:
                    return board
        return None

    # Obtiene la coordenada del primer movimiento
    def get_selected_piece_in_board(self, mouse_rect, selected_board):
        for y in range(4):
            for x in range(4):
                if mouse_rect.colliderect(selected_board.map[y][x].rect) and \
                        selected_board.map[y][x].value == self.player_playing.value:
                    return selected_board.map[y][x]
        return None

    # Obtiene la coordenada del movimiento hacia donde quiere moverse
    def get_selected_next_piece_in_board(self, mouse_rect, selected_board: Board):
        for y in range(4):
            for x in range(4):
                if mouse_rect.colliderect(selected_board.map[y][x].rect):
                    return selected_board.map[y][x]
        return None

    # Retorna la ficha seleccionada
    def get_selected_piece(self, is_first_click, piece_to_move: Piece = None):
        # Capturar la posición del mouse, crear un rectangulo y verificar en cual tablero hizo click
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx, my, 1, 1)
        board = self.get_selected_board(mouse_rect)

        if board is None:
            print("--> Seleccione un tablero correcto.")
            return None
        if is_first_click:
            selected_piece = self.get_selected_piece_in_board(mouse_rect, board)
        else:
            if piece_to_move.board != board:
                print("--> Seleccione el tablero de la misma ficha seleccionada")
                return None
            selected_piece = self.get_selected_next_piece_in_board(mouse_rect, board)

        # Si clickeó en una ficha que no sea del jugador actual no debe hacer nada
        if selected_piece is None:
            print("--> Seleccione una ficha correcta.")
            return None
        return selected_piece

    # Obtiene las coordenadas bloqueadas por otras fichas en el movimiento pasivo
    def get_blocked_pieces(self, board: Board, piece_to_move):
        if not self.player_playing.movimiento_pasivo:
            return []
        blocked_dict = {
            (1, 0): (2, 0),  # Derecha
            (-1, 0): (-2, 0),  # Izquierda
            (0, 1): (0, 2),  # Superior
            (0, -1): (0, -2),  # Inferior
            (1, 1): (2, 2),  # Inferior derecha
            (-1, -1): (-2, -2),  # Superior izquierda
            (1, -1): (2, -2),  # Inferior izquierda
            (-1, 1): (-2, 2),  # Superior derecha
        }
        blocked_positions = []
        for line in board.map:
            for piece in line:
                # En el movimiento pasivo se bloquean las posiciones que no están vacías
                if piece.value != 0:
                    dx = piece_to_move.x - piece.x
                    dy = piece_to_move.y - piece.y
                    # Sólo se puede mover máximo 2 fichas
                    if dx < 2 and dy < 2:
                        blocked_positions.append((dx, dy))
                        # Si hay una ficha en una posición se bloquea la que estén en la misma dirección
                        # respecto a la ficha que se desea mover
                        if (dx, dy) in blocked_dict.keys():
                            blocked_positions.append(blocked_dict[(dx, dy)])
        return blocked_positions

    # Obtiene las coordendas disponibles en el movimiento pasivo
    def get_available_pieces_passive(self, board, piece_to_move, debug=False):
        if not self.player_playing.movimiento_pasivo:
            return None

        blocked_positions = self.get_blocked_pieces(board, piece_to_move)
        available_coordinates = []

        for line in board.map:
            for piece in line:
                # Se calculan los dx y dy
                dx = piece_to_move.x - piece.x
                dy = piece_to_move.y - piece.y
                # Se verifica si es un movimiento valido y si no está en las posiciones bloqueadas.
                #  que no sea una ficha del mismo jugador.
                if (piece.x, piece.y) in piece_to_move.valid_moves and (
                        piece.value != self.player_playing.value) and not \
                        (dx, dy) in blocked_positions:
                    # Si es un espacio vacío
                    if piece.value == 0:
                        # Se resaltan las fichas que estén vacías
                        if not debug:
                            self.pieces_to_highligth.append(piece)
                        available_coordinates.append((piece.x, piece.y))
        return available_coordinates

    # Obtiene las coordendas disponibles en el movimiento agresivo
    def get_available_pieces_aggresive(self, board, piece_to_move, debug=False):
        if not self.player_playing.movimiento_agresivo:
            return None
        blocked_positions = self.get_blocked_pieces(board, piece_to_move)
        available_coordinates = []
        for line in board.map:
            for piece in line:
                is_blocked = piece.get_coordinates() in blocked_positions
                if is_blocked:
                    continue
                # Se calculan los dx y dy.
                next_x, next_y, dx, dy = piece_to_move.get_salto(piece)

                is_the_lastest_dx = self.player_playing.passive_move_dx == dx and self.player_playing.passive_move_dy == dy
                if not is_the_lastest_dx:
                    continue
                # Se verifica que sea un movimiento válido
                is_valid_movement = (piece.x, piece.y) in piece_to_move.valid_moves
                if not is_valid_movement:
                    if not debug:
                        print("No es un movimiento válido")
                    continue

                # Se verifica que la ficha no sea del mismo jugador
                is_different_player = (piece.value != self.player_playing.value)
                if not is_different_player:
                    if not debug:
                        print("Es del mismo jugador")
                    continue

                if abs(dx) == 2 or abs(dy) == 2:
                    # Se verifica que al desplazarse 2 posiciones y empujar no hayan otra ficha en medio estorbando
                    out_of_board = next_x < 0 or next_y < 0 or next_x >= len(board.map) or next_y >= len(board.map)
                    if not out_of_board:
                        if not debug:
                            print("DENTRO DEL TABLERO")
                        ficha = board.map[next_y][next_x]
                        middle_piece: Piece = board.map[int((piece_to_move.y + piece.y) / 2)][
                            int((piece_to_move.x + piece.x) / 2)]

                        if middle_piece.value != 0:
                            if not debug:
                                print(middle_piece)
                                print(ficha)
                                print(piece)
                            if piece.value != 0:
                                if not debug:
                                    print("Bloqueado por 2 fichas seguidas.")
                                continue
                            if ficha.value != 0:
                                if not debug:
                                    print("Funciona normal...")
                                continue
                            if middle_piece.value == self.player_playing.value:
                                # if ficha.value != 0:
                                if not debug:
                                    print("Bloqueado por ser ficha aliada", ficha)
                                continue
                            if middle_piece.value == self.player_playing.enemy_player.value:
                                if ficha.value != 0:
                                    if not debug:
                                        print("Bloqueado por ficha enemiga", ficha)
                                    continue
                    else:
                        if not debug:
                            print("FUERA DEL TABLERO")
                        middle_piece: Piece = board.map[int((piece_to_move.y + piece.y) / 2)][
                            int((piece_to_move.x + piece.x) / 2)]
                        if middle_piece.value == self.player_playing.value:
                            # if ficha.value != 0:
                            if not debug:
                                print("Bloqueado por ser ficha aliada", middle_piece)
                                print(piece)
                            continue
                        if middle_piece.value == self.player_playing.enemy_player.value:

                            if piece.value == self.player_playing.enemy_player.value:
                                if not debug:
                                    print("Bloqueado por 2 fichas enemigas")
                                    print(middle_piece)
                                    print(piece)
                                continue

                        #    continue

                    # middle_piece: Piece = board.map[int((piece_to_move.y + piece.y) / 2)][
                    #    int((piece_to_move.x + piece.x) / 2)]
                    # if middle_piece.value != 0:
                    #    print("Pieza del centro bloqueada", middle_piece)
                    #    continue

                # Se verifica si la ficha siguiente quedaría fuera del tablero
                out_of_board = next_x < 0 or next_y < 0 or next_x >= len(board.map) or next_y >= len(board.map)
                if out_of_board:
                    # Es una coordenada viable si la siguiente ficha queda fuera del tablero
                    if not debug:
                        self.pieces_to_highligth.append(piece)
                    available_coordinates.append((piece.x, piece.y))
                    return available_coordinates
                else:
                    nothing_behind = board.map[next_y][next_x].value == 0

                    if piece.value == 0:
                        # Es una coordenada viable si la ficha está vacía
                        if not debug:
                            self.pieces_to_highligth.append(piece)
                        available_coordinates.append((piece.x, piece.y))
                        return available_coordinates
                    elif nothing_behind:
                        # Es una coordenada viable si no hay nada detrás de la ficha
                        if not debug:
                            self.pieces_to_highligth.append(piece)
                        available_coordinates.append((piece.x, piece.y))
                        return available_coordinates
        return available_coordinates

    # Obtiene las coordenadas disponibles basado en si es un movimiento agresivo o pasivo
    def get_available_pieces(self, selected_piece):
        if self.player_playing.movimiento_pasivo:
            return self.get_available_pieces_passive(selected_piece.board, selected_piece)
        else:
            return self.get_available_pieces_aggresive(selected_piece.board, selected_piece)

    # Valida que el primer click haya sido correcto
    def validate_first_click(self):
        # Obtener la ficha seleccionada
        selected_piece = self.get_selected_piece(True)

        # Si clickeó en una ficha que no sea del jugador actual no debe hacer nada
        if selected_piece is None:
            return True

        # Obtener la lista de fichas donde se puede mover
        available_pieces_to_move = self.get_available_pieces(selected_piece)

        if not available_pieces_to_move:
            return True
        selected_piece.selected = True
        self.pieces_to_highligth.append(selected_piece)
        self.update_highlight()
        return self.validate_second_click(selected_piece, selected_piece.board, available_pieces_to_move)

    # Valida que el segundo click cumpla con las condiciones
    def is_valid_second_click(self, piece_to_move, available_coordinates):
        # Esperar al siguiente click para hacer el movimiento
        event = pygame.event.wait()
        # Si el evento no es un click entonces reinicie el bucle
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        # Obtener la ficha seleccionada
        piece_where_is_moved = self.get_selected_piece(False, piece_to_move)

        # Si no hay una ficha seleccionada reinicie el bucle
        if piece_where_is_moved is None:
            return None

        # Si la posición no está en los movimientos disponibles entonces no haga nada
        if piece_where_is_moved.get_coordinates() not in available_coordinates:
            print("--> Movimiento inválido")
            return None
        return piece_where_is_moved

    # Reiniciar las variables y avanzar los movimientos
    def reset_for_next_move(self, board, piece_to_move, piece_where_is_moved):
        if self.player_playing.movimiento_pasivo:
            print("--> Movimiento pasivo concretado")
        else:
            print("--> Movimiento agresivo concretado")
        # Limpiar las fichas a las que hay que mostrar highlight
        self.pieces_to_highligth = []
        # Cambiar el turno
        self.player_playing.move(board.lado_agresivo, piece_to_move, piece_where_is_moved)
        self.player_playing = self.player1 if self.player1.is_playing() else self.player2

    # Valida que el segundo click haya sido correcto
    def validate_second_click(self, piece_to_move, board, available_coordinates):
        # Mientras no clickee en una ficha correcta.
        while True:
            # Seleccionar la misma ficha
            available_coordinates.append(piece_to_move.get_coordinates())
            # Obtener la ficha a donde será movida. Si no es valida
            # entonces continue con el bucle.

            piece_where_is_moved = self.is_valid_second_click(piece_to_move, available_coordinates)
            if not piece_where_is_moved:
                continue

            # Verificar que la ficha clickeada no sea la misma que escogió al principio
            if piece_to_move.check_coordinates(piece_where_is_moved):
                print("--> Ha seleccionado la misma ficha")
                self.pieces_to_highligth = []
                self.update_highlight()
                return True

            # Mover la ficha
            piece_to_move.move(piece_where_is_moved, self.player_playing.movimiento_pasivo)
            if self.player_playing.contador_turno == 1:
                self.turno += 1
            self.reset_for_next_move(board, piece_to_move, piece_where_is_moved)
            # Verificar si al hacer el movimiento pasivo el movimiento agresivo se bloquea
            return self.possible_agressive_moves() != {}

    # Retorna los posibles movimientos en un estado del juego
    def possible_moves(self, debug=False):
        if self.player_playing.movimiento_pasivo:
            return self.possible_passive_moves(debug)
        else:
            return self.possible_agressive_moves(debug)

    # Retorna los posibles movimientos agresivos
    def possible_agressive_moves(self, debug=False):
        if not self.player_playing.movimiento_agresivo:
            return None
        acum = {}
        for board in self.boards:
            if board.lado_agresivo != self.player_playing.lado_agresivo:
                continue
            for line in board.map:
                for piece in line:
                    if piece.value != self.player_playing.value:
                        continue
                    temp = self.get_available_pieces_aggresive(board, piece, debug)
                    if temp:
                        acum[piece] = temp
        return acum

    # Retorna los posibles movimientos pasivos
    def possible_passive_moves(self, debug):
        if not self.player_playing.movimiento_pasivo:
            return None
        acum = {}
        for board in self.boards:
            if board.lado_pasivo != self.player_playing.lado_pasivo:
                continue
            for line in board.map:
                for piece in line:
                    if piece.value != self.player_playing.value:
                        continue
                    acum[piece] = (self.get_available_pieces_passive(board, piece, debug))
        return acum

    # Zona de display
    # Dibuja las fichas resaltadas
    def update_highlight(self):
        self.draw_highlights()
        pygame.display.update()

    # Dibujar todos los elementos del mapa
    def draw(self):
        # Fondo
        self.screen.fill((155, 155, 155))
        remaining_light_pieces, remaining_dark_pieces = self.count_pieces()
        game_tittle = pygame.font.SysFont('Comic Sans MS', 50)
        piece_tittle = pygame.font.SysFont('Comic Sans MS', 30)
        draw_text('The Shobu', game_tittle, self.screen, 650, 50)
        draw_text('Machine', game_tittle, self.screen, 675, 100)
        draw_text('Dark Pieces:', piece_tittle, self.screen, 605, 230)
        draw_text(f"{remaining_dark_pieces}", piece_tittle, self.screen, 795, 230)
        draw_text('Light Pieces:', piece_tittle, self.screen, 605, 280)
        draw_text(f"{remaining_light_pieces}", piece_tittle, self.screen, 795, 280)
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
        pygame.display.update()

    # Almacena el estado del juego
    def save_state(self):
        return deepcopy(self.boards), deepcopy(self.player1), deepcopy(self.player2)

    # Restaura el estado del juego
    def restore_state(self, boards, player1, player2):
        self.boards = boards
        self.player1 = player1
        self.player2 = player2

    # Capturar eventos
    def capture_events(self):
        boards, player1, player2 = self.save_state()
        for event in pygame.event.get():
            # Terminar el proceso cuando se cierre la ventana
            if event.type == pygame.QUIT:
                self.running = False
            # Evento del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click izquierdo
                if event.button != 1:
                    continue
                self.player_playing = self.player2 if self.turno % 2 == 0 else self.player1
                # print("TURNO DE:", self.player_playing)
                self.reset_last_move()
                if self.player_playing.is_machine:
                    self.try_all_possible_moves(depth=self.max_depth, alpha=-math.inf, beta=math.inf, maximizing=True,
                                                initial=True)
                elif not self.validate_first_click():
                    self.restore_state(boards, player1, player2)

    # Bucle del juego
    def game_loop(self):
        while self.running:
            # Capturar eventos
            self.capture_events()
            self.draw()
            self.update()
            self.clock.tick(60)

    def print_board(self, board):
        for line in board.map:
            for piece2 in line:
                print(piece2.value, end=", ")
            print()

    def save_map(self, piece):
        mapa = []
        for line in piece.board.map:
            temp = []
            for piece2 in line:
                temp.append(piece2.value)
            mapa.append(temp)

        return mapa

    def restore_map(self, mapa, piece):
        y = 0
        for line in mapa:
            x = 0
            for value in line:
                piece.board.map[y][x].value = value
                x += 1
            y += 1

    def apply_move(self, piece: Piece, move, debug=True):
        x, y = move
        piece.move(piece.board.map[y][x], self.player_playing.movimiento_pasivo, debug)

    def try_all_possible_moves(self, depth, alpha, beta, maximizing, initial):
        activated = True
        # Calcular los posibles movimientos pasivos
        passive_moves = self.possible_passive_moves(True)
        # for i in range(self.max_depth - depth):
        #    print("\t\t", end="")
        # print("MAXIMIZANDO" if maximizing else "MINIMIZANDO", "--------------------> ",
        #      self.player_playing, depth)

        # Crear las variables para tener la información
        best_passive_move = None
        best_passive_piece = None
        global_aggresive_move = None
        global_aggresive_piece = None
        global_aggresive_value = -math.inf if maximizing else math.inf
        initial_time = 0
        if initial:
            initial_time = time.time_ns()
            self.contador = 0
        # Iterar sobre cada ficha que se puede mover
        for passive_piece in passive_moves.keys():
            # Guardar el estado del mapa
            passive_map = self.save_map(passive_piece)
            self.player_playing.contador_turno = 2
            self.player_playing.movimiento_pasivo = True
            self.player_playing.movimiento_agresivo = False
            # Iterar sobre cada movimiento posible de una ficha
            for passive_move in passive_moves[passive_piece]:
                x, y = passive_move
                # Actualizar las variables

                self.player_playing.update_passive_change(passive_piece, passive_piece.board.map[y][x])
                self.player_playing.on_passive(passive_piece.board.lado_agresivo, passive_piece,
                                               passive_piece.board.map[y][x])

                # Calcular los posibles movimiento agresivos
                agressive_moves = self.possible_agressive_moves(True)
                # Crear las variables para tener la información
                best_aggresive_move = None
                best_aggresive_piece = None
                best_score = -math.inf if maximizing else math.inf

                # Iterar sobre cada ficha que se puede mover
                for aggresive_piece in agressive_moves.keys():
                    self.contador += 1
                    # Guardar el estado del mapa
                    agressive_map = self.save_map(aggresive_piece)
                    self.apply_move(passive_piece, passive_move)
                    self.player_playing.contador_turno = 1
                    self.player_playing.movimiento_pasivo = False
                    # self.player_playing.movimiento_agresivo = True
                    # print(self.player_playing.nombre,self.evaluate())
                    # Iterar sobre cada movimiento posible de una ficha
                    for aggresive_move in agressive_moves[aggresive_piece]:
                        # Actualizar las variables
                        self.apply_move(aggresive_piece, aggresive_move)
                        self.player_playing.enemy_player.contador_turno = 2
                        self.player_playing.enemy_player.movimiento_pasivo = True
                        self.player_playing.enemy_player.movimiento_agresivo = False
                        self.player_playing = self.player_playing.enemy_player

                        score = self.minimax(depth - 1, alpha, beta, not maximizing)

                        self.player_playing.enemy_player.contador_turno = 0
                        self.player_playing.enemy_player.movimiento_pasivo = False
                        self.player_playing.enemy_player.movimiento_agresivo = False
                        self.player_playing = self.player_playing.enemy_player
                        self.player_playing.contador_turno = 1
                        self.player_playing.movimiento_pasivo = False
                        self.player_playing.movimiento_agresivo = True
                        self.restore_map(agressive_map, aggresive_piece)
                        if maximizing:
                            # Condición invertida
                            if score > best_score:
                                best_score = score
                                best_aggresive_move = aggresive_move
                                best_aggresive_piece = aggresive_piece
                                if activated:
                                    alpha = max(alpha, score)
                                    if beta <= alpha:
                                        break
                        else:
                            if score < best_score:
                                best_score = score
                                best_aggresive_move = aggresive_move
                                best_aggresive_piece = aggresive_piece
                                if activated:
                                    beta = min(beta, score)
                                    if beta <= alpha:
                                        break
                    self.player_playing.contador_turno = 1
                    self.player_playing.movimiento_pasivo = False
                    self.player_playing.movimiento_agresivo = True
                # Restaurar el estado del tablero:
                self.restore_map(passive_map, passive_piece)
                if maximizing:
                    if best_score > global_aggresive_value:
                        best_passive_move = passive_move
                        best_passive_piece = passive_piece
                        global_aggresive_move = best_aggresive_move
                        global_aggresive_piece = best_aggresive_piece
                        global_aggresive_value = best_score
                        if activated:
                            alpha = max(alpha, global_aggresive_value)
                            if beta <= alpha:
                                break

                else:
                    if best_score < global_aggresive_value:
                        best_passive_move = passive_move
                        best_passive_piece = passive_piece
                        global_aggresive_move = best_aggresive_move
                        global_aggresive_piece = best_aggresive_piece
                        global_aggresive_value = best_score
                        if activated:
                            beta = min(beta, global_aggresive_value)
                            if beta <= alpha:
                                break

            self.player_playing.contador_turno = 2
            self.player_playing.movimiento_pasivo = True
            self.player_playing.movimiento_agresivo = False

        if initial:
            self.apply_best_move(best_passive_move, best_passive_piece, global_aggresive_move,
                                 global_aggresive_piece)
            print("POSSIBLE MOVES:", self.contador)
            print("Execution time (s):", (time.time_ns() - initial_time) / (10 ** 9))
        else:
            return global_aggresive_value

    def apply_best_move(self, best_passive_move, best_passive_piece, global_aggresive_move, global_aggresive_piece):
        # Aplicar el movimiento pasivo
        x, y = best_passive_move
        self.apply_move(best_passive_piece, best_passive_move, False)
        self.player_playing.on_passive(best_passive_piece.board.lado_agresivo, best_passive_piece,
                                       best_passive_piece.board.map[y][x])
        # Aplicar el movimiento agresivo
        self.apply_move(global_aggresive_piece, global_aggresive_move, False)
        self.player_playing.on_agressive()
        # Cambiar el jugador que está jugando
        self.turno += 1

    def reset_last_move(self):
        for board in self.boards:
            for line in board.map:
                for piece in line:
                    piece.last_move = None

    def check_win(self):
        remaining_light_pieces, remaining_dark_pieces = self.count_pieces()
        return 0 in remaining_dark_pieces or 0 in remaining_light_pieces

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0 or self.check_win():
            return self.evaluate()

        if maximizing:
            return self.try_all_possible_moves(depth=depth, alpha=alpha, beta=beta, maximizing=True, initial=False)
        else:
            return self.try_all_possible_moves(depth=depth, alpha=alpha, beta=beta, maximizing=False, initial=False)

    def evaluate(self):
        acum1 = 0
        fichas_centro = 0
        acum2 = 0
        for board in self.boards:
            y = 0
            count1 = 0
            count2 = 0
            for line in board.map:
                x = 0
                for piece in line:
                    if piece.value == self.player_playing.value:
                        count1 += 1
                    if piece.value == self.player_playing.enemy_player.value:
                        count2 += 1
                    if 1 <= x <= 2 and 1 <= y <= 2:
                        if piece.value == self.player_playing.value:
                            fichas_centro += 1
                    x += 1
                y += 1
            if count1 == 0:
                acum1 += 1000
            if count2 == 0:
                acum1 += 1000
            acum1 += count1
            acum2 += count2

        return acum1 - acum2

    def count_pieces(self):
        acum1 = []
        acum2 = []
        for board in self.boards:
            cont1 = 0
            cont2 = 0
            for line in board.map:
                for piece in line:
                    if piece.value == self.player1.value:
                        cont1 += 1
                    elif piece.value == self.player2.value:
                        cont2 += 1
            acum1.append(cont1)
            acum2.append(cont2)
        return acum1, acum2
