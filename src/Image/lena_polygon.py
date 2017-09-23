import time
import numpy as np
import matplotlib.pyplot as plt

from skimage.draw import polygon, set_color
from skimage.io import imread
from skimage.measure import compare_ssim
from skimage import img_as_float

from random import randint, random, uniform

# center, radius, color
# [x,y , r, r,g,b]

alpha = None
original = None
mx = None
my = None
img = None




def print_pop(population):
	for p in population:
		print p
	print '\n\n'


def individual():
	n = randint(3, 5)
	return [np.array([uniform(0, mx) for _ in xrange(n)]), np.array([uniform(0, my) for _ in xrange(n)]), random(), random(), random()]

def fitness(individual):
	tmp = img.copy()
	rr, cc = polygon(individual[0], individual[1], original.shape)
	set_color(tmp, (rr, cc), (individual[2], individual[3], individual[4]), alpha)
	return (1.0 - compare_ssim(original, tmp, multichannel=True))


def mutate_x(value):
	value *= uniform(0.9, 1.1)
	return mx if value > mx else value

def mutate_y(value):
	value *= uniform(0.9, 1.1)
	return mx if value > mx else value

def mutate_grow(x, y):
	idx = randint(0, len(x))
	return np.insert(x, idx, uniform(0, mx)), np.insert(y, idx, uniform(0, my)) 

def mutate_color(r, g, b):
	r *= uniform(0.9, 1.1)
	g *= uniform(0.9, 1.1)
	b *= uniform(0.9, 1.1)

	r = 1.0 if r > 1.0 else r
	g = 1.0 if g > 1.0 else g
	b = 1.0 if b > 1.0 else b

	return r, g, b




def crossover(male, female): 
	return [[male[0].copy()] + [male[1].copy()] + female[2:]] + [[female[0].copy()] + [female[1].copy()] + male[2:]]


def genetic_algorithm(n_individuals=500, figs=100, epochs=50, selection_rate=0.05, crossover_rate=0.6, mutation_rate=0.01):

	retain = int(n_individuals * (1.0 - crossover_rate))

	for _ in xrange(figs): 

		population = map(lambda _: individual(), xrange(n_individuals))

		for _ in xrange(epochs):
			
			population = list(zip(*sorted(zip(map(fitness, population), population), key=lambda t: t[0]))[1])

			parents = population[:retain] + [i for i in population[retain:] if selection_rate > random()]

			n_parents = len(parents)
			n_children = n_individuals - n_parents

			children = []
			while len(children) < n_children:
				male, female = randint(0, n_parents-1), randint(0, n_parents-1)
				if male != female:
					children.extend(crossover(parents[male], parents[female]))

			population = parents + children

			for i in population:
				for g in xrange(len(i[0])):
					if mutation_rate > random():
						i[0][g] = mutate_x(i[0][g])					

			for i in population:
				for g in xrange(len(i[1])):
					if mutation_rate > random():
						i[1][g] = mutate_y(i[1][g])

			for i in population:
				if mutation_rate > random():
					i[0], i[1] = mutate_grow(i[0], i[1])

			for i in population:
				if mutation_rate > random():
					i[2], i[3], i[4] = mutate_color(i[2], i[3], i[4])


		best = min(zip(map(fitness, population), population), key=lambda t: t[0])
		print "Fitness of adding circle: ", best[0]
		rr, cc = polygon(best[1][0], best[1][1], original.shape)
		set_color(img, (rr, cc), (best[1][2], best[1][3], best[1][4]), alpha)



def main():
	
	global alpha, original, mx, my, img

	alpha = 0.3
	original = img_as_float(imread('lena.png'))
	mx, my, _ = original.shape
	img = np.zeros(original.shape, dtype=np.double)

	start = time.clock()
	genetic_algorithm()
	print "Time elapsed: ", time.clock() - start

	print "Final fitness: ", (1.0 - compare_ssim(original, img, multichannel=True))

	fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(6, 3))
	ax1.imshow(original)
	ax1.set_title('Original')
	ax2.imshow(img)
	ax2.set_title('Generated')
	plt.show()


if __name__ == "__main__": 
	main()

