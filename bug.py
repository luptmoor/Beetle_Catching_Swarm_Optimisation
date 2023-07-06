import matplotlib.pyplot as plt

from main import PhysicalObject, dXmax_bug, r_bug_vision
import numpy as np

tree_land_prob = 0.66
escape_prob = 0.80
lift_prob = 0.10

bug_speed = 2



class Bug(PhysicalObject):
    def __init__(self, name, x, y, r_col, speed=bug_speed, heading=0, r_vis=r_bug_vision, mode='idle'):
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
        super().__init__(name, x, y, r_col)
        self.heading = heading
        self.speed = speed
        self.r_vis = r_vis
        self.mode = mode
        self.tree_cooldown = 0

        print(self.name, 'in', self.mode, 'mode created')

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
            self.heading += np.random.random() * 2 * dXmax_bug - dXmax_bug
            self.tree_cooldown = max(self.tree_cooldown - 1, 0)

        # Bug sits on tree (v)
        elif self.mode == 'tree':
            self.speed = 0
            if np.random.random() < lift_prob:
                self.tree_cooldown = 15
                self.speed = bug_speed
                self.mode = 'idle'


        # Heading periodicity and integration
        if self.heading >= 2 * np.pi:
            self.heading -= 2 * np.pi
        elif self.heading < 0:
            self.heading += 2 * np.pi
        self.x = int(round(self.x + self.speed * np.cos(self.heading) * dt, 0))
        self.y = int(round(self.y + self.speed * np.sin(self.heading) * dt, 0))
        print(self.name, '@', self.x, self.y, '(heading: ', round(self.heading * 57.3, 1), ') in mode:', self.mode)

    def processVisual(self, cue, x, y):

        # Bug sees a new tree (v)
        if self.mode == 'idle' and cue == 'tree' and self.tree_cooldown == 0:
            if np.random.random() < tree_land_prob:
                self.mode = 'land'
            else:
                self.tree_cooldown = 10

        # Bug sees a drone already identified (v)
        elif self.mode == 'land' and cue == 'tree':
            self.heading = np.arctan2(y - self.y, x - self.x)  # attracting heading

        # Bug sees a new drone (v)
        elif self.mode == 'idle' and cue == 'drone' and np.random.random() < escape_prob:
            self.mode = 'escape'

        # Bug sees a drone already identified (v)
        elif self.mode == 'escape' and cue == 'drone':
            self.heading = np.arctan2(self.y - y, self.x - x)  # opposing heading




######## Verification ###############

tree = PhysicalObject('Tree', 10, 10, 20)
bug = Bug("Bug", 50, 50, 1, mode='tree')
dt = 1
xs = []
ys = []
running = True

while running:
    bug.advance(dt)
    xs.append(bug.x)
    ys.append(bug.y)
    cue = str(input('Cue: '))

    if cue =='q':
        running = False
    elif not cue == 'c':
        x = int(input('x: '))
        y = int(input('y: '))

        bug.processVisual(cue, x, y)
    else:
        pass

plt.scatter(xs, ys)
plt.show()



