# Environment   scale: 1 px = 2cm
WIDTH                = 1400                                        # px,  28 m
HEIGHT               =  750                                        # px,  15 m
AREA                 = WIDTH * 0.02 * HEIGHT * 0.02                # m^2
LAUNCHPAD_FRAC       =    0.3                                      # -, used to determine drones' launchpad size

# Trees
TREE_DENSITY         =    0.08                                     # trees / m^2
N_TREES              =   int(round(AREA * TREE_DENSITY, 0))        # -
R_TREE_MIN           =    4                                        # px,  8 cm
R_TREE_MAX           =   40                                        # px, 80 cm
R_TREE_AVG           =   (R_TREE_MAX + R_TREE_MIN) / 2             # px, mean for normal distribution
R_TREE_STD           =   (R_TREE_MAX - R_TREE_MIN) / 6             # px, standard deviation for normal distribution
TREE_MIN_DIST        =   R_TREE_MAX                                # px, 1.00 m, minimum spacing

# Bugs
N_BUGS               =   int(round(1.4 * AREA * TREE_DENSITY, 0))  # -, number of bugs
R_BUG                =    1                                        # px, 2 cm, radius of bug
R_VIS_BUG            =  100                                       # px, 1 m, vision radius of bug
BUG_RANDOMNESS       =  120 / 57.3                                 # rad / s, bugs' maximum heading change per second
V_BUG                =   62                                        # px / s (1.24 m/s) bug velocity
TREE_LAND_PROB       =    0.005                                    # 1 / s
ESCAPE_PROB          =    0.20                                     # 1 / s
TAKEOFF_PROB         =    0.001                                    # 1 / s

# Static Drone Parameters
BUGS_PER_DRONE       =    3                                        # -
N_DRONES             =  int(round(N_BUGS / BUGS_PER_DRONE, 0))     # -, number of drones
R_DRONE              =    7                                        # px, 14 cm, drone radius
DRONE_MIN_DIST       =   40                                        # px, 80 cm, minimum initial drone spacing
V_DRONE_MAX          =  250                                        # px / s,  5 m / s
A_DRONE_MAX          =  165                                        # px / s^2, 3.3 m / s^2

# Simulation parameters
DT                   =    0.1                                       # s, timestep per tick
T_MAX                =    8                                   # s, 10min, maximum simulation duration
VISUALISE            =  True                                        # Boolean deciding if simulation shall be visualised
REALTIME             =  False                                       # Boolean deciding if visuals shall be real-time
VIEW                 =    0                                         # Variable for different views in visualisation


# RGB colours for visualisation
GREEN                = (0, 130, 20)
BROWN                = (117, 60, 26)
GREY                 = (128, 128, 128)
RED                  = (180, 0, 0)
YELLOW               = (255, 255, 0)
ORANGE               = (255, 134, 0)
PINK                 = (255, 0, 255)
BLUE                 = (0, 50, 255)
WHITE                = (255, 255, 255)

BUG_COLOURS = {'idle': RED, 'land': ORANGE, 'tree': YELLOW, 'escape': PINK}
TYPE_COLOURS = {'drone': GREY, 'tree': BROWN, 'bug': RED}


# CMA-ES settings
RUNS_PER_SOLUTION     =    3                                        # -, for how many conditions each solution is tested
N_GENERATIONS         =  100                                        # -, number of generations in CMA-ES
N_POP                 =   16                                        # -, number of genotypes per generation

# Parameter 0
MIN_R_VIS_TREE        =   10
MAX_R_VIS_TREE        =  150
MU_R_VIS_TREE         = (MAX_R_VIS_TREE + MIN_R_VIS_TREE) / 2
RANGE_R_VIS_TREE      = MAX_R_VIS_TREE - MIN_R_VIS_TREE

# Parameter 1
MIN_K_TREE            =    0
MAX_K_TREE            =  150
MU_K_TREE             = (MAX_K_TREE + MIN_K_TREE) / 2
RANGE_K_TREE          = MAX_K_TREE - MIN_K_TREE

# Parameter 2
MIN_R_VIS_BUG         =   10
MAX_R_VIS_BUG         =  200
MU_R_VIS_BUG          = (MAX_R_VIS_BUG + MIN_R_VIS_BUG) / 2
RANGE_R_VIS_BUG       = MAX_R_VIS_BUG - MIN_R_VIS_BUG

# Parameter 3
MIN_K_BUG             =   -150
MAX_K_BUG             =    0
MU_K_BUG              = (MAX_K_BUG + MIN_K_BUG) / 2
RANGE_K_BUG           = MAX_K_BUG - MIN_K_BUG

# Parameter 4
MIN_R_VIS_NEARDRONE   =   10
MAX_R_VIS_NEARDRONE   =  150
MU_R_VIS_NEARDRONE    = (MAX_R_VIS_NEARDRONE + MIN_R_VIS_NEARDRONE) / 2
RANGE_R_VIS_NEARDRONE = MAX_R_VIS_NEARDRONE - MIN_R_VIS_NEARDRONE

# Parameter 5
MIN_K_NEARDRONE       =    0
MAX_K_NEARDRONE       =  150
MU_K_NEARDRONE        = (MAX_K_NEARDRONE + MIN_K_NEARDRONE) / 2
RANGE_K_NEARDRONE     = MAX_K_NEARDRONE - MIN_K_NEARDRONE

# Parameter 6
MIN_R_VIS_FARDRONE    =  MAX_K_NEARDRONE
MAX_R_VIS_FARDRONE    =  500
MU_R_VIS_FARDRONE     = (MAX_R_VIS_FARDRONE + MIN_R_VIS_FARDRONE) / 2
RANGE_R_VIS_FARDRONE  = MAX_R_VIS_FARDRONE - MIN_R_VIS_FARDRONE

# Parameter 7
MIN_K_FARDRONE        =   -0.5
MAX_K_FARDRONE        =    0.5
MU_K_FARDRONE         = (MAX_K_FARDRONE + MIN_K_FARDRONE) / 2
RANGE_K_FARDRONE      = MAX_K_FARDRONE - MIN_K_FARDRONE

# Parameter 8
MIN_R_ACTIVITY        =  MIN_R_VIS_FARDRONE
MAX_R_ACTIVITY        =  MAX_R_VIS_FARDRONE
MU_R_ACTIVITY         = (MAX_R_ACTIVITY + MIN_R_ACTIVITY) / 2
RANGE_R_ACTIVITY      = MAX_R_ACTIVITY - MIN_R_ACTIVITY

# Parameter 9
MIN_K_ACTIVITY        =   -0.5
MAX_K_ACTIVITY        =    0.5
MU_K_ACTIVITY         = (MAX_K_ACTIVITY + MIN_K_ACTIVITY) / 2
RANGE_K_ACTIVITY      = MAX_K_ACTIVITY - MIN_K_ACTIVITY

# Parameter 10
MIN_V_MIN             =    0
MAX_V_MIN             =   20
MU_V_MIN              = (MAX_V_MIN + MIN_V_MIN) / 2
RANGE_V_MIN           = MAX_V_MIN - MIN_V_MIN

# Parameter 11
MIN_V_MAX             =   MAX_V_MIN
MAX_V_MAX             =  V_DRONE_MAX
MU_V_MAX              = (MAX_V_MAX + MIN_V_MAX) / 2
RANGE_V_MAX           = MAX_V_MAX - MIN_V_MAX

# Parameter 12
MIN_C                 =   0
MAX_C                 =   1
MU_C                  = (MAX_C + MIN_C) / 2
RANGE_C               = MAX_C - MIN_C



