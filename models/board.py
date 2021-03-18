import pygame

from models.piece import Piece


class Board:

    def __init__(self, x_pos, y_pos, piece_size, temp_to_center, lado_pasivo, lado_agresivo):
        self.map = []
        self.x = x_pos
        self.y = y_pos
        self.lado_pasivo = lado_pasivo
        self.lado_agresivo = lado_agresivo
        self.active = True
        for y in range(4):
            value = 0
            if y == 0:
                value = 1
            if y == 1 or y == 2:
                value = 0
            if y == 3:
                value = 2

            lista = list()
            for x in range(4):
                lista.append(Piece(value, self.x, self.y, piece_size, temp_to_center, x, y))
            self.map.append(lista)

        self.rect = pygame.Rect(x_pos,
                                y_pos,
                                4 * piece_size,
                                4 * piece_size)

    def __str__(self):
        return str(lista for lista in self.map)

    def draw(self, screen, piece_size, temp_line):
        pygame.draw.rect(screen, (0, 0, 155), self.rect)

        if not self.active:
            return
        #Dibujar lineas
        for x in range(5):
            pygame.draw.rect(screen, (155, 155, 155), pygame.Rect(self.x + x * piece_size,
                                                                  self.y,
                                                                  temp_line, 4 * piece_size))
            pygame.draw.rect(screen, (155, 155, 155), pygame.Rect(self.x,
                                                                  self.y + x * piece_size,
                                                                  4 * piece_size, temp_line))
        # Dibujar fichas

        for y in range(4):
            for x in range(4):
                self.map[y][x].draw(screen)

    def update(self):
        for y in range(4):
            for x in range(4):
                self.map[y][x].update()
