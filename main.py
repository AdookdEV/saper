import pygame
import random
from config import *
from game_objects import Field, FLAG_IMAGE, get_text
pygame.init()

CLOCK_IMAGE = pygame.image.load("images/clock.png")
CLOCK_IMAGE = pygame.transform.scale(CLOCK_IMAGE, (int(FIELD_W), int(FIELD_W)))


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.game_over = False
        self.game_objects = []
        self.grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_WIDTH)]
        self.create_objects()
        self.not_marked_bombs_count = BOMBS_COUNT
        self.game_state = None
        self.timer = 0
        self.font = get_text(20, "Arial")
        self.defused_fields_count = 0

    def set_bombs(self, f):
        pos_list = []
        for i in range(GRID_WIDTH):
            for j in range(GRID_WIDTH):
                pos_list.append([i, j])
        random.shuffle(pos_list)
        counter = 0
        for c, r in pos_list:
            if abs(c - f.col) + abs(r - f.row) > 2 and counter != BOMBS_COUNT:
                self.grid[r][c].with_bomb = True
                counter += 1
        for c, r in pos_list:
            if not self.grid[r][c].with_bomb:
                self.grid[r][c].near_bombs = sum(list(map(
                                lambda x: int(x.with_bomb),
                                self.grid[r][c].get_neighbors(self.grid))))
                self.grid[r][c].set_text()

    def defuse(self, f):
        if f.marked:
            return
        if f.with_bomb:
            self.game_state = "BOOM"
            return
        f.is_defused = True
        self.defused_fields_count += 1
        if f.near_bombs == 0:
            for n in f.get_neighbors(self.grid):
                if not n.is_defused and not n.with_bomb:
                    self.defuse(n)
        if self.defused_fields_count + BOMBS_COUNT == GRID_WIDTH**2:
            self.game_state = True

    def mark_field(self, f):
        if self.not_marked_bombs_count > 0:
            f.marked = not f.marked
            if f.marked:
                self.not_marked_bombs_count -= 1
            else:
                self.not_marked_bombs_count += 1
        elif f.marked:
            f.marked = False
            self.not_marked_bombs_count += 1

    def create_objects(self):
        for i in range(GRID_WIDTH):
            for j in range(GRID_WIDTH):
                self.grid[i][j] = Field(j*FIELD_W, i*FIELD_W, FIELD_W, Oy=50)
                self.game_objects.append(self.grid[i][j])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx >= 0 and mx <= WIN_SIZE[0] \
                        and my >= 50 and my <= WIN_SIZE[1]:
                    mxc, myr = mx // FIELD_W, (my - 50) // FIELD_W
                    if event.button == 1:
                        if self.defused_fields_count == 0:
                            self.set_bombs(self.grid[myr][mxc])
                        self.defuse(self.grid[myr][mxc])
                    elif event.button == 3:
                        self.mark_field(self.grid[myr][mxc])

    def draw(self):
        self.win.fill(BACKGROUND_COLOR)
        for o in self.game_objects:
            o.draw(self.win)

        # drawing timer
        self.win.blit(CLOCK_IMAGE, (0, (50 - FIELD_W) / 2))  # clock image
        self.win.blit(self.font.render(
            str(self.timer//self.fps), True, WHITE),
            (30, (50 - self.font.get_height()) / 2))  # text

        # drawing flag count
        self.win.blit(FLAG_IMAGE, (70, (50 - FIELD_W)/2))  # flag image
        self.win.blit(self.font.render(
                    str(self.not_marked_bombs_count), True, WHITE),
                    (75 + FIELD_W, (50 - self.font.get_height()) / 2))  # text

    def update(self):
        self.timer += 1
        pygame.display.update()
        for o in self.game_objects:
            o.update()
        if self.game_state == "WIN":
            pass
        elif self.game_state == "BOOM":
            self.game_over = True
            print("Game over")

    def run(self):
        while not self.game_over:
            self.clock.tick(self.fps)
            self.handle_events()
            self.draw()
            self.update()


if __name__ == "__main__":
    Game().run()
