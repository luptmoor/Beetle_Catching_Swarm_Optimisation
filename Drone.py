import numpy as np
from PhysicalObject import PhysicalObject
from settings import *


class Drone(PhysicalObject):
    def __init__(self, name, type, x, y, r_col=r_drone, r_vis=r_drone_vision):
        super().__init__(name, type, x, y, r_col)
        self.visible_phobjects = []
        self.speed = v_min
        self.ax = 0
        self.ay = 0
        self.heading = np.random.random() * 2 * np.pi
        self.r_vis = r_vis

        # Tunable Parameters
        self.k_tree = 0.6
        self.k_drone = 0.5
        self.k_bug = -0.7
        self.gains = {'tree': self.k_tree, 'drone': self.k_drone, 'bug': self.k_bug}

        self.k_random = 0.0


    def advance(self, dt):
        axs = []
        ays = []

        for phobject in self.visible_phobjects:
            d = np.sqrt((phobject.x - self.x)**2 + (phobject.y - self.y)**2) - phobject.r_col
            theta = np.arctan2(self.y - phobject.y, self.x - phobject.x)

            ays.append((max(self.r_vis - d, 0)) * self.gains[phobject.type] * np.sin(theta))
            axs.append((max(self.r_vis - d, 0)) * self.gains[phobject.type] * np.cos(theta))

        ay = sum(ays) + np.random.random() * 2 * a_max * self.k_random - self.k_random * a_max
        ax = sum(axs) + np.random.random() * 2 * a_max * self.k_random - self.k_random * a_max

        a = min(np.sqrt(ay**2 + ax**2), a_max)
        angle = np.arctan2(ay, ax)

        self.ax = a * np.cos(angle)
        self.ay = a * np.sin(angle)

        vx = self.speed * np.cos(self.heading) + self.ax * dt
        vy = self.speed * np.sin(self.heading) + self.ay * dt

        self.heading = np.arctan2(vy, vx)
        self.speed = max(min(np.sqrt(vy**2 + vx**2), v_max), v_min)




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

