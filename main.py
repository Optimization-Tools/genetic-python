#!/usr/bin/python
from genetic import *

MUTATE_CHANCE = 0.1
GENOME_LENGTH = 30
GENERATION_SIZE = 1000
MAX_GENERATIONS = 1000

def main():
    fitness = Fitness()
    env = Environment(TournamentSelection(), fitness, MUTATE_CHANCE)
    env.seed(GENERATION_SIZE, GENOME_LENGTH)
    generation = 1

    while generation < MAX_GENERATIONS and env.max_score < fitness.max_score:
        env.run()
        generation += 1

if __name__ == "__main__":
    main()