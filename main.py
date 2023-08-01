import numpy as np
from PhysicalObject import PhysicalObject
from Bug import Bug
from Drone import Drone
from Visuals import Visuals
from settings import *

score = 0

# Lists
phobjects = []
trees = []
drones = []
charging = []
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


def check_bug_vision(active, passive):
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
def check_drone_vision(active, passive):
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

def place_drones(n):
    for k in range(n):
        placing = True
        while placing:
            x = (np.random.random() * WIDTH * LAUNCHPAD_FRAC) // 1
            y = (np.random.random() * HEIGHT * LAUNCHPAD_FRAC) // 1

            newdrone = Drone('Drone ' + str(k), 'drone', x, y, R_DRONE)
            if not any([check_collision(newdrone, phobject, DRONE_MIN_DIST) for phobject in phobjects]):
                phobjects.append(newdrone)
                drones.append(newdrone)
                print(newdrone.name, 'placed!')
                placing = False
            else:
                pass

def load_environment():
    global phobjects

    # Place trees
    for i in range(N_TREES):
        placing = True
        while placing:
            x = np.random.random() * (WIDTH - 2 * (R_TREE + TREE_MIN_DIST)) + (R_TREE + TREE_MIN_DIST) // 1
            y = np.random.random() * (HEIGHT - 2 * (R_TREE + TREE_MIN_DIST)) + (R_TREE + TREE_MIN_DIST) // 1

            newtree = PhysicalObject('Tree ' + str(i), 'tree', x, y, R_TREE)
            if not any([check_collision(newtree, phobject, TREE_MIN_DIST) for phobject in phobjects]):
                phobjects.append(newtree)
                trees.append(newtree)
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
            if not any([check_collision(newbug, phobject) for phobject in phobjects]):
                phobjects.append(newbug)
                bugs.append(newbug)
                print(newbug.name, 'placed!')
                placing = False
            else:
                pass

    # Place drones
    place_drones(N_DRONES)


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
        return 300 * len(drones) / N_DRONES - 150


#if __name__ == 'main' and True:
if True:
    load_environment()
    visuals = Visuals(WIDTH, HEIGHT, DT)
    running = True
    t = 0

    while running:
        if t//1 % 5 == 0:
            print()
            print('Time:', round(t, 2), 's')

        # Guarantee this always holds (good candidate for removal if too slow)
        phobjects = trees + bugs + drones


        # Bug simulation
        for bug in bugs:
            for tree in trees:
                if check_collision(bug, tree):
                    bug.mode = 'tree'
                if check_bug_vision(bug, tree):
                    bug.processVisual('tree', tree.x, tree.y)

            for drone in drones:
                # if not any([check_vision(bug, drone) for drone in drones]):
                #     bug.processVisual('none')
                if check_bug_vision(bug, drone):
                    bug.processVisual('drone', drone.x, drone.y)


            repro = bug.advance(DT)
            if repro:
                newbug = Bug(bug.name + ' (' + str(t) + 's)', bug.x, bug.y)
                bugs.append(newbug)
                phobjects.append(newbug)

        # Drone simulation
        for drone in drones:
            drone.codrones = [otherdrone for otherdrone in drones if not otherdrone == drone]

            for phobject in phobjects:
                # Maintain list of visible phobjects
                if check_drone_vision(drone, phobject) and phobject not in drone.visible_phobjects:
                    drone.visible_phobjects.append(phobject)
                if not check_drone_vision(drone, phobject) and phobject in drone.visible_phobjects:
                    drone.visible_phobjects.remove(phobject)

            for phobject in drone.visible_phobjects:
                if phobject not in phobjects:
                    drone.visible_phobjects.remove(phobject)

                # Check collisions
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
                        drone.activity += ACTIVITY_AWARD
                    elif phobject in trees:
                        drones.remove(drone)
                        phobjects.remove(drone)

            recharge = drone.advance(DT)
            if recharge:
                drones.remove(drone)
                charging.append(drone)


        for drone in charging:
            drone.charge = min(drone.charge + CHARGE_RATE * DT, 100)
            if drone.charge >= 100:
                drone.x = 0
                drone.y = 0
                drones.append(drone)
                charging.remove(drone)






        visuals.update(trees, bugs, drones, charging)

        t += DT

        # End conditions
        # if not bugs:
        #     score = evaluate(1, t)
        #     break
        # if not drones:
        #     score = evaluate(2, t)
        #     break
        if t >= T_MAX:
            score = evaluate(3, t)
            break

print(score)


