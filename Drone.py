import numpy as np
from PhysicalObject import PhysicalObject
from settings import *


class Drone(PhysicalObject):
    def __init__(self, name, type, x, y, r_col=r_drone, r_vis=r_drone_vision):
        super().__init__(name, type, x, y, r_col)

        self.activity = 0

        # Tunable Parameters
        self.r_vis_bug = 150
        self.r_vis_drone = 100
        self.r_vis_tree = 40
        self.r_vis = {'tree': self.r_vis_tree, 'drone': self.r_vis_drone, 'bug': self.r_vis_bug}

        self.k_tree = 20
        self.k_neardrone = 1.5
        self.k_fardrone = -0.0001
        self.k_bug = -0.5
        self.gains = {'tree': self.k_tree, 'drone': self.k_neardrone, 'bug': self.k_bug}

        self.v_min = 5
        self.p_random = 0.1
        self.k_random = 0.4



        self.visible_phobjects = []
        self.codrones = []
        self.speed = self.v_min
        self.ax = 0
        self.ay = 0
        self.heading = np.random.random() * 2 * np.pi





    def advance(self, dt):
        axs = []
        ays = []

        for phobject in self.visible_phobjects:
            d = np.sqrt((phobject.x - self.x)**2 + (phobject.y - self.y)**2) - phobject.r_col
            theta = np.arctan2(self.y - phobject.y, self.x - phobject.x)

            ays.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.sin(theta))
            axs.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.cos(theta))

        for codrone in self.codrones:
            d = np.sqrt((codrone.x - self.x) ** 2 + (codrone.y - self.y) ** 2)
            theta = np.arctan2(self.y - codrone.y, self.x - codrone.x)

            ays.append(d * self.k_fardrone * codrone.activity * np.sin(theta))
            axs.append(d * self.k_fardrone * codrone.activity * np.cos(theta))

        ax = sum(axs)
        ay = sum(ays)
        a = min(np.sqrt(ay ** 2 + ax ** 2), a_max)
        if np.random.random() < self.p_random and a <=100:
            self.heading += 2 * 90 / 57.3 * self.k_random * np.random.random() - 90 / 57.3 * self.k_random


        angle = np.arctan2(ay, ax)

        self.ax = a * np.cos(angle)
        self.ay = a * np.sin(angle)

        vx = self.speed * np.cos(self.heading) + self.ax * dt
        vy = self.speed * np.sin(self.heading) + self.ay * dt

        self.heading = np.arctan2(vy, vx)
        self.speed = max(min(np.sqrt(vy**2 + vx**2), v_max), self.v_min)




        # Heading periodicity
        if self.heading >= 2 * np.pi:
            self.heading -= 2 * np.pi
        elif self.heading < 0:
            self.heading += 2 * np.pi

        # Integration
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * dt, 0))
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * dt, 0))

        # Position periodicity
        if self.x > width:
            self.x -= width
        if self.x < 0:
            self.x += width

        if self.y > height:
            self.y -= height
        if self.y < 0:
            self.y += height

        #print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1))

        self.activity = max(-5, self.activity - 0.5)


