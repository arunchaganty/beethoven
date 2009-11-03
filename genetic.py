"""
Genetic Algorithm Builder
"""

from random import randint

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

    selection = [ binsearch(items, randint(0, get(max_value)), get) for i in xrange(num)]
    return selection

def evolve(population, population_limit):
    # Initialise the algorithm

    while(True):
        # Select Breeders
        # At this point the population is already sorted!

        # Construct a "cdf" 
        sum = 0
        items = []
        for x in population: 
            sum += x.fitness
            items += (x, sum)
        
        matables = roulette(items)
        
        
        
        # Mate Pairs
        
        
        # Select fittest
        population.sort(cmp = lambda x,y: x.fitness - y.fitness)
        population = population[:population_limit]
        
