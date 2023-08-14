import numpy as np
from PhysicalObject import PhysicalObject
from settings import *


class Drone(PhysicalObject):
    def __init__(self, name, type, x, y, params, r_col=R_DRONE):
        super().__init__(name, type, x, y, r_col)

        # Tunable Parameters, negative ks mean attraction, positive means repulsion
        self.r_vis_bug = int(round(params[0] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG, 0))
        self.r_vis_neardrone = int(round(params[1] * RANGE_R_VIS_NEARDRONE / 2 + MU_R_VIS_NEARDRONE))
        self.r_vis_tree = int(round(params[2] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE))
        self.r_vis = {'tree': self.r_vis_tree, 'drone': self.r_vis_neardrone, 'bug': self.r_vis_bug}

        self.k_tree = params[3] * RANGE_K_TREE / 2 + MU_K_TREE
        self.k_neardrone = params[4] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE
        self.k_bug = params[5] * RANGE_K_BUG / 2 + MU_K_BUG
        self.gains = {'tree': self.k_tree, 'drone': self.k_neardrone, 'bug': self.k_bug}

        self.r_fardrone = params[6] * RANGE_R_VIS_FARDRONE / 2 + MU_R_VIS_FARDRONE
        self.k_fardrone = params[7] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE
        self.k_activity = params[8]  * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY

        self.v_min = min(V_DRONE_MAX, max(0, params[9] * RANGE_V_MIN / 2 + MU_V_MIN))
        self.v_max = min(V_DRONE_MAX, max(self.v_min, params[10] * RANGE_V_MAX / 2 + MU_V_MAX))

        self.carefulness = params[11] * RANGE_CAREFULNESS / 2 + MU_CAREFULNESS


        self.activity = 0

        self.visible_phobjects = []
        self.codrones = []
        self.speed = self.v_min
        self.ax = 0
        self.ay = 0
        self.heading = np.random.random() * 2 * np.pi


    def advance(self):
        axs = []
        ays = []

        for phobject in self.visible_phobjects:
            # Distance
            dx = np.abs(self.x - phobject.x)
            dy = np.abs(self.y - phobject.y)
            dx = min(dx, WIDTH - dx)
            dy = min(dy, HEIGHT - dy)
            d = np.sqrt(dx ** 2 + dy ** 2) - phobject.r_col


            #Heading
            dx = phobject.x - self.x
            dy = phobject.y - self.y

            if abs(dx) > WIDTH / 2:
                dx = WIDTH - dx
            if abs(dy) > HEIGHT / 2:
                dy = HEIGHT - dy
            theta = np.arctan2(-dy, -dx)


            # Local attraction/repulsion from other phobjects
            ays.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.sin(theta))
            axs.append((max(self.r_vis[phobject.type] - d, 0)) * self.gains[phobject.type] * np.cos(theta))

        for codrone in self.codrones:
            dx = np.abs(self.x - codrone.x)
            dy = np.abs(self.y - codrone.y)
            dx = min(dx, WIDTH - dx)
            dy = min(dy, HEIGHT - dy)
            d = np.sqrt(dx ** 2 + dy ** 2)
            theta = np.arctan2(self.y - codrone.y, self.x - codrone.x)

            # Attraction towards activity
            ays.append(d * self.k_activity * codrone.activity * np.sin(theta))
            axs.append(d * self.k_activity * codrone.activity * np.cos(theta))

            # Attraction towards other drones within a radius that determines the subflock size
            ays.append(max(0, self.r_fardrone - d) * self.k_fardrone * np.sin(theta))
            axs.append(max(0, self.r_fardrone - d) * self.k_fardrone * np.cos(theta))

        ax = sum(axs)
        ay = sum(ays)
        a = min(np.sqrt(ay ** 2 + ax ** 2), A_DRONE_MAX)

        if a <= 5:
            self.speed = (1 - self.carefulness) * self.speed

        angle = np.arctan2(ay, ax)

        self.ax = a * np.cos(angle)
        self.ay = a * np.sin(angle)

        vx = self.speed * np.cos(self.heading) + self.ax * DT
        vy = self.speed * np.sin(self.heading) + self.ay * DT

        self.heading = np.arctan2(vy, vx) % (2 * np.pi)
        self.speed = max(min(np.sqrt(vy**2 + vx**2), self.v_max), self.v_min)


        # Integration
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * DT, 0)) % WIDTH
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * DT, 0)) % HEIGHT


        #print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1))

        self.activity = min(50, max(-50, self.activity - ACTIVITY_DECAY * DT))




