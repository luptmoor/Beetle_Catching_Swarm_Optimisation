# Environment   1 px = 2cm
WIDTH           = 1200        # px,  24 m
HEIGHT          =  700         # px,  14 m
LAUNCHPAD_FRAC  =    0.4

N_TREES         =   35
R_TREE          =   20          # px, 40 cm
TREE_MIN_DIST   =   50          # px, 1.00 m

# Bugs
N_BUGS          =   50
R_BUG           =    1           # px, 2 cm
R_VIS_BUG       =   60          # px, 1.60 m
BUG_RANDOMNESS  =  120 / 57.3  # rad / s,  maximum heading change per second
V_BUG           =   12          # px / s (0.24 m/s    0.864 km/h) look at paper
TREE_LAND_PROB  =    0.005
ESCAPE_PROB     =    0.90
TAKEOFF_PROB    =    0.05
REPRO_PROB      =    0.0002

# Static Drone Parameters
N_DRONES        =  10
R_DRONE         =   7          # px, 22 cm
DRONE_MIN_DIST  =  40         # px (80 cm),   minimum distance that drones can be placed at start of simulation
V_DRONE_MAX     =  50         # px / s (0.8m/s   2.88 km/h) check again
A_DRONE_MAX     =  80         # px / s^2 (1.6 m/s^2      0.16g)

ACTIVITY_DECAY  =   0.2        # points / s
ACTIVITY_AWARD  =  10         # points / bug
BATTERY_CAP     = 300        # s
CHARGE_RATE     = 100 / BATTERY_CAP          # % / s


# Simulation parameters

DT              = 0.1        # s
T_MAX            = 5000       # s (1h 23min 20s)

# Colours for visualisation
GREEN           = (0, 130, 20)
BROWN           = (117, 60, 26)
GREY            = (128, 128, 128)
RED             = (180, 0, 0)
YELLOW          = (255, 255, 0)
ORANGE          = (255, 134, 0)
PINK            = (255, 0, 255)
BLUE            = (0, 50, 255)
WHITE           = (255, 255, 255)

BUG_COLOURS = {'idle': RED, 'land': ORANGE, 'tree': YELLOW, 'escape': PINK}

