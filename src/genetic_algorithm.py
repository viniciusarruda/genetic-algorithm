from random import randint, random

def genetic_algorithm(individual, fitness, mutate, crossover, n_individuals=10, epochs=10, crossover_rate=0.6, mutation_rate=0.2, callback=None):
	
	population = map(lambda _: individual(), xrange(n_individuals))
	retain = int(n_individuals * (1.0 - crossover_rate))

	for e in xrange(epochs):

		population = list(zip(*sorted(zip(map(fitness, population), population), key=lambda t: t[0]))[1])

		if callback is not None:
			callback(population, e)

		parents = population[:retain]

		n_parents = len(parents)
		n_offspring = n_individuals - n_parents

		offspring = []
		while len(offspring) < n_offspring:
			male, female = randint(0, n_parents-1), randint(0, n_parents-1)
			if male != female:
				offspring.append(crossover(parents[male], parents[female]))

		for i in xrange(n_offspring):
			if mutation_rate > random():
				offspring[i] = mutate(offspring[i])

		population = parents + offspring


	population = list(zip(*sorted(zip(map(fitness, population), population), key=lambda t: t[0]))[1])

	if callback is not None:
		callback(population, epochs)

	return population[0] 
	
