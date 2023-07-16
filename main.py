import random
from collections import Counter


QUEENS = 10


class Chromosome:
    def __init__(self, gens: list, value: int):
        self.gens = gens
        self.value = value


def initialize_population(n: int) -> list:
    """Create a random population. Gets the count of population as parameter"""
    population = []
    for _ in range(n):
        # TODO: random states
        gens = list(range(QUEENS))
        random.shuffle(gens)
        population.append(Chromosome(gens, fitness(gens)))
    return population


def crossover(chromosome1: Chromosome, chromosome2: Chromosome) -> Chromosome:
    """Combination of two parents and generate a new child."""
    gens = [*chromosome1.gens[:QUEENS // 2], *chromosome2.gens[QUEENS:]]
    return Chromosome(gens, fitness(gens))


def optimize_population(population: list, max_population: int = 1000) -> list:
    """Remove bad chromosomes if the population overheads."""
    if len(population) < max_population:
        return population
    population.sort(key=lambda x: x.value, reverse=True)
    return population[:max_population]


def fitness(gens: list) -> int:
    """Evaluate how good is the chromosome."""
    threats = 0
    # horizontal threats
    frequency = dict(Counter(gens))
    for i in frequency.values():
        threats += i if i > 1 else 0
    # diagonal threats
    sum_row_column = [row + column for row, column in enumerate(gens)]
    diff_row_column = [abs(row - column) for row, column in enumerate(gens)]
    for i in dict(Counter(sum_row_column)).values():
        threats += i if i > 1 else 0
    for i in dict(Counter(diff_row_column)).values():
        threats += i if i > 1 else 0
    return threats


def selection_parents():
    """The selection process for selecting the individuals who will become the parents."""
    pass



