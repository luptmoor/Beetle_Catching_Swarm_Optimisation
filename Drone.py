import numpy as np
from Entity import Entity
from settings import *


class Drone(Entity):
    def __init__(self, name, type, x, y, params, r_col=R_DRONE):
        super().__init__(name, type, x, y, r_col)

        # Tunable Parameters, negative ks mean attraction, positive means repulsion
        self.r_vis_tree = int(round(params[0] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE))
        self.k_tree = params[1] * RANGE_K_TREE / 2 + MU_K_TREE

        self.r_vis_bug = int(round(params[2] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG, 0))
        self.k_bug = params[3] * RANGE_K_BUG / 2 + MU_K_BUG

        self.r_vis_neardrone = int(round(params[4] * RANGE_R_VIS_NEARDRONE / 2 + MU_R_VIS_NEARDRONE))
        self.k_neardrone = params[5] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE

        self.r_vis = {'tree': self.r_vis_tree, 'drone': self.r_vis_neardrone, 'bug': self.r_vis_bug}
        self.gains = {'tree': self.k_tree, 'drone': self.k_neardrone, 'bug': self.k_bug}

        self.r_fardrone = params[6] * RANGE_R_VIS_FARDRONE / 2 + MU_R_VIS_FARDRONE
        self.k_fardrone = params[7] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE

        self.r_activity = params[8] * RANGE_R_ACTIVITY / 2 + MU_R_ACTIVITY
        self.k_activity = params[9]  * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY

        self.v_min = min(V_DRONE_MAX, max(0, params[10] * RANGE_V_MIN / 2 + MU_V_MIN))
        self.v_max = min(V_DRONE_MAX, max(self.v_min, params[11] * RANGE_V_MAX / 2 + MU_V_MAX))

        self.c = params[12] * RANGE_C / 2 + MU_C


        # Initialisation
        self.activity = 0
        self.visible_entities = []
        self.codrones = []
        self.speed = self.v_min
        self.ax = 0
        self.ay = 0
        self.heading = np.random.random() * 2 * np.pi

    def sees(self, entity):
        if entity is None:
            return False

        if entity == self:
            return False

        dx = np.abs(self.x - entity.x)
        dy = np.abs(self.y - entity.y)
        dx = min(dx, WIDTH - dx)
        dy = min(dy, HEIGHT - dy)

        d = np.sqrt(dx ** 2 + dy ** 2)
        obstructed = False
        if entity.type == 'bug' and entity.tree is not None:
            d_obs = np.sqrt((self.x - entity.tree.x) ** 2 + (self.y - entity.tree.y) ** 2)
            if d_obs < d:
                obstructed = True

        if d <= self.r_vis[entity.type] + entity.r_col and not obstructed:
            return True
        else:
            return False

    def advance(self):
        axs = []
        ays = []

        self.activity = 0
        for entity in self.visible_entities:
            if entity.type == 'bug':
                self.activity += 1

            # Distance
            dx = np.abs(self.x - entity.x)
            dy = np.abs(self.y - entity.y)
            dx = min(dx, WIDTH - dx)
            dy = min(dy, HEIGHT - dy)
            d = np.sqrt(dx ** 2 + dy ** 2) - entity.r_col


            #Heading
            dx = entity.x - self.x
            dy = entity.y - self.y

            if abs(dx) > WIDTH / 2:
                dx = WIDTH - dx
            if abs(dy) > HEIGHT / 2:
                dy = HEIGHT - dy
            theta = np.arctan2(-dy, -dx)


            # Local attraction/repulsion from other entities
            ays.append((max(self.r_vis[entity.type] - d, 0)) * self.gains[entity.type] * np.sin(theta))
            axs.append((max(self.r_vis[entity.type] - d, 0)) * self.gains[entity.type] * np.cos(theta))

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

        angle = np.arctan2(ay, ax)

        self.ax = a * np.cos(angle)
        self.ay = a * np.sin(angle)

        vx = self.speed * np.cos(self.heading) + self.ax * DT
        vy = self.speed * np.sin(self.heading) + self.ay * DT

        self.heading = np.arctan2(vy, vx) % (2 * np.pi)
        self.speed = max(min(np.sqrt(vy**2 + vx**2), self.v_max), self.v_min)

        if a <= 0.05 * A_DRONE_MAX:
            self.speed = max((1 - self.c) * self.speed, self.speed - A_DRONE_MAX * DT)


        # Integration
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * DT, 0)) % WIDTH
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * DT, 0)) % HEIGHT


        #print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1))




