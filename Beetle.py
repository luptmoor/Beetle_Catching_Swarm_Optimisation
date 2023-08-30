import matplotlib.pyplot as plt

from Entity import *
from settings import *
import numpy as np





class Beetle(Entity):
    def __init__(self, name, x, y, speed=V_BEETLE, r_vis=R_VIS_BEETLE, mode='idle'):
        """
        Simulated Bug
        :param name:
        :param x:
        :param y:
        :param r_col:
        :param speed:
        :param heading:
        :param r_vis:
        :param mode:
        """
        super().__init__(name, 'bug', x, y, R_BEETLE)
        self.heading = np.random.random() * 2 * np.pi
        self.speed = speed
        self.r_vis = r_vis
        self.mode = mode
        self.tree = None

        #print(self.name, 'in', self.mode, 'mode created')

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

        if d <= self.r_vis + entity.r_col:
            return True
        else:
            return False

    def advance(self, dt):
        """
        performs the integration of the bug's behaviour according to its current mode
        :param dt: timestep size, is variable because bugs perform half the step size twice
        :return: None
        """
        # Bug idles and changes direction randomly
        if self.mode == 'idle':
            self.heading += (np.random.random() * 2 * BEETLE_RANDOMNESS - BEETLE_RANDOMNESS) * dt

        # Bug escapes and changes direction less randomly
        elif self.mode == 'escape':
            self.heading += (np.random.random() * 2 * 0.3 * BEETLE_RANDOMNESS - 0.3 * BEETLE_RANDOMNESS) * dt

        # Bug sits on tree
        elif self.mode == 'tree':
            self.speed = 0
            self.heading = np.arctan2(self.y - self.tree.y, self.x - self.tree.x)  # bug faces away from tree

            # Bug randomly takes off from tree
            if np.random.random() < TAKEOFF_PROB * noise(NOISE) * dt:
                self.speed = V_BEETLE
                self.tree = None
                self.mode = 'idle'
            # Ensure that bug always sits on the bark of tree
            elif np.sqrt((self.x - self.tree.x)**2 + (self.y - self.tree.y)**2) < self.tree.r_col:
                self.x = self.tree.x + self.tree.r_col * np.cos(self.heading)
                self.y = self.tree.y + self.tree.r_col * np.sin(self.heading)


        # Heading periodicity
        self.heading = self.heading % (2 * np.pi)

        # Motion integration
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * dt, 0)) % WIDTH
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * dt, 0)) % HEIGHT

    def processVisual(self, cue):
        # Bug sees a new tree only while idling and goes to land mode
        if self.mode == 'idle' and cue.type == 'tree' and np.random.random() < TREE_LAND_PROB * noise(NOISE) * DT:
            self.mode = 'land'

        # Bug sees a tree already identified
        elif self.mode == 'land' and cue.type == 'tree':
            dx = cue.x - self.x
            dy = cue.y - self.y
            if abs(dx) > WIDTH / 2:
                dx = WIDTH - dx
            if abs(dy) > HEIGHT / 2:
                dy = HEIGHT - dy

            self.heading = np.arctan2(dy, dx)  # attracting heading


        # Bug sees a new drone while idling or landing (
        elif (self.mode == 'idle' or self.mode == 'land') and cue.type == 'drone' and np.random.random() < ESCAPE_PROB * noise(NOISE) * DT:
            self.mode = 'escape'

        # Bug sees a new drone while sitting on tree -> first goes to idle, escaping both tree and drone
        elif self.mode == 'tree' and cue.type == 'drone':
            dx = self.x - cue.x
            dy = self.y - cue.y
            if abs(dx) > WIDTH / 2:
                dx = WIDTH - dx
            if abs(dy) > HEIGHT / 2:
                dy = HEIGHT - dy

            # Bug flies half the angle between tree (its current heading) and the drone
            self.heading = (self.heading + np.arctan2(dy, dx)) / 2
            self.speed = V_BEETLE
            self.tree = None
            self.mode = 'idle'

        # Bug sees a drone already identified (v)
        elif self.mode == 'escape' and cue.type == 'drone':
            dx = self.x - cue.x
            dy = self.y - cue.y
            if abs(dx) > WIDTH / 2:
                dx = WIDTH - dx
            if abs(dy) > HEIGHT / 2:
                dy = HEIGHT - dy

            self.heading = np.arctan2(dy, dx)  # attracting heading
