# Global Parameters

# Environment
width = 1200  # px,  24 m
height = 800  # px,  16 m
launchpad_frac = 0.3

n_trees = 35
r_tree = 20  # px, 40 cm
tree_min_dist = 50  # px, 1 m

# Bugs
n_bugs = 40
r_bug = 3  # px, 2 cm
r_bug_vision = 80  # px, 1.60 m
dXmax_bug = 60 / 57.3  # rad / timestep
bug_speed = 10
tree_land_prob = 0.03
escape_prob = 0.80
lift_prob = 0.15

# Static Drone Parameters
n_drones = n_bugs // 3
r_drone = 13  # px, 26 cm
r_drone_vision = 200  # px, 4 m
dXmax_drone = 30 / 57.3  # rad / timestep


# Simulation parameters
tmax = 180  # s
dt = 0.5  # s


# Colours for visualisation
green = (0, 130, 20)
brown = (117, 60, 26)
grey = (128, 128, 128)
red = (180, 0, 0)
yellow = (255, 255, 0)
orange = (255, 134, 0)
pink = (255, 0, 255)

bug_colours = {'idle': red, 'land': orange, 'tree': yellow, 'escape': pink}



