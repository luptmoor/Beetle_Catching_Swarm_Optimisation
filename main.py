from Simulation import Simulation
import cma
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from settings import *


def fitness(params):
    scores = []
    for i in range(RUNS_PER_SOLUTION):
        sim = Simulation(params, seed=i, visualise=False)
        print('STARTING SIMULATION WITH SEED', i, 'AND PARAMETERS:')
        print('r_vis_bug:', params[0] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG)
        print('r_vis_drone:', params[1] * RANGE_R_VIS_DRONE / 2 + MU_R_VIS_DRONE)
        print('r_vis_tree:', params[2] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE)
        print('k_tree:', params[3] * RANGE_K_TREE / 2 + MU_K_TREE)
        print('k_neardrone:', params[4] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE)
        print('k_bug:', params[5] * RANGE_K_BUG / 2 + MU_K_BUG)
        print('k_fardrone:', params[6] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE)
        print('k_activity:', params[7] * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY)
        print('v_min:', params[8] * RANGE_V_MIN / 2 + MU_V_MIN)
        print('temp_cohesion:', params[9] * RANGE_TEMP_COHESION / 2 + MU_TEMP_COHESION)
        print()

        scores.append(sim.run())

    fitness_value = np.mean(scores)
    timestamp = datetime.now().strftime('%d_%m__%H_%M_%S')
    with open(str(fitness_value) + '_' + timestamp, 'w') as file:
        file.write('Simulation with parameters:\n')
        file.write('r_vis_bug: ' + str(params[0] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG) + '\n')
        file.write('r_vis_drone: ' + str(params[1] * RANGE_R_VIS_DRONE / 2 + MU_R_VIS_DRONE) + '\n')
        file.write('r_vis_tree: ' + str(params[2] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE) + '\n')
        file.write('k_tree: ' + str(params[3] * RANGE_K_TREE / 2 + MU_K_TREE) + '\n')
        file.write('k_neardrone: ' + str(params[4] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE) + '\n')
        file.write('k_bug: ' + str(params[5] * RANGE_K_BUG / 2 + MU_K_BUG) + '\n')
        file.write('k_fardrone: ' + str(params[6] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE) + '\n')
        file.write('k_activity: ' + str(params[7] * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY) + '\n')
        file.write('v_min: ' + str(params[8] * RANGE_V_MIN / 2 + MU_V_MIN) + '\n')
        file.write('temp_cohesion: ' + str(params[9] * RANGE_TEMP_COHESION / 2 + MU_TEMP_COHESION) + '\n')
        file.write('\n')
        file.write('attained fitness values of ' + str(scores) + ' (avg. ' + str(fitness_value) + ')')

    return fitness_value


# Set up of the CMA-ES hyperparameters
population_size = 10
max_iterations = 10

options = {
    'maxiter': max_iterations,
    'tolfun': 0,
}

# Run the CMA-ES optimization
es = cma.CMAEvolutionStrategy(10 * [0], 0.35, options)
best_solution = None

fitnesses = []
g = 1
while not es.stop():
    print('GENERATION:', g)
    solutions = es.ask()    # list of lists with parameters (n_pop x n_param)
    fitness_values = [fitness(x) for x in solutions]  # list of fitnesses (n_pop x 1)
    es.tell(solutions, fitness_values)
    best_solution = es.best.get()[0]  # list of params of best solution (1 x n_param)
    fitnesses.append(fitness(best_solution))
    es.disp()
    g += 1

# Retrieve the best solution and its fitness value
print("Best solution:", best_solution)

plt.plot(range(1, len(fitnesses) + 1), fitnesses)
plt.xlabel("Generation")
plt.ylabel("Best Fitness Value")
plt.title("Convergence Plot")
plt.grid(True)
plt.show()

# parameters = [50,  # 'r_vis_bug'
#                 15,  # 'r_vis_drone'
#           40,  # 'r_vis_tree'
#           50,  # 'k_tree'
#           100,  # 'k_neardrone'
#           -5,  # 'k_bug'
#           - 10e-4,  # 'k_fardrone'
#           - 1e-4,  # 'k_activity'
#           5,  # 'v_min'
#           100  # 'temp_cohesion'
#           ]
