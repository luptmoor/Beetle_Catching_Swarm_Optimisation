import numpy as np
import pygame
from settings import *

view            = 0         # Variable for different views in visualisation


def draw_circle(screen, x, y, r, colour):
    pygame.draw.circle(screen, colour, (x, y), r)


class Visuals:
    def __init__(self, width, height, dt):
        self.FPS = 1/dt
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bug Catching Swarming Simulation")

        self.font = pygame.freetype.Font(None, 12)
        self.clock = pygame.time.Clock()

        self.screen.fill(GREEN)
        pygame.display.flip()


    def update(self, trees, bugs, drones):
        # Make sure visualisation is ended when window is closed
        global view
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    view += 1
                    if view > 3:
                        view = 0
                elif event.key == pygame.K_SPACE:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    pause = False

        self.screen.fill(GREEN)

        text_surface, text_rect = self.font.render('Active Drones: ' + str(round(len(drones))), (0, 0, 0))
        text_rect.center = (50, 10)
        self.screen.blit(text_surface, text_rect)

        text_surface, text_rect = self.font.render('Dead Drones: ' + str(round(N_DRONES - len(drones))), (0, 0, 0))
        text_rect.center = (250, 10)
        self.screen.blit(text_surface, text_rect)

        text_surface, text_rect = self.font.render('Bugs: ' + str(round(len(bugs))), (0, 0, 0))
        text_rect.center = (30, 25)
        self.screen.blit(text_surface, text_rect)

        for tree in trees:
            pygame.draw.circle(self.screen, BROWN, (tree.x, tree.y), tree.r_col)

        # Draw all bugs
        for bug in bugs:
            pygame.draw.circle(self.screen, BUG_COLOURS[bug.mode], (bug.x, bug.y), bug.r_col)

            if view == 3:

                pygame.draw.circle(self.screen, BUG_COLOURS[bug.mode], (bug.x, bug.y), bug.r_vis, 1)  # visual fields
                if bug.tree is not None:
                    pygame.draw.line(self.screen, BLUE, (bug.x, bug.y), (bug.tree.x, bug.tree.y), 1)

        for drone in drones:
            pygame.draw.circle(self.screen, GREY, (drone.x, drone.y), drone.r_col)

            if view == 1:
                pygame.draw.circle(self.screen, GREY, (drone.x, drone.y), drone.r_vis['drone'], 1)  # visual range for drones
                pygame.draw.circle(self.screen, BROWN, (drone.x, drone.y), drone.r_vis['tree'], 1)  # visual range for trees
                pygame.draw.circle(self.screen, RED, (drone.x, drone.y), drone.r_vis['bug'], 1)  # visual range for bugs
                for phobject in drone.visible_phobjects:
                    pygame.draw.line(self.screen, TYPE_COLOURS[phobject.type], (drone.x, drone.y), (phobject.x, phobject.y), 1)

            if view == 2:
                #pygame.draw.line(self.screen, BLUE, (drone.x, drone.y), (drone.x + drone.ax * 20, drone.y + drone.ay * 20), 1)

                text_surface, text_rect = self.font.render(str(round(drone.speed / V_DRONE_MAX * 100, 0)), (0, 0, 0))
                text_rect.center = (drone.x, drone.y)
                self.screen.blit(text_surface, text_rect)
            # for phobject in drone.visible_phobjects:
            #     dx = np.abs(drone.x - phobject.x)
            #     dy = np.abs(drone.y - phobject.y)
            #
            #     x = drone.ax / a_max * dx
            #     y = drone.ay / a_max * dy
            #
            #     pygame.draw.line(self.screen, blue, (drone.x, drone.y), (x, y), 1)


        pygame.display.flip()
        # self.clock.tick(self.FPS)


