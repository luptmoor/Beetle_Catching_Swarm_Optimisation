import matplotlib.pyplot as plt

from PhysicalObject import *
from settings import *
import numpy as np





class Bug(PhysicalObject):
    def __init__(self, name, x, y, speed=V_BUG, r_vis=R_VIS_BUG, mode='idle'):
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
        super().__init__(name, 'bug', x, y, R_BUG)
        self.heading = np.random.random() * 2 * np.pi
        self.speed = speed
        self.r_vis = r_vis
        self.mode = mode
        self.tree = None

        #print(self.name, 'in', self.mode, 'mode created')

    def setSpeed(self, speed):
        self.speed = speed

    def setHeading(self, heading):
        self.heading = heading

    def advance(self, dt):
        """
        performs the integration of the bug's behaviour according to its current mode
        :param dt:
        :return: void
        """
        # Bug idles (v)
        if self.mode == 'idle':
            self.heading += (np.random.random() * 2 * BUG_RANDOMNESS - BUG_RANDOMNESS) * dt

        # Bug sits on tree (v)
        elif self.mode == 'tree':
            self.speed = 0
            self.heading = np.arctan2(self.y - self.tree.y, self.x - self.tree.x)  # bug faces away from tree
            if np.random.random() < TAKEOFF_PROB:
                self.speed = V_BUG
                self.tree = None
                self.mode = 'idle'
            elif np.sqrt((self.x - self.tree.x)**2 + (self.y - self.tree.y)**2) < self.tree.r_col:
                self.x = self.tree.x + self.tree.r_col * np.cos(self.heading)
                self.y = self.tree.y + self.tree.r_col * np.sin(self.heading)
            # elif np.random.random() < REPRO_PROB:
            #     self.speed = V_BUG
            #     self.mode = 'idle'
            #     return True


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

        return False
        #print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1), ') in mode:', self.mode)

    def processVisual(self, cue):

        # Bug sees a new tree only while idling (v)
        if self.mode == 'idle' and cue.type == 'tree' and np.random.random() < TREE_LAND_PROB:
            self.mode = 'land'

        # Bug sees a tree already identified (v)
        elif self.mode == 'land' and cue.type == 'tree':
            self.heading = np.arctan2(cue.y - self.y, cue.x - self.x)  # attracting heading

        # Bug sees the tree it is sitting on, turns away to start
        elif self.mode == 'tree' and cue.type == 'tree':
            pass

        elif cue is None:
            self.mode = 'idle'


        # Bug sees a new drone while idling or landing (v)
        elif (self.mode == 'idle' or self.mode == 'land') and cue.type == 'drone' and np.random.random() < ESCAPE_PROB:
            self.mode = 'escape'

        # Bug sees a new drone while sitting on tree -> first goes to idle, escaping both tree and drone
        elif self.mode == 'tree' and cue.type == 'drone' and np.random.random() < ESCAPE_PROB:
            self.heading = (self.heading + np.arctan2(self.y - cue.y, self.x - cue.x)) / 2
            self.speed = V_BUG
            self.tree = None
            self.mode = 'idle'

        # Bug sees a drone already identified (v)
        elif self.mode == 'escape' and cue.type == 'drone':
            self.heading = np.arctan2(self.y - cue.y, self.x - cue.x)  # repelling heading




######## Verification ###############
#
# tree = PhysicalObject('Tree', 10, 10, 20)
# bug = Bug("Bug", 50, 50, 1, mode='tree')
# dt = 1
# xs = []
# ys = []
# running = True
#
# while running:
#     bug.advance(dt)
#     xs.append(bug.x)
#     ys.append(bug.y)
#     cue = str(input('Cue: '))
#
#     if cue =='q':
#         running = False
#     elif not cue == 'c':
#         x = int(input('x: '))
#         y = int(input('y: '))
#
#         bug.processVisual(cue, x, y)
#     else:
#         pass
#
# plt.scatter(xs, ys)
# plt.show()
#
#
#
