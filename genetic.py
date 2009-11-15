"""
Genetic Algorithm Builder
"""

import pdb

from random import randint, random
from Gene import Gene

MUTATION_RATE = 0.0001

def binsearch(items, val, get=lambda x: x):
    """
    Returns the item in items whose bucket contains val - assumes items is (item, bottom of bucket)
    """
    low, high = 0, len(items)-1
    while ((high - low) > 1):
        if val < get(items[(low+high)/2]):
            high = (low+high)/2 
        elif val == get(items[(low+high)/2]):
            low = high = (low+high)/2
        else:
            low = (low+high)/2 

    return items[high]


def roulette(items, num, get=lambda x: x):
    """
    Runs a roulette selection algorithm on the items in the list given. 
    The algorithm is roughly a binary search on the list to find out which item is to be selected (with random values)
    """
    max_value = max(items, key=get)

    selection = [ binsearch(items, random() *  (get(max_value)), get) for i in xrange(num)]
    return selection

def evolve(population):
    """
    Evolve the initial population a generation at a time
    Expects that the input population is a class that computes 
    the fitness and mates two members
    """
    # Initialise the algorithm

    population_limit = len(population)
    mutation_rate = MUTATION_RATE
    population.sort(key = lambda x: x.fitness)

    while(True):
        # Select Breeders
        # At this point the population is already sorted!

        # Construct a "cdf" 
        sum = 0
        items = []
        for x in population: 
            sum += x.fitness
            items.append((x, sum))
        
        matables = roulette(items, population_limit, lambda x: x[1])
        mating_pairs = [(matables[i][0], matables[i+len(matables)/2][0]) for i in xrange(len(matables)/2)]

        # Mate Pairs
        for pair in mating_pairs:
            children = pair[0].mate(pair[1])
            if random() < mutation_rate:
                children = [child.mutate() for child in children]
            population += children
        
        # Select fittest
        population.sort(key = lambda x: x.fitness)
        population = population[:population_limit]

        yield population
        
