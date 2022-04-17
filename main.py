# Drew Turner and Kevin Pfeil
# Run using Python3

import sys
from queue import PriorityQueue

class State(object):
	def __init__(self, chickensRight, wolvesRight, chickensLeft, wolvesLeft, boat, parent, depth):
		self.chickensRight = chickensRight
		self.wolvesRight = wolvesRight
		self.chickensLeft = chickensLeft
		self.wolvesLeft = wolvesLeft
		self.parent = parent
		self.boat = boat
		self.depth = depth

	def __repr__(self):
		return "Left: " + str(self.chickensLeft) + " " + str(self.wolvesLeft) + " Right: " + str(self.chickensRight) + " " + str(self.wolvesRight) + " " + str(self.boat)

	def __eq__(self, other):
		if self.chickensRight == other.chickensRight \
		and self.chickensLeft == other.chickensLeft \
		and self.wolvesRight == other.wolvesRight \
		and self.wolvesLeft == other.wolvesLeft \
		and self.boat == other.boat:
			return True
		else:
			return False

	def __lt__(self, other):
		if self.chickensLeft < other.chickensLeft and self.wolvesLeft < other.wolvesLeft:
			return True
		else:
			return False
    
	def __gt__(self, other):
		if self.chickensLeft > other.chickensLeft and self.wolvesLeft > other.wolvesLeft:
			return True
		else:
			return False

	def isValidState(self):
		# ensuring that there are more chickens than wolves on the right
		if (self.chickensRight > 0) and (self.chickensRight < self.wolvesRight):
			return False
		# same as above but on the left
		elif (self.chickensLeft > 0) and (self.chickensLeft < self.wolvesLeft):
			return False
		# cannot have negative values, this comes into play when looking at all
        # of the possible moves
		elif self.chickensLeft < 0 or self.wolvesLeft < 0 or self.chickensRight < 0 or self.wolvesRight < 0:
			return False
		else:
			return True

def search(current):
	valid_moves = []
    # when we create the children, increment the depth by one so we can use iddfs
	if (current.boat == 'right'):
		# move one chicken
		state = State(current.chickensRight - 1, current.wolvesRight, current.chickensLeft + 1, current.wolvesLeft, 'left', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move two chickens
		state = State(current.chickensRight - 2, current.wolvesRight, current.chickensLeft + 2, current.wolvesLeft, 'left', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move one wolf
		state = State(current.chickensRight, current.wolvesRight - 1, current.chickensLeft, current.wolvesLeft + 1, 'left', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move one chicken and one wolf
		state = State(current.chickensRight - 1, current.wolvesRight - 1, current.chickensLeft + 1, current.wolvesLeft + 1, 'left', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move two wolves
		state = State(current.chickensRight, current.wolvesRight - 2, current.chickensLeft, current.wolvesLeft + 2, 'left', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
	elif (current.boat == 'left'):
		# move one chicken
		state = State(current.chickensRight + 1, current.wolvesRight, current.chickensLeft - 1, current.wolvesLeft, 'right', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move two chickens
		state = State(current.chickensRight + 2, current.wolvesRight, current.chickensLeft - 2, current.wolvesLeft, 'right', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move one wolf
		state = State(current.chickensRight, current.wolvesRight + 1, current.chickensLeft, current.wolvesLeft - 1, 'right', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move one wolf and one chicken
		state = State(current.chickensRight + 1, current.wolvesRight + 1, current.chickensLeft - 1, current.wolvesLeft - 1, 'right', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None
		# move two wolves
		state = State(current.chickensRight, current.wolvesRight + 2, current.chickensLeft, current.wolvesLeft - 2, 'right', current, current.depth + 1)
		valid_moves.append(state) if state.isValidState() else None

	return valid_moves

def path(state, initial):
    # make an array to store solution
    path = []
    # append goal state
    path.append(state)
    # while the current state is not the initial state
    while state.parent != initial:
        # go back up the graph, adding parent states to the path
        state = state.parent
        path.insert(0, state)
    # insert the initial state
    path.insert(0, initial)
    return path

def breadth_first_search(init_state, goal_state):
    # create array to keep track of the visited
	visited = []
	# create frontier
	frontier = []
    # push initial state onto queue
	frontier.append(init_state)
	# while queue is not empty
	while(len(frontier) > 0):
        # pop state off queue
		state = frontier.pop(0)
        # if state is goal state, return path
		if (state == goal_state):
			sol = path(state, init_state)
			return (sol, len(visited))
		# if we have not been to this state before
		if state not in visited:
			# visit it
			visited.append(state)
			# add all valid children to the queue
			valid_moves = search(state)
			for state in valid_moves:
				frontier.append(state)
	# if frontier is empty, return None because no solution was found
	return None

def depth_first_search(init_state, goal_state):
    # create array to keep track of the visited
	visited = []
	# create frontier
	frontier = []
	# push first node into queue
	frontier.append(init_state)
	# while frontier is not empty
	while(len(frontier) > 0):
		# pop curr_state off frontier, depth first
		curr_state = frontier.pop()
		# if curr_state is goal state, return path
		if (curr_state == goal_state):
			# solution found
			sol = path(curr_state, init_state)
			return (sol, len(visited))
		# if curr_state is valid
		if (curr_state not in visited):
			# add curr_state to visited
			visited.append(curr_state)
			# add all valid children to the queue
			valid_children = search(curr_state)
			for state in valid_children:
				frontier.append(state)
	# if frontier is empty, return None because no solution was found
	return None

def iterative_deepening(init_state, goal_state):
	visited = []
	# create frontier
	frontier = []
	depth_limit = sys.maxsize
	limit = 0
	num_visited = 0

    # run a for loop that keeps track of how many levels we can go down
	for _ in range(depth_limit):
		# push initial state onto frontier
		frontier.append(init_state)
		while(len(frontier) > 0):
			# pop curr_state off frontier
			curr_state = frontier.pop()
			# if curr_state is goal curr_state, return path
			if (curr_state == goal_state):
				sol = path(curr_state, init_state)
				return (sol, num_visited)
			# if curr_state is not visited
			if (curr_state not in visited):
				# add curr_state to visited
				visited.append(curr_state)

				# if the current depth is than this iteration's limit
				if (curr_state.depth < limit):
					# we want to search
					valid_moves = search(curr_state)
					# add all valid children to the frontier
					for state in valid_moves:
						frontier.append(state)
				else:
					visited = []

		# done with this iteration, increase limit, update visited count, reset visited
		num_visited += len(visited)
        # need to reset this array since this search is iterative
		visited = []
		frontier = []
		limit += 1

def heuristic(curr_state, goal_state):
	# smaller number means that we are closer to the solution
	return ((goal_state.chickensLeft - curr_state.chickensLeft) + (goal_state.wolvesLeft - curr_state.wolvesLeft))

def astar(init_state, goal_state):
	visited = []
	# create frontier using priority queue to keep track of heuristic score
	frontier = PriorityQueue()
	# get initial score for init_state and push onto frontier
	frontier.put((heuristic(init_state, goal_state), init_state))

	while(frontier):
        # get curr state from the priority queue
		curr_state = frontier.get()[1]
        # if curr_state is goal curr_state, return path
		if (curr_state == goal_state):
			# solution found
			sol = path(curr_state, init_state)
			return (sol, len(visited))

		if(curr_state not in visited):
			# add curr_state to visited
			visited.append(curr_state)
			valid_move = search(curr_state)
			for state in valid_move:
				# put score and state onto frontier
				frontier.put((heuristic(state, goal_state), state))

def init_state(file):
	left = []
	right = []
	first = True

	file = open(file, 'r')

    # loop through each line in file
	for line in file:
        # split line on comma
		line = line.split(',')
		# if first line, set left to line, grabbing the elements, converting to int, and appending to left
		if (first):
			left = list(map(int,line))
			first = False
		else:
			# else set right to line, grabbing the elements, converting to int, and appending to right
			right = list(map(int,line))

    # close file
	file.close()

	# look at side boat is on and create a game state
	if (right[2] == 1):
		state = State(right[0], right[1], left[0], left[1], 'right', None, 0)
	else:
		state = State(right[0], right[1], left[0], left[1], 'left', None, 0)
	return state

def main(args):
	if len(args) != 5:
		print("Usage: python3 main.py <initial state file> <goal state file> <mode> <output file>")
		sys.exit(1)

	start_state = args[1]
	goal_state = args[2]
	mode = args[3]
	output = open(args[4], 'w')

	initial = init_state(start_state)
	goal = init_state(goal_state)

	if (mode == 'bfs'):
		sol, num_visited = breadth_first_search(initial, goal)
		print("BFS:")
	elif (mode == 'dfs'):
		sol, num_visited = depth_first_search(initial, goal)
		print("DFS:")
	elif (mode == 'astar'):
		sol, num_visited = astar(initial, goal)
		print("A*:")
	elif (mode == 'iddfs'):
		sol, num_visited = iterative_deepening(initial, goal)
		print("IDDFS:")
	else:
		print("Invalid mode")
		sys.exit(1)
	if sol != None:
		print("Nodes visited: ", num_visited)
		print("Solution:")
		# print the solution path
		for state in sol:
			print(state)
			output.write(str(state) + '\n')
		print("Solution length: ", len(sol))
	else:
		print("No solution was found")

if __name__ == "__main__":
	starting_state = sys.argv[1]
	goal_state = sys.argv[2]
	initial = init_state(starting_state)
	goal = init_state(goal_state)
	main(sys.argv)