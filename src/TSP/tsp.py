from random import randint, random, shuffle
from operator import add

from genetic_algorithm import genetic_algorithm


city_distance = [
    [   0, 2451,  713, 1018, 1631, 1374, 2408,  213, 2571,  875, 1420, 2145, 1972], # New York
    [2451,    0, 1745, 1524,  831, 1240,  959, 2596,  403, 1589, 1374,  357,  579], # Los Angeles
    [ 713, 1745,    0,  355,  920,  803, 1737,  851, 1858,  262,  940, 1453, 1260], # Chicago
    [1018, 1524,  355,    0,  700,  862, 1395, 1123, 1584,  466, 1056, 1280,  987], # Minneapolis
    [1631,  831,  920,  700,    0,  663, 1021, 1769,  949,  796,  879,  586,  371], # Denver
    [1374, 1240,  803,  862,  663,    0, 1681, 1551, 1765,  547,  225,  887,  999], # Dallas
    [2408,  959, 1737, 1395, 1021, 1681,    0, 2493,  678, 1724, 1891, 1114,  701], # Seattle
    [ 213, 2596,  851, 1123, 1769, 1551, 2493,    0, 2699, 1038, 1605, 2300, 2099], # Boston
    [2571,  403, 1858, 1584,  949, 1765,  678, 2699,    0, 1744, 1645,  653,  600], # San Francisco
    [ 875, 1589,  262,  466,  796,  547, 1724, 1038, 1744,    0,  679, 1272, 1162], # St. Louis
    [1420, 1374,  940, 1056,  879,  225, 1891, 1605, 1645,  679,    0, 1017, 1200], # Houston
    [2145,  357, 1453, 1280,  586,  887, 1114, 2300,  653, 1272, 1017,    0,  504], # Phoenix
    [1972,  579, 1260,  987,  371,  999,  701, 2099,  600, 1162,  1200,  504,   0]] # Salt Lake City
    


def individual():
	i = range(0, len(city_distance))
	shuffle(i)
	return i

def fitness(individual):
    cost = 0
    for i in xrange(0, len(individual)-1):
    	cost += city_distance[individual[i]][individual[i+1]]
    cost += city_distance[len(individual)-1][0]
    return cost

def mutate(individual):
    idx1 = randint(0, len(individual)-1)
    idx2 = randint(0, len(individual)-1)
    tmp = individual[idx1]
    individual[idx1] = individual[idx2]
    individual[idx2] = tmp
    return individual

def crossover(male, female):   # OX crossover
    n = len(male)
    idx = randint(0, n-1)
    qnt = randint(2, 7)

    offspring = [-1] * n
    gene_male = [male[i % n] for i in xrange(idx, idx+qnt)]
    gene_female = [female[i % n] for i in xrange(idx+qnt, idx+qnt+n) if female[i % n] not in gene_male]

    ii = idx
    for i in gene_male:    
        offspring[ii % n] = i
        ii += 1

    for i in gene_female:
        offspring[ii % n] = i
        ii += 1        

    return offspring

def callback(population, e):
    print 'Epoch #{} Best: fitness ({}) individual ({})'.format(e, fitness(population[0]), population[0])


genetic_algorithm(individual, fitness, mutate, crossover, 1000, 30, 0.6, 0.5, callback)

