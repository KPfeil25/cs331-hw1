import sys
from queue import PriorityQueue

class State():
    def __init__(self, chickensLeft, wolvesLeft, chickensRight, wolvesRight, boat, parent, depth) -> None:
        self.chickensLeft: int = chickensLeft
        self.wolvesLeft: int = wolvesLeft
        self.chickensRight: int = chickensRight
        self.wolvesRight: int = wolvesRight
        self.boat = boat
        self.parent = parent
        self.depth: int = depth

    # def __eq__(self, other) -> bool:
    #     if (self.chickensRight == other.chickensRight and
    #         self.wolvesRight == other.wolvesRight and
    #         self.chickensLeft == other.chickensLeft and
    #         self.wolvesLeft == other.wolvesLeft and
    #         self.boat == other.boat and
    #             self.parent == other.parent):
    #         return True
    #     else:
    #         return False

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__
    
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

    def __repr__(self):
        return "left bank: %s %s right bank: %s %s boat: %s" % (self.chickensLeft, self.wolvesLeft, self.chickensRight, self.wolvesRight, self.boat)

    def isValidState(self) -> bool:
        # check left side for chickens and wolves
        if (self.chickensLeft) > 0 and (self.chickensLeft < self.wolvesLeft):
            return False
        # check right side for chickens and wolves
        if (self.chickensRight) > 0 and (self.chickensRight < self.wolvesRight):
            return False
        # make sure that moves that subtract chickens or wolves dont go below zero
        if (self.chickensLeft < 0 or self.chickensRight < 0 or self.wolvesLeft < 0 or self.wolvesRight < 0):
            return False
        return True


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
            left = list(map(int, line))
            first = False
        else:
            # else set right to line, grabbing the elements, converting to int, and appending to right
            right = list(map(int, line))

    # close file
    file.close()

    # create initial state
    # if boat is on the left shore
    if (left[2] == 1):
        state = State(left[0], left[1], right[0], right[1], "left", None, None)
        print(state)
    # else boat is on the right shore
    else:
        state = State(left[0], left[1], right[0], right[1], 'right', None, None)
        print(state)

    return state

def heuristic(curr_state: State, goal_state: State):
    # smaller number means that we are closer to the solution
    return (goal_state.wolvesLeft - curr_state.wolvesLeft) + (goal_state.chickensLeft - curr_state.chickensLeft)

def breadth_first_search(init_state, goal_state):
    visited = []
    # create frontier
    frontier = []
    # push initial state onto queue
    frontier.append(init_state)
    # while queue is not empty
    while (len(frontier) > 0):
        # pop state off queue
        state = frontier.pop(0)
        # if state is goal state, return path
        if (state == goal_state):
            return state
        # if we have not been to this state before
        if state not in visited:
            visited.append(state)
            valid_moves = search(state)
            for move in valid_moves:
                frontier.append(move)

def depth_first_search(init_state, goal_state):
  visited = {}
  # create frontier
  frontier = []
  # push initial state onto frontier
  frontier.append(init_state)
  # while frontier is not empty
  while (len(frontier) > 0):
      # pop curr_state off frontier
      curr_state = frontier.pop()
      # if curr_state is goal curr_state, return path
      if (curr_state == goal_state):
        # solution found
          return curr_state
      # if curr_state is valid
      if (curr_state not in visited):
          # add curr_state to visited
          visited.add(curr_state)
          # push children onto frontier
          frontier.add(search(curr_state))
  # if frontier is empty, return False because no solution was found
  return False

def iterative_deepening_search(init_state, goal_state):
  depth_limit = 500
  visited = {}
  # create frontier
  frontier = []
  # push initial state onto frontier
  frontier.append(init_state)
  # while frontier is not empty
  for i in range(depth_limit):
    while (len(frontier) > 0):
      # pop curr_state off frontier
      curr_state = frontier.pop()
      # if curr_state is goal curr_state, return path
      if (curr_state == goal_state):
        # solution found
        return curr_state
      # if curr_state is valid
      if (curr_state not in visited):
          # add curr_state to visited
          visited.add(curr_state)
          #check depth limit HERE -> NEED TO ADD LIMIT TO STATE
          if(curr_state.depth < depth_limit):
                frontier.add(search(curr_state))

  # if frontier is empty, return False because no solution was found
  return False


def astar(init_state, goal_state):
    visited = {}
    frontier = PriorityQueue()
    frontier.put(heuristic(init_state, goal_state), init_state)
    while(len(frontier) > 0):
        #get curr state from the priority queue
        curr_state = frontier.get()[1]
        # if curr_state is goal curr_state, return path
        if (curr_state == goal_state):
            # solution found
            return curr_state
        if (curr_state not in visited):
            # add curr_state to visited
            visited.add(curr_state)
            frontier.add(search(curr_state))
    # if frontier is empty, return False because no solution was found
    return False


def search(state):
    valid_moves = []
    if (state.boat == "left"):
        # 1 wolf moves
        move = State(state, state.chickensLeft, state.wolvesLeft - 1, state.chickensRight, state.wolvesRight + 1, 'right', state)
        valid_moves.append(move) if move.isValidState() else None
        # 2 wolves move
        move = State(state, state.chickensLeft, state.wolvesLeft - 2, state.chickensRight, state.wolvesRight + 2, 'right', state)
        valid_moves.append(move) if move.isValidState() else None
        # 1 chicken and 1 wolf move
        move = State(state, state.chickensLeft - 1, state.wolvesLeft - 1, state.chickensRight + 1, state.wolvesRight + 1, 'right', state)
        valid_moves.append(move) if move.isValidState() else None
        # 2 chickens
        move = State(state, state.chickensLeft - 2, state.wolvesLeft, state.chickensRight + 2, state.wolvesRight, 'right', state)
        valid_moves.append(move) if move.isValidState() else None
        # 1 chicken
        move = State(state, state.chickensLeft - 1, state.wolvesLeft, state.chickensRight + 1, state.wolvesRight, 'right', state)
        valid_moves.append(move) if move.isValidState() else None
    else:
        # 1 wolf moves
        move = State(state, state.chickensLeft, state.wolvesLeft + 1, state.chickensRight, state.wolvesRight - 1, 'left', state)
        valid_moves.append(move) if move.isValidState() else None
        # 2 wolves move
        move = State(state, state.chickensLeft, state.wolvesLeft + 2, state.chickensRight, state.wolvesRight - 2, 'left', state)
        valid_moves.append(move) if move.isValidState() else None
        # 1 chicken and 1 wolf move
        move = State(state, state.chickensLeft + 1, state.wolvesLeft + 1, state.chickensRight - 1, state.wolvesRight - 1, 'left', state)
        valid_moves.append(move) if move.isValidState() else None
        # 2 chickens
        move = State(state, state.chickensLeft + 2, state.wolvesLeft, state.chickensRight - 2, state.wolvesRight, 'left', state)
        valid_moves.append(move) if move.isValidState() else None
        # 1 chicken
        move = State(state, state.chickensLeft + 1, state.wolvesLeft, state.chickensRight - 1, state.wolvesRight, 'left', state)
        valid_moves.append(move) if move.isValidState() else None
        
    return valid_moves

#function that returns the path from the initial state to the goal state
def path(state):
    #create a list to store the path
    path = []
    #while the state is not the initial state
    while state.parent != None:
      #append the state to the path
        path.append(state)
        #set the state to the parent of the state
        state = state.parent
    return path


def main(args):
    if len(args) != 5:
        print("Usage: python3 main.py <initial state file> <goal state file> <mode> <output file>")
        sys.exit(1)

    start_state = sys.argv[1]
    goal_state = sys.argv[2]
    mode = sys.argv[3]

    starting_state = init_state(start_state)
    goal_state = init_state(goal_state)

    if mode == 'bfs':
        solution = path(breadth_first_search(starting_state, goal_state))
        
    print(solution)

if __name__ == "__main__":
    start_state = sys.argv[1]
    goal_state = sys.argv[2]
    mode = sys.argv[3]
    output = sys.argv[4]
    main(sys.argv)
