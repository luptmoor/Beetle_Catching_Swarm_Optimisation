# Environment   1 px = 2cm
WIDTH               = 1200        # px,  24 m
HEIGHT              =  700         # px,  14 m
LAUNCHPAD_FRAC      =    0.4

N_TREES             =   35
R_TREE              =   20          # px, 40 cm
TREE_MIN_DIST       =   50          # px, 1.00 m

# Bugs
N_BUGS              =   50
R_BUG               =    1           # px, 2 cm
R_VIS_BUG           =   60          # px, 1.60 m
BUG_RANDOMNESS      =  120 / 57.3  # rad / s,  maximum heading change per second
V_BUG               =   12          # px / s (0.24 m/s    0.864 km/h) look at paper
TREE_LAND_PROB      =    0.005
ESCAPE_PROB         =    0.90
TAKEOFF_PROB        =    0.05
REPRO_PROB          =    0.0002

# Static Drone Parameters
N_DRONES            =  10
R_DRONE             =   7          # px, 22 cm
DRONE_MIN_DIST      =  40         # px (80 cm),   minimum distance that drones can be placed at start of simulation
V_DRONE_MAX         =  50         # px / s (0.8m/s   2.88 km/h) check again
A_DRONE_MAX         =  80         # px / s^2 (1.6 m/s^2      0.16g)

ACTIVITY_DECAY      =   0.2        # points / s
ACTIVITY_AWARD      =  10         # points / bug
BATTERY_CAP         = 300        # s
CHARGE_RATE         = 100 / BATTERY_CAP          # % / s


# Simulation parameters

DT                  = 0.1        # s
T_MAX               = 5000       # s (1h 23min 20s)

# Colours for visualisation
GREEN               = (0, 130, 20)
BROWN               = (117, 60, 26)
GREY                = (128, 128, 128)
RED                 = (180, 0, 0)
YELLOW              = (255, 255, 0)
ORANGE              = (255, 134, 0)
PINK                = (255, 0, 255)
BLUE                = (0, 50, 255)
WHITE               = (255, 255, 255)

BUG_COLOURS = {'idle': RED, 'land': ORANGE, 'tree': YELLOW, 'escape': PINK}


# CMA-ES parameter settings
MIN_R_VIS_BUG           =  50
MAX_R_VIS_BUG           = 200
MU_R_VIS_BUG            = (MAX_R_VIS_BUG + MIN_R_VIS_BUG) / 2
RANGE_R_VIS_BUG         = MAX_R_VIS_BUG - MIN_R_VIS_BUG

MIN_R_VIS_DRONE         =  20
MAX_R_VIS_DRONE         = 150
MU_R_VIS_DRONE          = (MAX_R_VIS_DRONE + MIN_R_VIS_DRONE) / 2
RANGE_R_VIS_DRONE       = MAX_R_VIS_DRONE - MIN_R_VIS_DRONE

MIN_R_VIS_TREE          =  20
MAX_R_VIS_TREE          = 100
MU_R_VIS_TREE           = (MAX_R_VIS_TREE + MIN_R_VIS_TREE) / 2
RANGE_R_VIS_TREE        = MAX_R_VIS_TREE - MIN_R_VIS_TREE

MIN_K_TREE              =   0
MAX_K_TREE              = 100
MU_K_TREE               = (MAX_K_TREE + MIN_K_TREE) / 2
RANGE_K_TREE            = MAX_K_TREE - MIN_K_TREE

MIN_K_NEARDRONE         =   0
MAX_K_NEARDRONE         = 100
MU_K_NEARDRONE          = (MAX_K_NEARDRONE + MIN_K_NEARDRONE) / 2
RANGE_K_NEARDRONE       = MAX_K_NEARDRONE - MIN_K_NEARDRONE

MIN_K_BUG               =   -5
MAX_K_BUG               =    0
MU_K_BUG                = (MAX_K_BUG + MIN_K_BUG) / 2
RANGE_K_BUG             = MAX_K_BUG - MIN_K_BUG

MIN_K_FARDRONE          =  -20e-4
MAX_K_FARDRONE          =   20e-4
MU_K_FARDRONE           = (MAX_K_FARDRONE + MIN_K_FARDRONE) / 2
RANGE_K_FARDRONE        = MAX_K_FARDRONE - MIN_K_FARDRONE

MIN_K_ACTIVITY          =  -20e-4
MAX_K_ACTIVITY          =   20e-4
MU_K_ACTIVITY           = (MAX_K_ACTIVITY + MIN_K_ACTIVITY) / 2
RANGE_K_ACTIVITY        = MAX_K_ACTIVITY - MIN_K_ACTIVITY

MIN_V_MIN               =    0
MAX_V_MIN               =   15
MU_V_MIN                = (MAX_V_MIN + MIN_V_MIN) / 2
RANGE_V_MIN             = MAX_V_MIN - MIN_V_MIN

MIN_TEMP_COHESION       =    0
MAX_TEMP_COHESION       =  100
MU_TEMP_COHESION        = (MAX_TEMP_COHESION + MIN_TEMP_COHESION) / 2
RANGE_TEMP_COHESION     = MAX_TEMP_COHESION - MIN_TEMP_COHESION

RUNS_PER_SOLUTION       =   3