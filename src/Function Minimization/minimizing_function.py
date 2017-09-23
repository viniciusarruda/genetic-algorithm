####################################################################################
#                                                                                  #
# The MIT License (MIT)                                                            #
#                                                                                  #
# Copyright (c) 2017 viniciusferracoarruda@gmail.com (viniciusarruda.github.io)    #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy of  #
# this software and associated documentation files (the "Software"), to deal in    #
# the Software without restriction, including without limitation the rights to     #
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of #
# the Software, and to permit persons to whom the Software is furnished to do so,  #
# subject to the following conditions:                                             #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS #
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR   #
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER   #
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN          #
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.       #
#                                                                                  #
####################################################################################


from random import randint, random, uniform
from genetic_algorithm import genetic_algorithm
import numpy as np
import pylab as plt


# Data for draw the level curve of the function
row = np.linspace(-2,3.3,200)
col = np.linspace(-3,2.3,200)
X,Y = np.meshgrid(row,col)
Z   = -np.exp(-((X-1.5)**2+(Y+1)**2)) - np.exp(-((X)**2+(Y)**2))


 # - e^(-((x-1.5)^2 + (y+1)^2)) - e^(-(x^2 + y^2))

# Figure
fig = plt.figure(figsize=(10,30))
plt.ion()
ax = fig.add_subplot(111)

# min and max x,y where the individuals can be
x_min = -1.7
x_max = 3.1
y_min = -2.7
y_max = 2.1

# Function to create a new random individual
def individual():
	return (uniform(x_min, x_max), uniform(y_min, y_max))

# Function that evaluates an individual
def fitness(individual):
	x, y = individual
	return -np.exp(-((x-1.5)**2+(y+1)**2)) - np.exp(-((x)**2+(y)**2))

# Function that mutates an individual
def mutate(individual):
	x, y = individual
	return (uniform(-0.1, 0.1) * x, uniform(-0.1, 0.1) * y)

# Given two parents, it returns the offspring of them
def crossover(male, female):
	mx, _ = male
	_, fy = female
	return (mx, fy)

# Callback function to render the animation
def callback(population, epoch):
	ax.cla()
	plt.contourf(X,Y,Z, 10)
	ax.set_title('Epoch: {}'.format(epoch))
	yaxis = 2.2
	ax.text(x_min, yaxis, 'Offspring (#, fitness)', bbox={'facecolor':'red', 'alpha':0, 'pad':100})
	yaxis -= 0.12
	i = 0
	for x, y in population:
		yaxis -= 0.12
		ax.text(x_min, yaxis, '({}, {:0.5f})\n'.format(i, fitness((x, y))), bbox={'facecolor':'red', 'alpha':0, 'pad':100})
		plt.scatter(x, y)
		i += 1
		plt.pause(0.5)
	plt.pause(1)


if __name__ == '__main__':
	best = genetic_algorithm(individual=individual, fitness=fitness, mutate=mutate, crossover=crossover, callback=callback)
	while True:
		plt.pause(0.05)
