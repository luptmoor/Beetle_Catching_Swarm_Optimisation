from Simulation import Simulation


params = [50,       # 'r_vis_bug'
          15,       # 'r_vis_drone'
          40,       # 'r_vis_tree'
          50,       # 'k_tree'
          100,      # 'k_neardrone'
          -5,       # 'k_bug'
          - 10e-4,  # 'k_fardrone'
          - 1e-4,   # 'k_activity'
          5,        # 'v_min'
          100       # 'temp_cohesion'
          ]

sim = Simulation(params)
sim.run()
