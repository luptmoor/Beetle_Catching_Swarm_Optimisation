import numpy as np
from PhysicalObject import PhysicalObject
from Bug import Bug
from Visuals import Visuals
from settings import *



# Lists
phobjects = []
trees = []
drones = []
bugs = []


def check_collision(obj1, obj2, margin=0):
    if obj1 is None or obj2 is None:
        return False

    if obj1.name == obj2.name:
        return False

    if np.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) <= obj1.r_col + obj2.r_col + margin:
        return True
    else:
        return False


def check_vision(active, passive, margin=0):
    if active is None or passive is None:
        return False

    if active.name == passive.name:
        return False

    if np.sqrt((active.x - passive.x) ** 2 + (active.y - passive.y) ** 2) <= active.r_vis + passive.r_col + margin:
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
                trees.append(newtree)
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

            newbug = Bug('Bug ' + str(j), x, y, r_bug)
            if not any([check_collision(newbug, phobject) for phobject in phobjects]):
                phobjects.append(newbug)
                bugs.append(newbug)
                print(newbug.name, 'placed!')
                placing = False
            else:
                pass

    # Place drones
    # for k in range(n_drones):
    #     placing = True
    #     while placing:
    #         x = (np.random.random() * width * launchpad_frac) // 1
    #         y = (np.random.random() * height * launchpad_frac) // 1
    #
    #         newdrone = PhysicalObject('Drone ' + str(k), x, y, r_drone)
    #         if not any([check_collision(newdrone, phobject) for phobject in phobjects]):
    #             phobjects.append(newdrone)
    #             drones.append(newdrone)
    #             print(newdrone.name, 'placed!')
    #             placing = False
    #         else:
    #             pass


# def collision_loop():
#     """
#     loops over drones and checks for collisions with other phobjects.
#     note: instances need to be the same in drones list and phobjects list!
#     :return: void
#     """
#

def evaluate(mode, t):
    if mode == 1:
        return t - 450
    if mode == 2:
        return 450 - t
    if mode == 3:
        return 300 * len(drones) / n_drones - 150


#if __name__ == 'main' and True:
if True:
    load_environment()
    visuals = Visuals(width, height, dt)

    for t in range(tmax+1):
        print('Time:', t, 's')

        # Guarantee this always holds (good candidate for removal if too slow)
        phobjects = trees + bugs + drones


        # Bug simulation
        for bug in bugs:
            for tree in trees:
                if check_collision(bug, tree):
                    bug.mode = 'tree'
                if check_vision(bug, tree):
                    bug.processVisual('tree', tree.x, tree.y)

            for drone in drones:
                if check_vision(bug, drone):
                    bug.processVisual('drone', drone.x, drone.y)

            bug.advance(dt)



        visuals.update(trees, bugs)
        # Drone simulation
        # for drone in drones:
        #     for phobject in phobjects:
        #         if check_collision(drone, phobject):
        #             print('Collision between ', drone.name, 'and', phobject.name)
        #             if phobject in drones:
        #                 drones.remove(drone)
        #                 drones.remove(phobject)
        #                 phobjects.remove(drone)
        #                 phobjects.remove(phobject)
        #             elif phobject in bugs:
        #                 bugs.remove(phobject)
        #                 phobjects.remove(phobject)
        #             else:
        #                 drones.remove(drone)
        #                 phobjects.remove(drone)

        # End conditions
        # if not bugs:
        #     score = evaluate(1, t)
        #     break
        # if not drones:
        #     score = evaluate(2, t)
        #     break
        if t >= tmax:
            score = evaluate(3, t)
            break



