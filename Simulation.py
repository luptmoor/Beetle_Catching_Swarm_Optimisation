import numpy as np
from Entity import Entity
from Bug import Bug
from Drone import Drone
from Visuals import Visuals
from settings import *


def F_time(x):
    """
    Mathematical transfer function for time criterion.
    :param x: (float) function argument.
    :return: (float) partial fitness.
    """
    return 1 - 0.3 * x ** 2


def F_bugs(x):
    """
    Mathematical transfer function for "bugs killed" criterion.
    :param x: (float) function argument.
    :return: (float) partial fitness.
    """
    a = 0.3
    # return a ** 2 / ((1 - x) ** 2 + a ** 2)
    return x ** 2


def F_drones(x):
    """
    Mathematical transfer function for "drones died" criterion.
    :param x: (float) function argument.
    :return: (float) partial fitness.
    """
    a = 0.08
    return a ** 2 / (x ** 2 + a ** 2)


def check_collision(obj1, obj2, margin=0):
    if obj1 is None or obj2 is None:
        return False

    if obj1.name == obj2.name:
        return False

    if np.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) <= obj1.r_col + obj2.r_col + margin:
        return True
    else:
        return False





def check_drone_vision(active, passive):
    if active is None or passive is None:
        return False

    if active.name == passive.name:
        return False

    dx = np.abs(active.x - passive.x)
    dy = np.abs(active.y - passive.y)
    dx = min(dx, WIDTH - dx)
    dy = min(dy, HEIGHT - dy)

    d = np.sqrt(dx**2 + dy**2)
    obstructed = False
    if passive.type == 'bug' and passive.tree is not None:
        d_obs = np.sqrt((active.x - passive.tree.x) ** 2 + (active.y - passive.tree.y) ** 2)
        if d_obs < d:
            obstructed = True


    if d <= active.r_vis[passive.type] + passive.r_col and not obstructed:
        return True
    else:
        return False


class Simulation:
    """
    Class holding all the functions and parameters for a single simulation instance.
    """
    def __init__(self, params, seed=42, visualise=False):
        self.score = 0
        self.t = 0

        # Lists holding simulated entities
        self.entities = []
        self.trees = []
        self.drones = []
        self.bugs = []

        self.params = params  # tunable parameters chosen for this particular simulation to be evaluated
        self.seed = seed  # seed for random number generator
        self.visualise = visualise  # boolean determining if visualisation should be shown

        if visualise:
            self.visuals = Visuals(WIDTH, HEIGHT, DT)

    def load_environment(self):

        # Place trees
        for i in range(N_TREES):
            placing = True
            while placing:
                x = np.random.random() * (WIDTH - 2 * TREE_MIN_DIST) + TREE_MIN_DIST // 1
                y = np.random.random() * (HEIGHT - 2 * TREE_MIN_DIST) + TREE_MIN_DIST // 1

                newtree = Entity('Tree ' + str(i), 'tree', x, y, round(np.random.normal(R_TREE_AVG, R_TREE_STD), 0))
                if not any([check_collision(newtree, entity, TREE_MIN_DIST) for entity in self.entities]):
                    self.entities.append(newtree)
                    self.trees.append(newtree)
                    # print(newtree.name, 'placed!')
                    placing = False


        # Place bugs
        for j in range(N_BUGS):
            placing = True
            while placing:
                x = (np.random.random() * WIDTH) // 1
                y = (np.random.random() * HEIGHT) // 1

                newbug = Bug('Bug ' + str(j), x, y)
                if not any([check_collision(newbug, entity) for entity in self.entities]):
                    self.entities.append(newbug)
                    self.bugs.append(newbug)
                    # print(newbug.name, 'placed!')
                    placing = False


        # Place drones
        for k in range(N_DRONES):
            placing = True
            while placing:
                x = (np.random.random() * WIDTH * LAUNCHPAD_FRAC) // 1
                y = (np.random.random() * HEIGHT * LAUNCHPAD_FRAC) // 1

                newdrone = Drone('Drone ' + str(k), 'drone', x, y, self.params)
                if not any([check_collision(newdrone, entity, DRONE_MIN_DIST) for entity in self.entities]):
                    self.entities.append(newdrone)
                    self.drones.append(newdrone)
                    # print(newdrone.name, 'placed!')
                    placing = False



    def evaluate(self):
        score = F_drones(len(self.drones) / N_DRONES) * F_bugs(1 - len(self.bugs) / N_BUGS) * F_time(self.t / T_MAX)
        return score


    def run(self):
        np.random.seed(self.seed)
        self.load_environment()
        running = True

        while running:

            if int(round(self.t, 0)) % 10 == 0 and abs(int(round(self.t, 0)) - self.t) < 0.001:
                print('Seed:', self.seed, 'Time:', round(self.t, 0), 's')

            # Guarantee this always holds (good candidate for removal if too slow)
            self.entities = self.trees + self.bugs + self.drones

            # Bug simulation
            for bug in self.bugs:
                for drone in self.drones:
                    # if not any([check_vision(bug, drone) for drone in drones]):
                    #     bug.processVisual('none')
                    if bug.check_vision(drone):
                        bug.processVisual(drone)

                bug.advance(DT / 2)

                for tree in self.trees:
                    if check_collision(bug, tree):
                        bug.mode = 'tree'
                        bug.tree = tree
                    if bug.check_vision(tree):
                        bug.processVisual(tree)

                bug.advance(DT / 2)


            # Drone simulation
            for drone in self.drones:
                for entity in self.entities:
                    # Check collisions
                    if check_collision(drone, entity):
                        # print('Collision between ', drone.name, 'and', entity.name)
                        if entity in self.drones:
                            self.drones.remove(drone)
                            self.drones.remove(entity)
                            self.entities.remove(drone)
                            self.entities.remove(entity)
                        elif entity in self.bugs:
                            self.bugs.remove(entity)
                            self.entities.remove(entity)
                        elif entity in self.trees:
                            self.drones.remove(drone)
                            self.entities.remove(drone)

                    # Maintain list of visible entities
                    if check_drone_vision(drone, entity) and entity not in drone.visible_entities:
                        drone.visible_entities.append(entity)
                    if not check_drone_vision(drone, entity) and entity in drone.visible_entities:
                        drone.visible_entities.remove(entity)

                    for entity in drone.visible_entities:
                        if entity not in self.entities:
                            drone.visible_entities.remove(entity)


                drone.codrones = [otherdrone for otherdrone in self.drones if not otherdrone == drone]








                drone.advance()



            if self.visualise:
                self.visuals.update(self.trees, self.bugs, self.drones)

            self.t += DT

            #End conditions
            if len(self.drones) / N_DRONES < 0.2 or not self.bugs or self.t >= T_MAX:
                running = False
                self.score = self.evaluate()

        return self.score
