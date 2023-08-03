from Simulation import Simulation


params = {
    'r_vis_bug': 50,
    'r_vis_drone': 15,
    'r_vis_tree': 40,
    'k_tree': 50,
    'k_neardrone': 100,
    'k_bug': -5,
    'k_fardrone': - 10e-4,
    'k_activity': - 1e-4,
    'v_min': 5,
    'temp_cohesion': 100
}

sim = Simulation(params)
sim.run()
