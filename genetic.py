import random


class Individual(object):
    """ An individual solution """
    def __init__(self, genome, parent1, parent2):
        self.genome = genome
        self.parent1 = parent1
        self.parent2 = parent2
        self.fitness = None

    def breed(self, partner, mutation_chance):
        """ Breed this individual with another and generate two children """
        genes = self.genome.crossover(partner.genome, mutation_chance)

        return [Individual(g, self, partner) for g in genes]


class Genome(object):
    """ Genome that defines the genetic code of each individual """
    chromosomes = 'ULDRN'

    def __init__(self, genes):
        self.genes = genes
        self.mutant = False

    def crossover(self, genome, mutation_chance):
        """ Cross this genome with another and return two offspring """
        offspring = []
        splice = 1 + random.randint(0, len(self.genes) - 1)

        offspring.append(Genome(self.genes[0:splice] + genome.genes[splice:]))
        offspring.append(Genome(genome.genes[0:splice] + self.genes[splice:]))
        map(lambda o: o.mutate(mutation_chance), offspring)

        return offspring

    def mutate(self, chance):
        """ Mutate this genome if chance """
        if random.random() <= chance:
            splice = random.randint(0, len(self.genes) - 1)
            # don't replace chromosome with same one
            chars = Genome.chromosomes.replace(self.genes[splice], '')
            self.genes = (self.genes[:splice] +
                          Genome.get_random_string(1, chars) +
                          self.genes[splice + 1:])

    def __str__(self):
        return self.genes

    @staticmethod
    def random(length):
        """ Create a Genome with random genes """
        return Genome(Genome.get_random_string(length))

    @staticmethod
    def get_random_string(length, chars=chromosomes):
        """ Create string of size length of random characters """
        return ''.join(random.choice(chars) for x in range(length))


class Generation(object):
    """ A generation of individual solutions """
    def __init__(self, number, population):
        self.number = number
        self.population = population

    def output(self):
        """ Display the highest scoring individuals in this generation """
        def output_helper(i):
            print "%s %d %s | %s x %s" % (
                i.genome.genes,
                i.fitness,
                '*' if i.genome.mutant else ' ',
                i.parent1.genome if i.parent1 else 'none',
                i.parent2.genome if i.parent2 else 'none'
            )

        max_score = self.get_max_score()
        print "Generation #%d, Score: %d" % (self.number, max_score)
        map(output_helper,
            filter(lambda i: i.fitness == max_score, self.population))

    def get_max_score(self):
        """ Get the highest score of individuals in this generation """
        return max([i.fitness for i in self.population])


class Fitness(object):
    """ Evaluate an field for fitness bases on the number of nodes visited """
    max_score = field_size = 25

    def test(self, individual, output=False):
        """ Test an individual and determine it's fitness score """
        field = self.get_empty_field()
        position = 0
        field[0] = 1

        for g in individual.genome.genes:
            field, position = self.move(field, position, g)

        if output:
            self.print_field(field)

        return self.get_score(field)

    def move(self, field, position, direction):
        """ Given a field and position, update the field for a movement
            in a direction """
        def up(position):
            if position > 4:
                position -= 5
                field[position] = 1
            return (field, position)

        def down(position):
            if position < 20:
                position += 5
                field[position] = 1
            return (field, position)

        def left(position):
            if position % 5 != 0:
                position -= 1
                field[position] = 1
            return (field, position)

        def right(position):
            if position % 5 != 4:
                position += 1
                field[position] = 1
            return (field, position)

        def nop(population):
            return (field, position)

        return {
            'U': up,
            'D': down,
            'L': left,
            'R': right,
            'N': nop
        }[direction](position)

    def print_field(self, field):
        """ Display the visited nodes in a field """
        for i in range(len(field)):
            print '*' if field[i] == 1 else '.',
            if i % 5 == 4:
                print

    def get_score(self, field):
        """ Get the fitness score for a field """
        return sum(field)

    def get_empty_field(self):
        """ Get an unvisited field """
        return [0] * Fitness.field_size


class TournamentSelection(object):
    """ Select individuals by random matchups """
    def select_parents(self, population):
        parents = []

        while len(parents) < len(population):
            c2 = c1 = random.randint(0, len(population) - 1)

            while c2 == c1:
                c2 = random.randint(0, len(population) - 1)

            if population[c1].fitness > population[c2].fitness:
                parents.append(population[c1])
            else:
                parents.append(population[c2])

        return parents


class FitnessProportionateSelection(object):
    """ Select individuals randomly, weighted by fitness """
    def select_parents(self, population):
        parents = []
        scoreboard = self.get_scoreboard(population)

        while len(parents) < len(population):
            parents.append(scoreboard[random.randint(0, len(scoreboard) - 1)])

        return parents

    def get_scoreboard(self, population):
        return [individual for individual in population
                           for i in range(individual.fitness)]


class Environment(object):
    """ The environment in which generations exist """
    def __init__(self, selection, fitness, mutate_chance):
        self.selection = selection
        self.fitness = fitness
        self.mutate_chance = mutate_chance
        self.generations = []
        self.max_score = 0

    def seed(self, num_individuals, genome_length):
        """ Generate the first generation of individuals """
        self.generations.append(
            Generation(1, self.get_random_population(num_individuals,
                                                     genome_length)))
        self.max_score = self.generations[-1].get_max_score()
        #self.generations[-1].output()

    def run(self, output=True):
        """ Run one iteration """
        offspring = []
        parents = self.selection.select_parents(
            self.generations[-1].population)

        for i in range(0, len(parents), 2):
            offspring += parents[i].breed(parents[i + 1], self.mutate_chance)

        self.calculate_fitnesses(offspring)
        self.generations.append(Generation(len(self.generations) + 1,
                                           offspring))
        self.max_score = self.generations[-1].get_max_score()

        if output:
            self.generations[-1].output()

    def get_random_population(self, size, genome_length):
        """ Get a population of random invidivuals """
        population = [Individual(Genome.random(genome_length), None, None)
                      for i in range(size)]
        self.calculate_fitnesses(population)

        return population

    def calculate_fitnesses(self, population):
        """ Calculate the fitness for a population of invidivuals """
        for individual in population:
            individual.fitness = self.fitness.test(individual)
