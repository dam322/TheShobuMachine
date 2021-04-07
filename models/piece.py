from copy import copy

import pygame


class Piece:

    def __init__(self, value, piece_size, temp_to_center, x, y, board):
        self.board = board
        self.selected = False
        self.value = value
        self.rect = pygame.Rect(board.x + x * piece_size,
                                board.y + y * piece_size,
                                piece_size,
                                piece_size)
        self.draw_rect = pygame.Rect(board.x + x * piece_size + temp_to_center / 2,
                                     board.y + y * piece_size + temp_to_center / 2,
                                     piece_size - temp_to_center,
                                     piece_size - temp_to_center)
        self.x = x
        self.y = y
        self.valid_moves = [(x + 1, y),  # Derecha
                            (x - 1, y),  # Izquierda
                            (x, y + 1),  # Superior
                            (x, y - 1),  # Inferior
                            (x + 1, y + 1),  # Inferior derecha
                            (x - 1, y - 1),  # Superior izquierda
                            (x + 1, y - 1),  # Inferior izquierda
                            (x - 1, y + 1),  # Superior derecha
                            (x + 2, y),  # Derecha 2
                            (x - 2, y),  # Izquierda 2
                            (x, y + 2),  # Superior 2
                            (x, y - 2),  # Inferior 2
                            (x + 2, y + 2),  # Inferior derecha 2
                            (x - 2, y - 2),  # Superior izquierda 2
                            (x + 2, y - 2),  # Inferior izquierda 2
                            (x - 2, y + 2),  # Superior derecha 2
                            ]
        for x in self.valid_moves:
            if x[0] < 0 or x[0] < 0:
                self.valid_moves.remove(x)

    def draw(self, screen):
        if self.value == 1:
            pygame.draw.rect(screen, (255, 255, 255), self.draw_rect)
        elif self.value == 2:
            pygame.draw.rect(screen, (0, 0, 0), self.draw_rect)
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        self.draw_string(f"{self.y, self.x}", self.rect.x, self.rect.y, screen, myfont)

    def draw_highlight(self, screen):
        if self.selected:
            pygame.draw.rect(screen, (0, 155, 155), self.draw_rect)
        else:
            pygame.draw.rect(screen, (155, 155, 155), self.draw_rect)

    def get_salto(self, piece_to_move):
        dx = self.x - piece_to_move.x
        dy = self.y - piece_to_move.y
        new_dx = 0
        new_dy = 0
        if dx < 0:
            new_dx = 1
        elif dx > 0:
            new_dx = -1
        if dy < 0:
            new_dy = 1
        elif dy > 0:
            new_dy = -1
        # Verificar la siguiente ficha
        next_x = piece_to_move.x + new_dx
        next_y = piece_to_move.y + new_dy
        return next_x, next_y, dx, dy

    # TODO Definir la lógica del movimiento. Por ahora es sólo un intercambio que no sirve de mucho
    def move(self, piece_where_is_moved, movimiento_pasivo):
        if movimiento_pasivo:
            self.value, piece_where_is_moved.value = piece_where_is_moved.value, self.value
        else:
            # Obtener la posición siguiente
            next_x, next_y, dx, dy = self.get_salto(piece_where_is_moved)

            # Si está dentro del mapa
            if 0 <= next_x < len(self.board.map) and 0 <= next_y < len(self.board.map):
                if piece_where_is_moved.value == 0:
                    if abs(dx) == 2 or abs(dy) == 2:
                        middle_piece: Piece = self.board.map[int((self.y + piece_where_is_moved.y) / 2)][
                            int((self.x + piece_where_is_moved.x) / 2)]

                        if middle_piece.value == 0:
                            # La ficha del medio está vacía, no importa
                            print("--> Ficha movida 1")
                            value_self = copy(self.value)
                            self.value = 0
                            piece_where_is_moved.value = value_self
                        else:
                            # La ficha del medio es enemiga
                            print("--> Ficha empujada 2 posiciones")
                            next_piece = self.board.map[next_y][next_x]
                            value_self = copy(self.value)
                            self.value = 0
                            piece_where_is_moved.value = value_self
                            next_piece.value = copy(middle_piece.value)
                            middle_piece.value = 0
                    else:
                        print("--> Ficha movida 2")
                        value_self = copy(self.value)
                        self.value = 0
                        piece_where_is_moved.value = value_self
                else:
                    print("--> Ficha empujada 1 posición")
                    next_piece = self.board.map[next_y][next_x]
                    value_self = copy(self.value)
                    value_piece = copy(piece_where_is_moved.value)
                    self.value = 0
                    piece_where_is_moved.value = value_self
                    next_piece.value = value_piece
            else:
                if abs(dx) == 2 or abs(dy) == 2:
                    middle_piece: Piece = self.board.map[int((self.y + piece_where_is_moved.y) / 2)][
                        int((self.x + piece_where_is_moved.x) / 2)]
                    middle_piece.value = 0

                print("--> Ficha sacada del tablero")
                value_self = copy(self.value)
                self.value = 0
                piece_where_is_moved.value = value_self
        self.selected = False

    def check_coordinates(self, other_piece):
        if self.get_coordinates() == other_piece.get_coordinates():
            print("--> Selección cancelada")
            # Retorna false para que se pueda cancelar el movimiento
            return True
        return False

    def get_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return f"X:{self.x}, Y:{self.y}"

    def draw_string(self, string: str, x, y, ventana, font):
        textsurface = font.render(string, False, (255, 255, 255))
        ventana.blit(textsurface, (x, y))
