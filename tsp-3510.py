import sys
# cost is 29000 for sample input
def main(args):
	output_filename = args[2]
	maxTime = args[3]
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
	pairwise = [[0 for i in range(len(nodes))] for j in range(len(nodes))]
	# initialize matrix to track min distances to each node
	min_distances = [[sys.maxsize for i in range(len(nodes))] for j in range(len(nodes))]
	# go through all nodes to find distances
	for i in range(len(nodes)):
		first = nodes[i+1]
		for j in range(len(nodes)):
			second = nodes[j+1]
			if i is not j:
				# get euclidean distance
				xdiff = first[0]-second[0]
				ydiff = first[1]-second[1]
				dist = round((xdiff**2 + ydiff**2)**(0.5))
				pairwise[i][j] = dist
			else:
				# distance from v to v is always 0
				min_distances[i][j] = 0

	print(pairwise)




if __name__ == '__main__':
	main(sys.argv)