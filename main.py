from Simulation import Simulation
import cma
import numpy as np
import matplotlib.pyplot as plt


def fitness(params):
    sim = Simulation(params)
    score = sim.run()
    return score


# Set up of the CMA-ES hyperparameters
initial_mean = np.zeros(10)
initial_sigma = 0.5
population_size = 10
max_iterations = 10

options = {
    'maxiter': max_iterations,
}

# Run the CMA-ES optimization
es = cma.CMAEvolutionStrategy(initial_mean, initial_sigma, options)
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
