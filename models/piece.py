import pygame


class Piece:
    def __init__(self, value, init_x, init_y, piece_size, temp_to_center, x, y):
        self.value = value
        self.rect = pygame.Rect(init_x + x * piece_size + temp_to_center / 2,
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

    def draw(self, screen):
        if self.value == 1:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
        elif self.value == 2:
            pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def draw_highlight(self, screen):
        # if self.value == 1:
        pygame.draw.rect(screen, (155, 155, 155), self.rect)
        # elif self.value == 2:
        # pygame.draw.rect(screen, (225, 225, 255), self.rect)

    def update(self):
        pass

    def is_valid_moves(self, x, y):
        return (x, y) in self.valid_moves

    def move(self, piece):
        # TODO Definir la lógica del movimiento. Por ahora es sólo un intercambio que no sirve de mucho
        self.value, piece.value = piece.value, self.value
        # self.valid_moves, piece.valid_moves = piece.valid_moves, self.valid_moves

    def get_coordinates(self):
        return self.x, self.y
