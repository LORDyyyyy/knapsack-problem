import random
import math
from typing import List
from .knapsack import Knapsack

Genome = Knapsack
Population = List[Genome]


class Genetic:
    """Genetic Algorithm for 1-0 Knapsack"""

    def fitness(self, genome: Genome) -> int:
        """Determine how much a solution
        is good for our problem"""

        if genome.get_weight() > Knapsack.maximum_capacity:
            return 0

        return genome.get_value()

    def generate_genome(self) -> Genome:
        """Generate a genome with random values"""

        genome = Genome(
            random.choices(population=[False, True], weights=[
                           0.95, 0.05], k=Knapsack.n)
        )

        return genome

    def generate_population(self, k: int) -> Population:
        """Make generation 0 with k genomes"""

        generation = [self.generate_genome() for _ in range(k)]
        return generation

    def natural_selection(self, population: Population, k: int) -> Population:
        """Select best k solution from a
        generation based on genomes' fitness"""

        population.sort(key=self.fitness, reverse=True)

        if k > len(population) or k <= 0:
            return population

        return population[:k]

    def select_parents(self, population: Population) -> List[Genome]:
        """Select two parents from a population"""

        parents = random.choices(population=population, k=2)
        return parents

    def crossover(self, parents: List[Genome]) -> List[Genome]:
        """Generate k genomes from two parents
        with random portion from each parent's dna"""

        cross_point = random.randrange(Knapsack.n + 1)
        genomes = [
            Genome(
                parents[0].selected_items[:cross_point]
                + parents[1].selected_items[cross_point:]
            ),
            Genome(
                parents[1].selected_items[:cross_point]
                + parents[0].selected_items[cross_point:]
            ),
        ]

        return genomes

    def mutation(self, genome: Genome, mutation_rate: float = 0.05) -> Genome:
        """Change point(s) is genome's dna to achieve variety"""

        points = random.choice(
            range(math.ceil(Knapsack.n * mutation_rate) + 1))
        new_genome = Genome(genome.selected_items)

        for _ in range(points):
            index = random.randrange(Knapsack.n)
            new_genome.change_quantity(index=index)

        return new_genome

    def make_generation(self, population: Population, k: int) -> Population:
        """Make new generation based on current generation with k genomes"""

        generation = []
        for _ in range(k):
            parents = self.select_parents(population=population)
            genomes = self.crossover(parents=parents)
            generation += genomes

        generation = [self.mutation(genome) for genome in generation]
        return generation

    def evolution(self, lim: int = 100) -> tuple[Knapsack, List[int]]:
        """Evolution function"""

        generation = self.generate_population(k=1200)
        result = generation[0]
        gen_fitness = []

        for gen in range(lim):
            top_genomes = self.natural_selection(population=generation, k=100)
            best_genome = top_genomes[0]
            gen_fitness.append(self.fitness(best_genome))

            if self.fitness(best_genome) > self.fitness(result):
                result = best_genome

            yield (
                f"Generation {gen}'s best solution is {
                    self.fitness(best_genome)}",
                "",
            )

            generation = self.make_generation(population=top_genomes, k=1200)

        yield result, gen_fitness


class UnboundedGenetic(Genetic):
    """Unbounded version of genetic algorithm"""

    def mutation(self, genome: Genome, mutation_rate: float = 0.05) -> Genome:
        """Change point(s) is genome's dna to achieve variety"""

        points = random.choice(
            range(math.ceil(Knapsack.n * mutation_rate) + 1))
        new_genome = Genome(genome.selected_items)

        for _ in range(points):
            index = random.randrange(Knapsack.n)
            current = genome.selected_items[index]
            lim = Knapsack.maximum_capacity // Knapsack.available_items[index].weight

            diff = random.choice(
                list(range(max(-current, -5), 1))
                + list(range(min(lim - current, 5) + 1))
            )

            new_genome.change_quantity(index=index, quantity=current + diff)

        return new_genome
