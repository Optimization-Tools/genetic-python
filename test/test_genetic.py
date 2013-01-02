import unittest
import copy
from genetic import *

GENOME_LENGTH = 25
POPULATION_SIZE = 100

class TestIndividual(unittest.TestCase):
    def test_breed(self):
        individual1 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual2 = Individual(Genome.random(GENOME_LENGTH), None, None)
        children = individual1.breed(individual2, 0)
        self.assertEqual(len(children), 2)


class TestGenome(unittest.TestCase):
    def test_random(self):
        genome = Genome.random(GENOME_LENGTH)
        self.assertTrue(isinstance(genome, Genome))
        self.assertEqual(len(genome.genes), GENOME_LENGTH)

    def test_get_random_string(self):
        gene = Genome.get_random_string(GENOME_LENGTH)
        self.assertEqual(len(gene), GENOME_LENGTH)

    def test_crossover(self):
        genome1 = Genome.random(GENOME_LENGTH)
        genome2 = Genome.random(GENOME_LENGTH)
        offspring = genome1.crossover(genome2, 0)
        self.assertEqual(len(offspring), 2)
        self.assertEqual(len(offspring[0].genes), GENOME_LENGTH)
        self.assertEqual(len(offspring[1].genes), GENOME_LENGTH)

    def test_mutate_mutates(self):
        genome1 = Genome.random(GENOME_LENGTH)
        genome2 = copy.copy(genome1)
        genome1.mutate(1)
        self.assertNotEqual(genome1.genes, genome2.genes)
        self.assertEqual(len(genome1.genes), GENOME_LENGTH)

    def test_mutate_does_not_mutate(self):
        genome1 = Genome.random(GENOME_LENGTH)
        genome2 = copy.copy(genome1)
        genome1.mutate(0)
        self.assertEqual(genome1.genes, genome2.genes)
        self.assertEqual(len(genome1.genes), GENOME_LENGTH)


class TestGeneration(unittest.TestCase):
    def test_output(self):
        pass

    def test_get_max_score(self):
        individual1 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual2 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual3 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual1.fitness = 0
        individual2.fitness = 100
        individual3.fitness = 50
        generation = Generation(3, [individual1, individual2, individual3])
        self.assertEqual(generation.get_max_score(), 100)


class TestFitness(unittest.TestCase):
    def test_get_score_empty(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_score(fitness.get_empty_field()), 0)

    def test_get_score_not_empty(self):
        fitness = Fitness()
        field = fitness.get_empty_field()
        field[1] = 1
        self.assertEqual(fitness.get_score(field), 1)

    def test_get_empty_field(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_empty_field(), [0] * Fitness.field_size)

    def test_move_up(self):
        fitness = Fitness()
        field = fitness.get_empty_field()
        f, p = fitness.move(field, 5, 'U')
        self.assertEqual(f[0], 1)

    def test_move_down(self):
        fitness = Fitness()
        field = fitness.get_empty_field()
        f, p = fitness.move(field, 0, 'D')
        self.assertEqual(f[5], 1)

    def test_move_left(self):
        fitness = Fitness()
        field = fitness.get_empty_field()
        f, p = fitness.move(field, 1, 'L')
        self.assertEqual(f[0], 1)

    def test_move_right(self):
        fitness = Fitness()
        field = fitness.get_empty_field()
        f, p = fitness.move(field, 0, 'R')
        self.assertEqual(f[1], 1)

    def test_test(self):
        fitness = Fitness()
        individual = Individual(Genome('DRUL'), None, None)
        score = fitness.test(individual)
        self.assertEqual(score, 4)

    def test_print_field(self):
        pass


class TestTournamentSelection(unittest.TestCase):
    def test_select_parents(self):
        selection = TournamentSelection()
        population = [Individual(Genome.random(GENOME_LENGTH), None, None) for i in range(10)]
        parents = selection.select_parents(population)
        self.assertEqual(len(parents), len(population))


class TestFitnessProportionateSelection(unittest.TestCase):
    def test_select_parents(self):
        selection = FitnessProportionateSelection()
        individual1 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual2 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual1.fitness = 5
        individual2.fitness = 3
        parents = selection.select_parents([individual1, individual2])
        self.assertEqual(len(parents), 2)        

    def test_get_scoreboard(self):
        selection = FitnessProportionateSelection()
        individual1 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual2 = Individual(Genome.random(GENOME_LENGTH), None, None)
        individual1.fitness = 5
        individual2.fitness = 3
        scoreboard = selection.get_scoreboard([individual1, individual2])
        self.assertEqual(len(scoreboard), 8)


class TestEnvironment(unittest.TestCase):
    def test_get_random_population(self):
        env = Environment(FitnessProportionateSelection(), Fitness(), 0)
        population = env.get_random_population(10, GENOME_LENGTH)
        self.assertEqual(len(population), 10)

    def test_seed(self):
        env = Environment(FitnessProportionateSelection(), Fitness(), 0)
        env.seed(POPULATION_SIZE, GENOME_LENGTH)
        self.assertTrue(env.max_score > 0)
        self.assertEqual(len(env.generations), 1)

    def test_run(self):
        env = Environment(FitnessProportionateSelection(), Fitness(), 0)
        env.seed(POPULATION_SIZE, GENOME_LENGTH)
        env.run(False)



if __name__ == "__main__":
    unittest.main()