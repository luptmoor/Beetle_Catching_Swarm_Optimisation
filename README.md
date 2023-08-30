# Bug_Catching_Swarm_Optimisation

This repository is part of a coding assignment for the course AE4350: Bio-Inspired Intelligence and Learning for Aerospace Engineering at Delft University of Technology,
supervised by prof. Guido de Croon. Aim of this programme is optimising a simulated drone swarm in 2D
to catch beetles, inspired by the invasive Asian Longhorned Beetle (A. glabripennis). The optimisation is conducted using CMA-ES by importing library 'cma'. Please contact
the author Lukas Uptmoor for a full report about this project. To run the code, adjust settings.py to your wishes and then run main.py.

## settings.py
This file contains all adjustable global parameters, marked by full capitalisation, like simulation settings, visualisation settings, CMA-ES settings and the initial parameter
ranges.

## main.py
This file contains the setup of the evolutionary algorithm, the optimisation loop and exporting of optimisation results to a CSV file using pandas.

## Simulation.py
This file houses the Simulation class, which contains all information and functions to run a simulation with a specified parameter set and seed. Also, the fitness function can
be found in this file.

## Visuals.py
If enabled in the settings, this file takes care of the graphical visualisation of the simulation, using pygame, which is helpful for verification of the simulation process.
The simulation can be halted and resumed pressing the spacebar.
When pressing 'v', it is cycled between 4 views.
0: Default, 1: Drone vision radii and influenced objects, 2: Bug vision radii and attached trees, 3: Drone mid-range communication and activity levels (# of visible bugs).

## Entity.py
Parent class for all physical objects.

## Bug.py
This file contains the Bug class, which contains the bugs' dynamics according to the different modes.

## Drone.py
This file contains the Drone class, which controls the drones' dynamics based on the tunable parameters.
