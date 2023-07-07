import pygame
from settings import *


def draw_circle(screen, x, y, r, colour):
    pygame.draw.circle(screen, colour, (x, y), r)


class Visuals:
    def __init__(self, width, height, dt):
        self.FPS = 1/dt
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bug Catching Swarming Simulation")
        self.clock = pygame.time.Clock()

        self.screen.fill(green)
        pygame.display.flip()


    def update(self, trees, bugs):
        # Make sure visualisation is ended when window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.fill(green)

        for tree in trees:
            pygame.draw.circle(self.screen, brown, (tree.x, tree.y), tree.r_col)

        # Draw all bugs
        for bug in bugs:
            pygame.draw.circle(self.screen, bug_colours[bug.mode], (bug.x, bug.y), bug.r_col)


        pygame.display.flip()
        self.clock.tick(self.FPS)


