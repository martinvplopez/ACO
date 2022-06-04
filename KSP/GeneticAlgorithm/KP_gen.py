import numpy as np
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random


# https://deap.readthedocs.io/en/master/examples/ga_knapsack.html

N_INIT = 5 # Number of times an individual is instantiated
MAX_ITEM = 10 # Maximum number of items that can be in the bag
MAX_WEIGHT = 50 # Bag´s capacity
N_ITEMS = 20 # Number of objects which are choosable

# Item´s dictionary: identifier:(weight,value)
items = {}
for i in range(N_ITEMS):
    items[i] = (random.randint(1, 10), random.randint(0, 35))

print(items)

creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0)) # Minimize weight and maximize value inside the bag
creator.create("Individual", set, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("attr_item", random.randrange, N_ITEMS)
toolbox.register("individual", tools.initRepeat, creator.Individual,
toolbox.attr_item, N_INIT)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0             # Erase individuals which are overweight or too many items.
    return weight, value

def cxSet(ind1, ind2): # Crossover Function
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2

def mutSet(individual): # Mutation function
    if random.random() < 0.5:
        if len(individual) > 0:     # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(N_ITEMS))
    return individual,

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2) # http://repository.ias.ac.in/83498/1/2-a.pdf


def main():
    random.seed(128)
    NGEN = 50 # Number of generations
    POPSIZE = 50 # Population size
    CXPB = 0.7 # Cross-over probability
    MUTPB = 0.2 # Mutation probability
    LAMBDA = 100 # Offspring size

    pop = toolbox.population(n=POPSIZE)
    hof = tools.ParetoFront() # Contains list of fittest individuals
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    # stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)


    # algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats,
    #                           halloffame=hof) # It uses mutation+crossover

    algorithms.eaMuPlusLambda(pop, toolbox, POPSIZE, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof) # It uses mutation or crossover or selection defined by lambda iterations

    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof = main()
    print("Best individual:", hof[-1])
    print(len(pop))
    print(len(hof))
    print("The weight and value of the best package (best fitness):", evalKnapsack(hof[-1]))