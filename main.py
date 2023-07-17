import logging
import random
import sys
from collections import Counter


class Chromosome:
    def __init__(self, gens: list, value: int):
        self.gens = gens
        self.value = value

    def __repr__(self):
        return f'gens={self.gens} value={self.value}'

    def __eq__(self, other):
        return isinstance(other, Chromosome) and self.gens == other.gens


def initialize_population(n: int) -> list:
    """Create a random population. Gets the count of population as parameter."""
    population = []
    for _ in range(n):
        gens = [random.randrange(0, QUEENS) for _ in range(QUEENS)]
        population.append(Chromosome(gens, fitness(gens)))
    return population


def crossover(chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
    """Combination of two parents and generate a new child."""
    gens = [*chromosome1.gens[:QUEENS // 2], *chromosome2.gens[QUEENS // 2:]]
    return Chromosome(gens, fitness(gens))


def optimize_population(population: list, max_population: int = 300) -> list:
    """Remove bad chromosomes if the population overheads."""
    if len(population) < max_population:
        return population
    return population[:max_population]


def add_threats(threats: set, frequency: list):
    """This is a helper function that will only call by fitness function."""
    for key, value in dict(Counter(frequency)).items():
        if value > 1:
            for i, v in enumerate(frequency):
                if v == key:
                    threats.add(i)


def fitness(gens: list) -> int:
    """Evaluate how good is the chromosome."""
    queens_in_threat = set()
    # horizontal threats
    add_threats(queens_in_threat, gens)
    # diagonal threats
    sum_row_column = [row + column for row, column in enumerate(gens)]
    diff_row_column = [abs(row - column) for row, column in enumerate(gens)]
    add_threats(queens_in_threat, sum_row_column)
    add_threats(queens_in_threat, diff_row_column)
    return len(queens_in_threat)


def mutation(chromosome: Chromosome):
    frequency = dict(Counter(chromosome.gens))
    _max = max(frequency.values())
    index = random.randrange(0, QUEENS)
    if _max > 1:
        for k, v in frequency.items():
            if v == _max:
                index = chromosome.gens.index(k)
    chromosome.gens[index] = random.randrange(0, QUEENS)
    chromosome.value = fitness(chromosome.gens)


def select_parents(population: list) -> list:
    """This function splits the sorted population into 4 slices and shuffle each slice and then append all of them.

    Groups: Excellent | Good | Normal | Bad
    """
    n = len(population)
    groups = (population[:n // 4],
              population[n // 4:n // 2],
              population[n // 2:n * 3 // 4],
              population[n * 3 // 4:],
              )
    result = []
    for i in groups:
        random.shuffle(i)
        result.extend(i)
    return result


def main():
    population = initialize_population(10)
    population.sort(key=lambda x: x.value)
    for i in range(30000):
        population = select_parents(population)
        children = [crossover(population[j - 1], population[j]) for j in range(1, len(population), 2)]
        for j, child in enumerate(children):
            # The mutation rate is 20%
            if j % 5 == 0:
                mutation(child)
            if child not in population:
                population.append(child)
        population.sort(key=lambda x: x.value)
        if population[0].value == 0:
            print('Solution found:', population[0])
            break
        population = optimize_population(population)
        log.info(f'In i={i} population={len(population)} bestFit={population[0].value}')
    else:
        print(f'Solution not found.\nThe best: {population[0]}')


if __name__ == '__main__':
    QUEENS = 10
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    log = logging.getLogger(__name__)
    main()
