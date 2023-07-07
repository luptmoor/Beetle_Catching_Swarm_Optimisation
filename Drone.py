import numpy as np
from PhysicalObject import PhysicalObject
from settings import *


class Drone(PhysicalObject):
    def __init__(self, name, x, y, r_col=r_drone, r_vis=r_drone_vision):
        super().__init__(name, x, y, r_col)
        self.visible_phobjects = []
        self.speed = v_drone
        self.heading = np.random.random() * 2 * np.pi
        self.r_vis = r_vis


    def advance(self, dt):
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

        print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1))

