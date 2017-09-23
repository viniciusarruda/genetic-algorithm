from random import randint, random
from genetic_algorithm import genetic_algorithm

minimum = ord('a')
maximum = ord('z')
obj = "entscheidungsproblem"
length = len(obj)

def individual():
	return [randint(minimum,maximum) for x in xrange(length)]

def fitness(chromosome):   
	f = 0                          
	for a,b in zip(obj, chromosome):
		f += abs(ord(a)-b)
	return f

def mutate(individual):
	i = randint(0, len(individual) - 1)
	individual[i] = randint(minimum,maximum)
	return individual

def crossover(male, female):
	half = randint(0, len(male)-1)
	return male[:half] + female[half:]

def callback(population, e):
	print 'Epoch #{} Best: fitness ({}) individual ({})'.format(e, fitness(population[0]), ''.join([chr(e) for e in population[0]]))


# genetic_algorithm(individual, fitness, mutate, crossover, n_individuals=10, epochs=10, crossover_rate=0.6, mutation_rate=0.2, callback=None):
genetic_algorithm(individual, fitness, mutate, crossover, 1000, 50, 0.6, 0.5, callback)
