# Martín van Puffelen López
# 0-1 Knapsack problem using Genetic Algorithms.

import numpy as np
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random


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
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT: # Erase individuals which are overweight or too many items.
        return 10000, 0
    return weight, value

def cycleCross(p1,p2):
    elementsChecked = 1
    cycleNum = 1
    cycles = [0] * len(p1)
    cycles[0] = cycleNum
    child = [0] * len(p1)
    i = 0
    j = 0
    while elementsChecked < len(p1):
        if p1[i] == p2[j]:
            cycles[j] = cycleNum
            i = j
            j = 0
            elementsChecked += 1
        j += 1
        if j == len(p1) and elementsChecked < len(p1):
            j = 0
            for k in range(len(p1)):
                if cycles[k] == 0:
                    i = k
                    cycleNum += 1
                    cycles[k] = cycleNum
                    elementsChecked += 1
                    break

    for k in range(len(cycles)):
        if cycles[k] % 2 == 0:  # Even cycle picks mother genes
            child[k] = p2[k]
        else:  # Odd cycle picks mother genes
            child[k] = p1[k]
    return child

def cxSet(ind1, ind2): # Crossover Function Using Cycle Cross
    ind3=list(ind1)
    ind4=list(ind2)
    # print("SET:",ind1,"LIST",ind3)
    if len(ind3) == len(ind4) and len(ind3)!=0:
        child=cycleCross(ind3,ind4)
        child=creator.Individual(set(child))
        # print(child)
        return child, ind2
    else:
        ind2 -= ind1                    # Difference (inplace)
        return ind1, ind2

def mutSet(individual): # Mutation function
    if random.random() < 0.5:
        if len(individual) > 0:
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(N_ITEMS))
    return individual,

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)


def main():
    random.seed(128)
    NGEN = 100 # Number of generations
    POPSIZE = 50 # Population size
    CXPB = 0.6 # Cross-over probability
    MUTPB = 0.3 # Mutation probability
    LAMBDA = 100 # Offspring size

    pop = toolbox.population(n=POPSIZE)
    hof = tools.ParetoFront() # Contains list of fittest individuals
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)


    # algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats,
    #                           halloffame=hof) # It uses mutation+crossover
    #
    algorithms.eaMuPlusLambda(pop, toolbox, POPSIZE, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof) # It uses mutation or crossover or reproduction every lambda iterations

    return pop, stats, hof

if __name__ == "__main__":
    pop, stats, hof= main()
    print("Best individual:", hof[-1])
    for item in hof[-1]: # Selected elements
        print(items[item])
    print("The weight and value:", evalKnapsack(hof[-1]))