import sys
import itertools
import random
# cost is 29000 for sample input

initTour = []

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
				dist = round((xdiff**2 + ydiff**2)**(0.5))
				pairwise[i][j] = dist

	# get initial tour
	# doesn't have to be great, but helps computation if it's better than random
	startNode = random.randint(1,len(nodes))
	cost  = 0
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
	outputFile = open(args[2], 'w')
	outputFile.write(str(bestCost) + "\n")
	outputFile.write(" ".join(str(item) for item in bestTour))
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
	for i in range(len(tour)-2):
		cost += pairwise[tour[i]][tour[i+1]]
	return cost



if __name__ == '__main__':
	main(sys.argv)