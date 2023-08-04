import numpy as np
from PhysicalObject import PhysicalObject
from settings import *


class Drone(PhysicalObject):
    def __init__(self, name, type, x, y, params, r_col=R_DRONE):
        super().__init__(name, type, x, y, r_col)



        self.p_random = 0.1
        self.k_random = 0.4

        # Tunable Parameters, negative ks mean attraction, positive means repulsion
        self.r_vis_bug = params[0] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG
        self.r_vis_drone = params[1] * RANGE_R_VIS_DRONE / 2 + MU_R_VIS_DRONE
        self.r_vis_tree = params[2] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE
        self.r_vis = {'tree': self.r_vis_tree, 'drone': self.r_vis_drone, 'bug': self.r_vis_bug}

        self.k_tree = params[3] * RANGE_K_TREE / 2 + MU_K_TREE
        self.k_neardrone = params[4] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE
        self.k_bug = params[5] * RANGE_K_BUG / 2 + MU_K_BUG
        self.gains = {'tree': self.k_tree, 'drone': self.k_neardrone, 'bug': self.k_bug}

        self.k_fardrone = params[6] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE
        self.k_activity = params[7]  * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY

        self.v_min = params[8] * RANGE_V_MIN / 2 + MU_V_MIN

        self.temp_cohesion = params[9] * RANGE_TEMP_COHESION / 2 + MU_TEMP_COHESION


        self.activity = 0
        self.charge = round(np.random.random() * (100 - self.temp_cohesion) + self.temp_cohesion, 1)

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

            # Local attraction/repulsion from other phobjects
            ays.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.sin(theta))
            axs.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.cos(theta))

        for codrone in self.codrones:
            d = np.sqrt((codrone.x - self.x) ** 2 + (codrone.y - self.y) ** 2)
            theta = np.arctan2(self.y - codrone.y, self.x - codrone.x)

            # Attraction towards activity
            ays.append(d * self.k_activity * codrone.activity * np.sin(theta))
            axs.append(d * self.k_activity * codrone.activity * np.cos(theta))

            # Attraction towards other drones
            ays.append(d * self.k_fardrone * np.sin(theta))
            axs.append(d * self.k_fardrone * np.cos(theta))

        ax = sum(axs)
        ay = sum(ays)
        a = min(np.sqrt(ay ** 2 + ax ** 2), A_DRONE_MAX)
        if np.random.random() < self.p_random and a <= 100:
            self.heading += 2 * 90 / 57.3 * self.k_random * np.random.random() - 90 / 57.3 * self.k_random


        angle = np.arctan2(ay, ax)

        self.ax = a * np.cos(angle)
        self.ay = a * np.sin(angle)

        vx = self.speed * np.cos(self.heading) + self.ax * dt
        vy = self.speed * np.sin(self.heading) + self.ay * dt

        self.heading = np.arctan2(vy, vx)
        self.speed = max(min(np.sqrt(vy**2 + vx**2), V_DRONE_MAX), self.v_min)




        # Heading periodicity
        if self.heading >= 2 * np.pi:
            self.heading -= 2 * np.pi
        elif self.heading < 0:
            self.heading += 2 * np.pi

        # Integration
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * dt, 0))
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * dt, 0))

        # Position periodicity
        if self.x > WIDTH:
            self.x -= WIDTH
        if self.x < 0:
            self.x += WIDTH

        if self.y > HEIGHT:
            self.y -= HEIGHT
        if self.y < 0:
            self.y += HEIGHT

        #print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1))

        self.activity = min(50, max(-50, self.activity - ACTIVITY_DECAY * dt))
        self.charge = max(0, self.charge - CHARGE_RATE * dt)

        if self.charge == 0:
            return True
        else:
            return False



