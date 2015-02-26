from __future__ import division

from base import memo

CONFIG = memo(
    Searcher=memo(era_length=50, terminate_early=True,
                  log_energies=True,
                  iterations=1000, p_mutation=1/3, epsilon=.01),
    SimulatedAnnealer=memo(cooling_factor=.8),
    MaxWalkSat=memo(),
    GeneticAlgorithm=memo(population_size=50, p_mutation=.001,
                          crossovers=2),
    DifferentialEvolution=memo(generations=100, n_candiates=100,
                               f=.75, p_crossover=.3),
    ParticleSwarmOptimizer=memo(population_size=30, phi1=2.8, phi2=1.3,
                                generations=100))
