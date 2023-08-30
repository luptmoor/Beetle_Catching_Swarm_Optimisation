import concurrent.futures

from Simulation import Simulation
import cma
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from settings import *
import os
import pandas as pd
n = 1


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

    df = pd.DataFrame(solutions, index=[i for i in range(len(solutions) - 1)] + ['Underlying Mean'],
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

    df['Sigma'] = pd.Series(N_POP * [sigma])

    #  fitness_values: (n_pop x RUNS_PER_SOLUTION x 4)
    df['Fitness 1'] = pd.Series([value[0][0] for value in fitness_values])
    df['Crashed Drones 1'] = pd.Series([value[0][1] for value in fitness_values])
    df['Killed Bugs 1'] = pd.Series([value[0][2] for value in fitness_values])
    df['Passed Time 1'] = pd.Series([value[0][3] for value in fitness_values])

    df['Fitness 2'] = pd.Series([value[1][0] for value in fitness_values])
    df['Crashed Drones 2'] = pd.Series([value[1][1] for value in fitness_values])
    df['Killed Bugs 2'] = pd.Series([value[1][2] for value in fitness_values])
    df['Passed Time 2'] = pd.Series([value[1][3] for value in fitness_values])

    df['Fitness 3'] = pd.Series([value[2][0] for value in fitness_values])
    df['Crashed Drones 3'] = pd.Series([value[2][1] for value in fitness_values])
    df['Killed Bugs 3'] = pd.Series([value[2][2] for value in fitness_values])
    df['Passed Time 3'] = pd.Series([value[2][3] for value in fitness_values])

    df['Average Fitness'] = df[['Fitness 1', 'Fitness 2', 'Fitness 3']].mean(axis=1)
    df['Average Crashed Drones'] = df[['Crashed Drones 1', 'Crashed Drones 2', 'Crashed Drones 3']].mean(axis=1)
    df['Average Killed Bugs'] = df[['Killed Bugs 1', 'Killed Bugs 2', 'Killed Bugs 3']].mean(axis=1)
    df['Average Passed Time'] = df[['Passed Time 1', 'Passed Time 2', 'Passed Time 3']].mean(axis=1)

    # Coordinate shift
    df['r_vis_tree'] = round(df['r_vis_tree'] * RANGE_R_VIS_TREE / 2 + MU_R_VIS_TREE)
    df['k_tree'] = df['k_tree'] * RANGE_K_TREE / 2 + MU_K_TREE

    df['k_bug'] = df['k_bug'] * RANGE_K_BEETLE / 2 + MU_K_BEETLE
    df['r_vis_bug'] = round(df['r_vis_bug'] * RANGE_R_VIS_BEETLE / 2 + MU_R_VIS_BEETLE, 0)

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
    df.index = [i for i in range(len(solutions) - 1)] + ['Underlying Mean']

    if not os.path.exists('logs'):
        os.mkdir('logs')
    df.to_csv('logs/Gen' + str(g) + '_' + str(np.round(np.mean(df['Average Fitness']), 5)) + '.csv')


def sim(params, seed):
    simulation = Simulation(params, seed=seed)
    return simulation.run()


def resume_evolution(filename, g):
    """
    restarts CMA-ES by taking means and standard deviation from last reported generation
    :param filename: (String) filename of CSV file that contains report about last generation.
    :param g: (int) number of last reported generation, could also be extracted from filename.
    :return: None
    """
    options = {
        'maxiter': N_GENERATIONS - g,  # sets maximum number of generations
        'popsize': N_POP,
    }
    global n

    df = pd.read_csv(filename)
    sigma = df['Sigma'][0]
    means = pd.Series(df.iloc[20][1:14])

    # Transform parameters back to space that is used by cma library
    offsets = np.array([MU_R_VIS_TREE, MU_K_TREE, MU_R_VIS_BEETLE, MU_K_BEETLE, MU_R_VIS_NEARDRONE, MU_K_NEARDRONE, MU_R_VIS_FARDRONE, MU_K_FARDRONE, MU_R_ACTIVITY, MU_K_ACTIVITY, MU_V_MIN, MU_V_MAX, MU_C])
    scales = np.array([RANGE_R_VIS_TREE, RANGE_K_TREE, RANGE_R_VIS_BEETLE, RANGE_K_BEETLE, RANGE_R_VIS_NEARDRONE, RANGE_K_NEARDRONE, RANGE_R_VIS_FARDRONE, RANGE_K_FARDRONE, RANGE_R_ACTIVITY, RANGE_K_ACTIVITY, RANGE_V_MIN, RANGE_V_MAX, RANGE_C])
    means = means - offsets
    means = 2 * means / scales
    means = list(means)
    print(means)
    print(sigma)

    es = cma.CMAEvolutionStrategy(means, sigma, options)

    while not es.stop():
        g += 1
        n = 1

        print('GENERATION:', g)
        solutions = es.ask()  # list of lists with parameters (n_pop x n_param)
        fitness_metrics = np.array(
            [fitness(x) for x in solutions])  # array of fitnesses (n_pop x RUNS_PER_SOLUTION x 4)
        log(g, es.mean, es.sigma, solutions.copy(), fitness_metrics)

        # Take fitness of each run
        fitness_values = fitness_metrics[:, :, 0]
        average_fitnesses = np.mean(fitness_values, axis=1)

        cost = [-x for x in average_fitnesses]  # es object minimises function, so negative fitness is defined as cost
        es.tell(solutions, cost)
        es.disp()




def fitness_multi(params):
    """
    determines fitness values for a solution using the simulation.
    :param params: (list) List of parameters, a.k.a. solution (N_pop x 1).
    :return: scores: (List) List of fitness values and metrics for each run (RUNS_PER_SOLUTION x 4).
    """
    scores = []
    seeds = [seed for seed in range(RUNS_PER_SOLUTION)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(sim, params, seed) for seed in seeds]
        print('All threads started')

    for future in concurrent.futures.as_completed(futures):
        scores.append(future.result())  # elements are list 1 x 4 (score + 3 criteria)

    return scores  # list RUNS_PER_SOLUTION x 4


def fitness(params):
    """
    determines fitness values for a solution using the simulation.
    :param params: (list) List of parameters, a.k.a. solution (N_pop x 1).
    :return: scores: (List) List of fitness values and metrics for each run (RUNS_PER_SOLUTION x 4).
    """
    global n
    print('Genotype: ', n)
    scores = []
    for i in range(RUNS_PER_SOLUTION):
        sim = Simulation(params, seed=i)
        scores.append(sim.run())  # list 1 x 4 (score + 3 criteria)
    n += 1

    return scores  # list RUNS_PER_SOLUTION x 4


def analyse_sensitivity(filename):
    """
    analyses sensitivity of list of solutions to environmental parameters.
    :param filename: filename of CSV containing solutions.
    :return: None, exports results to other Sensitivity_Analysis.csv
    """

    df = pd.read_csv(filename)
    candidates = df.loc[5:7, 'r_vis_tree':'c']
    print(candidates)
    df_sa = pd.DataFrame()
    i = 1
    for index, params in candidates.iterrows():
        print('Evaluating candidate', i)
        print(params)

        # Coordinate shift to normalised domain
        offsets = np.array(
            [MU_R_VIS_TREE, MU_K_TREE, MU_R_VIS_BEETLE, MU_K_BEETLE, MU_R_VIS_NEARDRONE, MU_K_NEARDRONE, MU_R_VIS_FARDRONE,
             MU_K_FARDRONE, MU_R_ACTIVITY, MU_K_ACTIVITY, MU_V_MIN, MU_V_MAX, MU_C])
        scales = np.array(
            [RANGE_R_VIS_TREE, RANGE_K_TREE, RANGE_R_VIS_BEETLE, RANGE_K_BEETLE, RANGE_R_VIS_NEARDRONE, RANGE_K_NEARDRONE,
             RANGE_R_VIS_FARDRONE, RANGE_K_FARDRONE, RANGE_R_ACTIVITY, RANGE_K_ACTIVITY, RANGE_V_MIN, RANGE_V_MAX,
             RANGE_C])
        params = params - offsets
        params = 2 * params / scales
        params = list(params)

        scores = []
        killed_bugs = []
        passed_time = []
        dead_drones = []
        for seed in range(101, 151):
            sim = Simulation(params, seed=seed)
            score = sim.run()
            scores.append(score[0])
            killed_bugs.append(score[1])
            passed_time.append(score[2])
            dead_drones.append(score[3])

        df_sa['Fitness ' + str(i)] = pd.Series(scores)
        df_sa['Kiled Bugs ' + str(i)] = pd.Series(killed_bugs)
        df_sa['Passed Time ' + str(i)] = pd.Series(passed_time)
        df_sa['Crashed Drones ' + str(i)] = pd.Series(dead_drones)
        i += 1

    df_sa.to_csv('Sensitivity_Analysis_extra.csv')



#
analyse_sensitivity('toplist.csv')





# resume_evolution('logs/Gen90_0.72006.csv', 90)




# options = {
#     'maxiter': N_GENERATIONS,  # sets maximum number of generations
#     'popsize': N_POP,
# }
#
# # Run the CMA-ES optimization
# es = cma.CMAEvolutionStrategy(N_POP * [0], 0.35, options)
# fitnesses = []
# g = 1
#
# while not es.stop():
#     print('GENERATION:', g)
#     solutions = es.ask()  # list of lists with parameters (n_pop x n_param)
#     fitness_metrics = np.array([fitness(x) for x in solutions])  # array of fitnesses (n_pop x RUNS_PER_SOLUTION x 4)
#     log(g, es.mean, es.sigma, solutions.copy(), fitness_metrics)
#
#     # Take fitness of each run
#     fitness_values = fitness_metrics[:, :, 0]
#     average_fitnesses = np.mean(fitness_values, axis=1)
#
#     cost = [-x for x in average_fitnesses]  # es object minimises function, so negative fitness is defined as cost
#     es.tell(solutions, cost)
#     best_solution = es.best.get()[0]  # list of params of best solution (1 x n_param)
#     es.disp()
#
#     g += 1
#     n = 1


# Retrieve the best solution and its fitness value
# print("Best solution:", best_solution)
#
# plt.plot(range(1, len(fitnesses) + 1), fitnesses)
# plt.xlabel("Generation")
# plt.ylabel("Best Fitness Value")
# plt.title("Convergence Plot")
# plt.grid(True)
# plt.show()

# parameters = [(180 - MU_R_VIS_BEETLE) * 2 / RANGE_R_VIS_BEETLE,  # 'r_vis_bug'
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