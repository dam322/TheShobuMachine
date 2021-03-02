import pygame


class Piece:
    def __init__(self, value, init_x, init_y, piece_size, temp_to_center, x, y):
        self.value = value
        self.rect = pygame.Rect(init_x + x * piece_size + temp_to_center / 2,
                                init_y + y * piece_size + temp_to_center / 2,
                                piece_size - temp_to_center,
                                piece_size - temp_to_center)

    def draw(self, screen):
        if self.value == 1:
            pygame.draw.rect(screen, (255, 255, 255), self.rect)
        elif self.value == 2:
            pygame.draw.rect(screen, (0, 0, 0), self.rect)

    def update(self):
        pass
