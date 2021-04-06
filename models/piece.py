import pygame


class Piece:
    def __init__(self, value, init_x, init_y, piece_size, temp_to_center, x, y):
        self.value = value
        self.rect = pygame.Rect(init_x + x * piece_size,
                                init_y + y * piece_size,
                                piece_size,
                                piece_size)
        self.draw_rect = pygame.Rect(init_x + x * piece_size + temp_to_center / 2,
                                     init_y + y * piece_size + temp_to_center / 2,
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
        self.draw_string(f"{self.x, self.y}", self.rect.x, self.rect.y, screen, myfont)

    def draw_highlight(self, screen):
        if self.selected:
            pygame.draw.rect(screen, (0, 155, 155), self.draw_rect)
        else:
            pygame.draw.rect(screen, (155, 155, 155), self.draw_rect)

    def update(self):
        pass

    # TODO Definir la lógica del movimiento. Por ahora es sólo un intercambio que no sirve de mucho
    def move(self, piece, movimiento_pasivo, val):
        if movimiento_pasivo:
            # No se pueden empujar fichas
            if piece_to_move.value == val:
                self.value, piece_to_move.value = piece_to_move.value, self.value
                return True
            else:
                return False
        else:
            # Se pueden empujar fichas
            next_x, next_y, _, _ = self.get_salto(piece_to_move)

            dentro_mapa = 0 <= next_x < len(board.map) and 0 <= next_y < len(board.map)

            # condicion_existe = board.map[next_y][next_x].value == 0
            if dentro_mapa:
                print("EMPUJE")
                if piece_to_move.value == 0:
                    value_self = copy(self.value)
                    self.value = val
                    piece_to_move.value = value_self
                else:
                    next_piece = board.map[next_y][next_x]
                    value_self = copy(self.value)
                    value_piece = copy(piece_to_move.value)
                    self.value = val
                    piece_to_move.value = value_self
                    next_piece.value = value_piece

            else:
                value_self = copy(self.value)
                # value_piece = piece.value
                self.value = val
                piece_to_move.value = value_self
                # next_piece.value = value_piece
            return True

    def get_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return f"X:{self.x}, Y:{self.y}"

    def draw_string(self, string: str, x, y, ventana, font):
        textsurface = font.render(string, False, (255, 255, 255))
        ventana.blit(textsurface, (x, y))
