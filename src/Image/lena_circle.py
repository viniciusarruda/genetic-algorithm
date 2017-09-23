import math
import numpy as np
import matplotlib.pyplot as plt
import time

from skimage.draw import circle, set_color
from skimage.io import imread
from skimage.measure import compare_ssim
from skimage import img_as_float

from random import randint, random, uniform

# center, radius, color
# [x,y , r, r,g,b]

alpha = None
min_r = None
max_r = None
original = None
mx = None
my = None
img = None


def print_pop(population):
	for p in population:
		print p
	print '\n\n'

def individual():
	return [randint(0, mx), randint(0, my),
            uniform(min_r, max_r),
            random(), random(), random()]

def fitness(individual):
	tmp = img.copy()
	rr, cc = circle(individual[0], individual[1], individual[2], original.shape)
	set_color(tmp, (rr, cc), (individual[3], individual[4], individual[5]), alpha)
	return (1.0 - compare_ssim(original, tmp, multichannel=True))


def mutate(g, value):
	if g == 0:
		value *= uniform(0.9, 1.1)
		return mx if value > mx else value
	elif g == 1:
		value *= uniform(0.9, 1.1)
		return my if value > my else value
	elif g == 2:
		value *= uniform(0.9, 1.1)
		return max_r if value > max_r else min_r if value < min_r else value
	else:
		value *= uniform(0.9, 1.1)
		return 1.0 if value > 1.0 else value



def crossover(male, female):  
	w = randint(0, 2)

	if w == 0:
		return [male[0]*0.5 + female[0]*0.5, male[1]*0.5 + female[1]*0.5]  + male[2:]
	elif w == 1:
		return male[:2] + [male[2]*0.5 + female[2]*0.5] + male[3:]
	else:
		return male[:3] + [male[3]*0.5 + female[3]*0.5, male[4]*0.5 + female[4]*0.5, male[5]*0.5 + female[5]*0.5]


def genetic_algorithm(n_individuals=500, figs=300, epochs=50, selection_rate=0.05, crossover_rate=0.6, mutation_rate=0.01):

	global max_r
	global min_r

	mult_max_r = math.pow((3.0/max_r), 1.0/figs)
	mult_min_r = math.pow((2.0/min_r), 1.0/figs)

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
					children.append(crossover(parents[male], parents[female]))

			population = parents + children

			for i in population:
				for g in xrange(len(i)):
					if mutation_rate > random():
						i[g] = mutate(g, i[g])


		best = min(zip(map(fitness, population), population), key=lambda t: t[0])
		print "Fitness of adding circle: ", best[0]
		rr, cc = circle(best[1][0], best[1][1], best[1][2], original.shape)
		set_color(img, (rr, cc), (best[1][3], best[1][4], best[1][5]), alpha)

		max_r *= mult_max_r
		min_r *= mult_min_r



def main():

	global alpha, min_r, max_r, original, mx, my, img

	alpha = 0.3
	min_r = 30.0
	max_r = 40.0
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

