import numpy as np

# Global Parameters

width = 1200  # px
height = 800  # px

r_tree = 30
r_drone = 0
r_drone_vision = 0
r_bug = 0
r_bug_vision = 0

tree_min_dist = 50

n_trees = 10
n_drones = 0
n_bugs = 25

# Lists
phobjects = []



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
            x = np.random.random() * (width - 2*(r_tree + tree_min_dist)) + (r_tree + tree_min_dist) //1
            y = np.random.random() * (height - 2*(r_tree + tree_min_dist)) + (r_tree + tree_min_dist) //1

            newtree = PhysicalObject('Tree ' + str(i), x, y, r_tree)
            if not any([check_collision(newtree, phobject, tree_min_dist) for phobject in phobjects]):
                phobjects.append(newtree)
                print(newtree.name, 'placed!')
                placing = False
            else:
                pass

    # Place bugs
    for i in range(n_bugs):
        placing = True
        while placing:
            x = (np.random.random() * width) // 1
            y = (np.random.random() * height) // 1

            newbug = PhysicalObject('Bug ' + str(i), x, y, r_bug)
            if not any([check_collision(newbug, phobject) for phobject in phobjects]):
                phobjects.append(newbug)
                print(newbug.name, 'placed!')
                placing = False
            else:
                pass


load_environment()
