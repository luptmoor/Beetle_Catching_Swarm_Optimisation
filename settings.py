# Global Parameters

# Environment
width = 700  # px,  24 m 1200
height = 700  # px,  16 m 700
launchpad_frac = 1

n_trees = 17
r_tree = 20  # px, 40 cm
tree_min_dist = 70  # px, 1.20 m

# Bugs
n_bugs = 30
r_bug = 3  # px, 6 cm
r_bug_vision = 60  # px, 1.60 m
dXmax_bug = 60 / 57.3  # rad / timestep
v_bug = 12
tree_land_prob = 0.005
escape_prob = 0.90
lift_prob = 0.05

# Static Drone Parameters
n_drones = 8
r_drone = 11  # px, 22 cm
drone_min_dist = 40
r_drone_vision = 80  # px, 4 m
dXmax_drone = 30 / 57.3  # rad / timestep
v_max = 60
v_min = 5
a_max = 1000 # ?


# Simulation parameters

dt = 0.1 # s
tmax = 180  # s

# Colours for visualisation
green = (0, 130, 20)
brown = (117, 60, 26)
grey = (128, 128, 128)
red = (180, 0, 0)
yellow = (255, 255, 0)
orange = (255, 134, 0)
pink = (255, 0, 255)
blue = (0, 50, 255)
white = (255, 255, 255)

bug_colours = {'idle': red, 'land': orange, 'tree': yellow, 'escape': pink}

view = 0
