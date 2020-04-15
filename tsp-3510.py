import sys
import itertools
import random
import time
import math
import matplotlib.pyplot as plt
# cost is 29000 for sample input

initTour = []
start = time.time()

def main(args):

	maxTime = args[3]
	output_filename = args[2]
	f = open(args[1], 'r')
	# {node: (x, y)}
	nodes = dict()
	for line in f:
		parts = line.split()
		node = int(parts[0])
		x = float(parts[1])
		y = float(parts[2])
		nodes[node] = (x,y)

		plt.plot(x, y, marker='o')
	# initialize pairwise distance matrix
	pairwise = [[0 for i in range(len(nodes)+1)] for j in range(len(nodes)+1)]

	# go through all nodes to find distances
	for i in nodes:
		first = nodes[i]
		for j in nodes:
			second = nodes[j]
			if i is not j:
				# get euclidean distance
				xdiff = first[0]-second[0]
				ydiff = first[1]-second[1]
				dist = round(math.sqrt((xdiff**2 + ydiff**2)))
				pairwise[i][j] = dist

	runs = 1
	allCosts = []
	allTours = []
	# runs until time is up
	while (float(time.time() - start) <= float(maxTime)) and runs < 9:
		# get initial tour
		# doesn't have to be great, but helps computation if it's better than random
		startNode = newStartNode(nodes)
		cost  = 0
		initTour = []
		initTour.append(startNode)
		curr = startNode

		while len(initTour) < len(nodes):
			currDistances = pairwise[curr]
			closest = None
			closestCost = sys.maxsize
			for i in nodes:
				if i is not curr and i not in initTour:
					if currDistances[i] < closestCost:
						closestCost = currDistances[i]
						closest = i
			cost = cost + closestCost
			initTour.append(closest)
			curr = closest
		initTour.append(startNode)
		cost += pairwise[initTour[len(initTour)-1]][startNode]

		# find best tour by running twoOpt
		bestTour = twoOpt(pairwise, initTour)
		bestCost = findCost(pairwise, bestTour)
		# print result to file
		if runs == 1:
			outputFile = open(args[2], 'w')
		else:
			outputFile = open(args[2], 'a')
		outputFile.write('Run: {}\n'.format(runs))
		outputFile.write('{}\n'.format(bestCost))
		outputFile.write(' '.join(str(item) for item in bestTour))
		outputFile.write('\n')

		runs += 1
		allCosts.append(bestCost)
		allTours.append(bestTour)
	
	# calculating mean and standard deviation of runs
	print(allCosts)
	mean = sum(allCosts) / len(allCosts)
	sumDifferences = 0
	for cost in allCosts:
		sumDifferences += ((cost - mean) ** 2)
	
	standardDeviation = math.sqrt(sumDifferences / len(allCosts))

	outputFile.write('\nAverage: {}'.format(mean))
	outputFile.write('\nStandard Deviation: {}'.format(standardDeviation))

	# colors = ['b', 'g', 'r', 'm', 'y', 'c', 'k', 'w']
	# colorIndex = 0
	# for tour in allTours:
	# 	for i in range(len(tour) - 1):
	# 		x1, y1 = nodes[tour[i]]
	# 		x2, y2 = nodes[tour[i + 1]]
	# 		plt.plot([x1, x2], [y1, y2], colors[colorIndex])
	# 	if colorIndex > len(colors):
	# 		continue
	# 	colorIndex += 1
	# plt.show()

	outputFile.close()
	f.close()


# iteratively checks tour for optimality by swapping two edges 
# and seeing if the swap is cheaper than what the original had
def twoOpt(pairwise, tour):

	best = tour
	improved = True
	while improved:
		improved = False
		for i in range(1, len(best)-2):
			for j in range(i+1, len(best)):
				if j-i == 1:
					continue
				newTour = best[:]
				newTour[i:j] = best[j-1:i-1:-1]
				if findCost(pairwise, newTour) < findCost(pairwise, best):
					best = newTour
					improved = True
	
	return best


# gets cost of a particular tour by summing the costs between each node
def findCost(pairwise, tour):

	cost = 0
	for i in range(len(tour)-1):
		cost += pairwise[tour[i]][tour[i+1]]
	return cost

def newStartNode(nodes):
	return random.randint(1, len(nodes))



if __name__ == '__main__':
	main(sys.argv)