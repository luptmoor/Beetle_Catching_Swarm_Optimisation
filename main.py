from Simulation import Simulation
import cma
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from settings import *
import os
import pandas as pd


def log(g, mean, sigma, solutions, fitness_values):
    """
    exports evolution results per generation to CSV file using pandas.
    :param g: (int) Generation number, used for file name.
    :param mean: (float) Means used to create solutions.
    :param sigma: (float) Standard deviations used to create solutions.
    :param solutions: (list) List of evolved parameters (N_pop x N_parameters)
    :param fitness_values: (list) List of fitness values for each solution (N_pop x RUNS_PER_SOLUTION)
    :return: None.
    """
    solutions.append(mean)

    df = pd.DataFrame(solutions, index=[i for i in range(len(solutions)-1)] + ['Underlying Mean'],
                      columns=['r_vis_tree',
                               'k_tree',
                               'r_vis_bug',
                               'k_bug',
                               'r_vis_neardrone',
                               'k_neardrone',
                               'r_vis_fardrone',
                               'k_fardrone',
                               'r_activity',
                               'k_activity',
                               'v_min',
                               'v_max',
                               'c'])

    df['Fitness 1'] = pd.Series([value[0] for value in fitness_values])
    df['Fitness 2'] = pd.Series([value[1] for value in fitness_values])
    df['Fitness 3'] = pd.Series([value[2] for value in fitness_values])
    df['Average Fitness'] = pd.Series([np.mean(value) for value in fitness_values])
    df['Sigma'] = pd.Series(13 * [sigma])

    # Coordinate shift
    df['r_vis_tree'] = round(df['r_vis_tree'] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE)
    df['k_tree'] = df['k_tree'] * RANGE_K_TREE / 2 + MU_K_TREE

    df['k_bug'] = df['k_bug'] * RANGE_K_BUG / 2 + MU_K_BUG
    df['r_vis_bug'] = round(df['r_vis_bug'] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG, 0)

    df['r_vis_neardrone'] = df['r_vis_neardrone'] * RANGE_R_VIS_NEARDRONE / 2 + MU_R_VIS_NEARDRONE
    df['k_neardrone'] = df['k_neardrone'] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE

    df['r_vis_fardrone'] = round(df['r_vis_fardrone'] * RANGE_R_VIS_FARDRONE / 2 + MU_R_VIS_FARDRONE)
    df['k_fardrone'] = df['k_fardrone'] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE

    df['r_activity'] = df['r_activity'] * RANGE_R_ACTIVITY / 2 + MU_R_ACTIVITY
    df['k_activity'] = df['k_activity'] * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY

    df['v_min'] = df['v_min'] * RANGE_V_MIN / 2 + MU_V_MIN
    df['v_max'] = df['v_max'] * RANGE_V_MAX / 2 + MU_V_MAX
    df['c'] = df['c'] * RANGE_C / 2 + MU_C

    df = df.sort_values(by='Average Fitness', ascending=False)
    df.index = [i for i in range(len(solutions)-1)] + ['Underlying Mean']
    df.to_csv('logs/Gen' + str(g) + '.csv')


def fitness(params):
    """
    determines fitness values for a solution using the simulation.
    :param params: (list) List of parameters, a.k.a. solution (N_pop x 1).
    :return: scores: (List) List of fitness values (RUNS_PER_SOLUTION x 1).
    """
    scores = []
    for i in range(RUNS_PER_SOLUTION):
        sim = Simulation(params, seed=i)
        # print('STARTING SIMULATION WITH SEED', i, 'AND PARAMETERS:')
        # print('r_vis_bug:', int(round(params[0] * RANGE_R_VIS_BUG / 2 + MU_R_VIS_BUG, 0)))
        # print('r_vis_neardrone:', int(round(params[1] * RANGE_r_vis_neardrone / 2 + MU_r_vis_neardrone)))
        # print('r_vis_tree:', int(round(params[2] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE)))
        # print('k_tree:', params[3] * RANGE_K_TREE / 2 + MU_K_TREE)
        # print('k_neardrone:', params[4] * RANGE_K_NEARDRONE / 2 + MU_K_NEARDRONE)
        # print('k_bug:', params[5] * RANGE_K_BUG / 2 + MU_K_BUG)
        # print('k_fardrone:', params[6] * RANGE_K_FARDRONE / 2 + MU_K_FARDRONE)
        # print('k_activity:', params[7] * RANGE_K_ACTIVITY / 2 + MU_K_ACTIVITY)
        # print('v_min:', min(V_DRONE_MAX, max(0, params[8] * RANGE_V_MIN / 2 + MU_V_MIN)))
        # print('temp_cohesion:', min(100, max(0, params[9] * RANGE_TEMP_COHESION / 2 + MU_TEMP_COHESION)))
        # print()

        scores.append(sim.run())
    return scores


options = {
    'maxiter': N_GENERATIONS,  # sets maximum number of generations
}

# Run the CMA-ES optimization
es = cma.CMAEvolutionStrategy(13 * [0], 0.35, options)
fitnesses = []
g = 1

while not es.stop():
    print('GENERATION:', g)
    solutions = es.ask()  # list of lists with parameters (n_pop x n_param)
    fitness_values = [fitness(x) for x in solutions]  # list of fitnesses (n_pop x RUNS_PER_SOLUTION)
    log(g, es.mean, es.sigma, solutions.copy(), fitness_values)
    average_fitnesses = [np.mean(fitness_value) for fitness_value in fitness_values]  # list of avg fitnesses (n_pop x 1)

    cost = [-x for x in average_fitnesses]  # es object minimises function, so negative fitness is defined as cost
    es.tell(solutions, cost)
    best_solution = es.best.get()[0]  # list of params of best solution (1 x n_param)
    fitnesses.append(fitness(best_solution))
    es.disp()

    g += 1

# Retrieve the best solution and its fitness value
# print("Best solution:", best_solution)
#
# plt.plot(range(1, len(fitnesses) + 1), fitnesses)
# plt.xlabel("Generation")
# plt.ylabel("Best Fitness Value")
# plt.title("Convergence Plot")
# plt.grid(True)
# plt.show()

# parameters = [(180 - MU_R_VIS_BUG) * 2 / RANGE_R_VIS_BUG,  # 'r_vis_bug'
#               (180 - MU_r_vis_neardrone) * 2 / RANGE_r_vis_neardrone,  # 'r_vis_neardrone'
#               (50 - MU_R_VIS_TREE) * 2 / RANGE_R_VIS_TREE,  # 'r_vis_tree'
#           300,  # 'k_tree'
#           60,  # 'k_neardrone'
#           -4,  # 'k_bug'
#           - 50e-4,  # 'k_fardrone'
#           - 1e-4,  # 'k_activity'
#           3,  # 'v_min'
#           100  # 'temp_cohesion'
#           ]
#
# sim = Simulation(parameters, seed=355, visualise=True)
# sim.run()
