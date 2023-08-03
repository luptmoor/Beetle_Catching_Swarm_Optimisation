import numpy as np
from PhysicalObject import PhysicalObject
from Bug import Bug
from Drone import Drone
from Visuals import Visuals
from settings import *


class Simulation:
    def __init__(self, params):
        self.score = 0

        # Lists
        self.phobjects = []
        self.trees = []
        self.drones = []
        self.charging = []
        self.bugs = []

        self.params = params

    def check_collision(self, obj1, obj2, margin=0):
        if obj1 is None or obj2 is None:
            return False

        if obj1.name == obj2.name:
            return False

        if np.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) <= obj1.r_col + obj2.r_col + margin:
            return True
        else:
            return False

    def check_bug_vision(self, active, passive):
        if active is None or passive is None:
            return False

        if active.name == passive.name:
            return False

        # if passive in bugs or passive in drones and True:
        #     ds = np.zeros(9)
        #     ds[0] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - (passive.y - height)) ** 2)
        #     ds[1] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - (passive.y - height)) ** 2)
        #     ds[2] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - (passive.y - height)) ** 2)
        #     ds[3] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - passive.y) ** 2)
        #     ds[4] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - passive.y) ** 2)
        #     ds[5] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - passive.y) ** 2)
        #     ds[6] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - (passive.y + height)) ** 2)
        #     ds[7] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - (passive.y + height)) ** 2)
        #     ds[8] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - (passive.y + height)) ** 2)
        #     d = np.min(ds)
        # else:
        d = np.sqrt((active.x - passive.x) ** 2 + (active.y - passive.y) ** 2)

        if d <= active.r_vis + passive.r_col:
            return True
        else:
            return False

    def check_drone_vision(self, active, passive):
        if active is None or passive is None:
            return False

        if active.name == passive.name:
            return False

        # if passive in bugs or passive in drones and True:
        #     ds = np.zeros(9)
        #     ds[0] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - (passive.y - height)) ** 2)
        #     ds[1] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - (passive.y - height)) ** 2)
        #     ds[2] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - (passive.y - height)) ** 2)
        #     ds[3] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - passive.y) ** 2)
        #     ds[4] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - passive.y) ** 2)
        #     ds[5] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - passive.y) ** 2)
        #     ds[6] = np.sqrt((active.x - (passive.x - width)) ** 2 +     (active.y - (passive.y + height)) ** 2)
        #     ds[7] = np.sqrt((active.x - passive.x) ** 2 +               (active.y - (passive.y + height)) ** 2)
        #     ds[8] = np.sqrt((active.x - (passive.x + width)) ** 2 +     (active.y - (passive.y + height)) ** 2)
        #     d = np.min(ds)
        # else:
        d = np.sqrt((active.x - passive.x) ** 2 + (active.y - passive.y) ** 2)

        if d <= active.r_vis[passive.type] + passive.r_col:
            return True
        else:
            return False

    def load_environment(self):

        # Place trees
        for i in range(N_TREES):
            placing = True
            while placing:
                x = np.random.random() * (WIDTH - 2 * (R_TREE + TREE_MIN_DIST)) + (R_TREE + TREE_MIN_DIST) // 1
                y = np.random.random() * (HEIGHT - 2 * (R_TREE + TREE_MIN_DIST)) + (R_TREE + TREE_MIN_DIST) // 1

                newtree = PhysicalObject('Tree ' + str(i), 'tree', x, y, R_TREE)
                if not any([self.check_collision(newtree, phobject, TREE_MIN_DIST) for phobject in self.phobjects]):
                    self.phobjects.append(newtree)
                    self.trees.append(newtree)
                    print(newtree.name, 'placed!')
                    placing = False
                else:
                    pass

        # Place bugs
        for j in range(N_BUGS):
            placing = True
            while placing:
                x = (np.random.random() * WIDTH) // 1
                y = (np.random.random() * HEIGHT) // 1

                newbug = Bug('Bug ' + str(j), x, y)
                if not any([self.check_collision(newbug, phobject) for phobject in self.phobjects]):
                    self.phobjects.append(newbug)
                    self.bugs.append(newbug)
                    print(newbug.name, 'placed!')
                    placing = False
                else:
                    pass

        # Place drones
        for k in range(N_DRONES):
            placing = True
            while placing:
                x = (np.random.random() * WIDTH * LAUNCHPAD_FRAC) // 1
                y = (np.random.random() * HEIGHT * LAUNCHPAD_FRAC) // 1

                newdrone = Drone('Drone ' + str(k), 'drone', x, y, self.params)
                if not any([self.check_collision(newdrone, phobject, DRONE_MIN_DIST) for phobject in self.phobjects]):
                    self.phobjects.append(newdrone)
                    self.drones.append(newdrone)
                    print(newdrone.name, 'placed!')
                    placing = False
                else:
                    pass

    # def collision_loop():
    #     """
    #     loops over drones and checks for collisions with other phobjects.
    #     note: instances need to be the same in drones list and phobjects list!
    #     :return: void
    #     """
    #

    def evaluate(self, mode, t):
        if mode == 1:
            return t - 450
        if mode == 2:
            return 450 - t
        if mode == 3:
            return 300 * len(self.drones) / N_DRONES - 150

    # if __name__ == 'main' and True:
    def run(self):
        self.load_environment()
        visuals = Visuals(WIDTH, HEIGHT, DT)
        running = True
        t = 0

        while running:
            if t // 1 % 5 == 0:
                print()
                print('Time:', round(t, 2), 's')

            # Guarantee this always holds (good candidate for removal if too slow)
            self.phobjects = self.trees + self.bugs + self.drones

            # Bug simulation
            for bug in self.bugs:
                for tree in self.trees:
                    if self.check_collision(bug, tree):
                        bug.mode = 'tree'
                    if self.check_bug_vision(bug, tree):
                        bug.processVisual('tree', tree.x, tree.y)

                for drone in self.drones:
                    # if not any([check_vision(bug, drone) for drone in drones]):
                    #     bug.processVisual('none')
                    if self.check_bug_vision(bug, drone):
                        bug.processVisual('drone', drone.x, drone.y)

                repro = bug.advance(DT)
                if repro:
                    newbug = Bug(bug.name + ' (' + str(t) + 's)', bug.x, bug.y)
                    self.bugs.append(newbug)
                    self.phobjects.append(newbug)

            # Drone simulation
            for drone in self.drones:
                drone.codrones = [otherdrone for otherdrone in self.drones if not otherdrone == drone]

                for phobject in self.phobjects:
                    # Maintain list of visible phobjects
                    if self.check_drone_vision(drone, phobject) and phobject not in drone.visible_phobjects:
                        drone.visible_phobjects.append(phobject)
                    if not self.check_drone_vision(drone, phobject) and phobject in drone.visible_phobjects:
                        drone.visible_phobjects.remove(phobject)

                for phobject in drone.visible_phobjects:
                    if phobject not in self.phobjects:
                        drone.visible_phobjects.remove(phobject)

                    # Check collisions
                    if self.check_collision(drone, phobject):
                        print('Collision between ', drone.name, 'and', phobject.name)
                        if phobject in self.drones:
                            self.drones.remove(drone)
                            self.drones.remove(phobject)
                            self.phobjects.remove(drone)
                            self.phobjects.remove(phobject)
                        elif phobject in self.bugs:
                            self.bugs.remove(phobject)
                            self.phobjects.remove(phobject)
                            drone.activity += ACTIVITY_AWARD
                        elif phobject in self.trees:
                            self.drones.remove(drone)
                            self.phobjects.remove(drone)

                recharge = drone.advance(DT)
                if recharge:
                    self.drones.remove(drone)
                    self.charging.append(drone)

            for drone in self.charging:
                drone.charge = min(drone.charge + CHARGE_RATE * DT, 100)
                if drone.charge >= 100:
                    drone.x = 0
                    drone.y = 0
                    self.drones.append(drone)
                    self.charging.remove(drone)

            visuals.update(self.trees, self.bugs, self.drones, self.charging)

            t += DT

            # End conditions
            # if not bugs:
            #     score = evaluate(1, t)
            #     break
            # if not drones:
            #     score = evaluate(2, t)
            #     break
            if t >= T_MAX:
                self.score = self.evaluate(3, t)
                break

        print(self.score)



