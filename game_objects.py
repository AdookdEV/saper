import pygame
from config import *

FLAG_IMAGE = pygame.image.load("images/flag.png")
FLAG_IMAGE = pygame.transform.scale(FLAG_IMAGE, (int(FIELD_W), int(FIELD_W)))


def get_text(size, font_family):
    font = pygame.font.SysFont(font_family, size)
    return font


class Field:
    def __init__(self, x, y, w, Ox=0, Oy=0):
        self.rect = pygame.Rect(x+Ox, y+Oy, w, w)
        self.marked = False
        self.with_bomb = False
        self.is_defused = False
        self.Ox, self.Oy = Ox, Oy
        self.near_bombs = 0

    def set_text(self):
        if self.near_bombs != 0:
            self.number_text = get_text(FIELD_W, "Arial").render(
                                                str(self.near_bombs), True,
                                                NUMBER_COLORS[self.near_bombs])
            self.number_text_rect = self.number_text.get_rect()
            self.number_text_rect.center = self.rect.center

    @property
    def col(self):
        return (self.x - self.Ox) // self.w

    @property
    def row(self):
        return (self.y - self.Oy) // self.w

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def w(self):
        return self.rect.w

    def get_neighbors(self, grid):
        l = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                if dx + self.col < len(grid) and dx + self.col >= 0 \
                        and dy + self.row < len(grid) and dy + self.row >= 0:
                    l.append(grid[self.row + dy][self.col + dx])
        return l

    def draw(self, surf):
        if not self.is_defused:
            pygame.draw.rect(
                    surf,
                    FIELD_COLORS[(self.col + self.row) % 2],
                    self.rect)
            if self.marked:
                surf.blit(FLAG_IMAGE, self.rect)
        elif not self.with_bomb:
            pygame.draw.rect(
                    surf,
                    DEFUSED_FIELD_COLORS[(self.col + self.row) % 2],
                    self.rect)
            if self.near_bombs != 0:
                surf.blit(
                            self.number_text,
                            self.number_text_rect)

    def update(self):
        pass
