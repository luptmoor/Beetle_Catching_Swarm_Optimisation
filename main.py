import numpy as np

# Global Parameters
width = 1200  # px,  24 m
height = 800  # px,  16 m
launchpad_frac = 0.3

n_trees = 25
r_tree = 20  # px, 40 cm
tree_min_dist = 50  # px, 1 m

n_drones = 10
r_drone = 13  # px, 26 cm
r_drone_vision = 200  # px, 4 m

n_bugs = 20
r_bug = 1  # px, 2 cm
r_bug_vision = 80  # px, 1.60 m

tmax = 180

# Lists
phobjects = []
drones = []
bugs = []


# Physical Object Class
class PhysicalObject:
    def __init__(self, name, x, y, r_col):
        self.name = name
        self.x = x
        self.y = y
        self.r_col = r_col


def check_collision(obj1, obj2, margin=0):
    if obj1 is None or obj2 is None:
        return False

    if np.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) <= obj1.r_col + obj2.r_col + margin:
        return True
    else:
        return False


def load_environment():
    global phobjects

    # Place trees
    for i in range(n_trees):
        placing = True
        while placing:
            x = np.random.random() * (width - 2 * (r_tree + tree_min_dist)) + (r_tree + tree_min_dist) // 1
            y = np.random.random() * (height - 2 * (r_tree + tree_min_dist)) + (r_tree + tree_min_dist) // 1

            newtree = PhysicalObject('Tree ' + str(i), x, y, r_tree)
            if not any([check_collision(newtree, phobject, tree_min_dist) for phobject in phobjects]):
                phobjects.append(newtree)
                print(newtree.name, 'placed!')
                placing = False
            else:
                pass

    # Place bugs
    for j in range(n_bugs):
        placing = True
        while placing:
            x = (np.random.random() * width) // 1
            y = (np.random.random() * height) // 1

            newbug = PhysicalObject('Bug ' + str(j), x, y, r_bug)
            if not any([check_collision(newbug, phobject) for phobject in phobjects]):
                phobjects.append(newbug)
                bugs.append(newbug)
                print(newbug.name, 'placed!')
                placing = False
            else:
                pass

    # Place drones
    for k in range(n_drones):
        placing = True
        while placing:
            x = (np.random.random() * width * launchpad_frac) // 1
            y = (np.random.random() * height * launchpad_frac) // 1

            newdrone = PhysicalObject('Drone ' + str(k), x, y, r_drone)
            if not any([check_collision(newdrone, phobject) for phobject in phobjects]):
                phobjects.append(newdrone)
                drones.append(newdrone)
                print(newdrone.name, 'placed!')
                placing = False
            else:
                pass


def collision_loop():
    """
    loops over drones and checks for collisions with other phobjects.
    note: instances need to be the same in drones list and phobjects list!
    :return: void
    """
    for drone in drones:
        for phobject in phobjects:
            if check_collision(drone, phobject):
                print('Collision between ', drone.name, 'and', phobject.name)
                if phobject in drones:
                    drones.remove(drone)
                    drones.remove(phobject)
                    phobjects.remove(drone)
                    phobjects.remove(phobject)
                elif phobject in bugs:
                    bugs.remove(phobject)
                    phobjects.remove(phobject)
                else:
                    drones.remove(drone)
                    phobjects.remove(drone)

def evaluate(mode, t):
    if mode == 1:
        return t - 450
    if mode == 2:
        return 450 - t
    if mode == 3:
        return 300 * len(drones) / n_drones - 150

load_environment()

for t in range(tmax+1):
    print(t)

    collision_loop()

    if not bugs:
        evaluate(1, t)
        break
    if not drones:
        evaluate(2, t)
        break
    if t >= tmax:
        evaluate(3, t)
        break



