from queue import PriorityQueue
import copy
import os

def read_file(filename):
    """
    Return the list of maze configurations to use

    Parameters:
    filename: name of file with the mazes to be read in 
    """

    # Read in input file
    file_object = open(filename, "r")
    # Parse input into array
    sizes = file_object.read().splitlines()

    file_object.close()
    mazes = []
    maze = []
    for i in range(len(sizes)):
        # When we've reached a new grid
        if (len(sizes[i]) == 0):
            mazes.append(maze)
            maze = []
        # Construct the current row of the maze, and append it to the maze    
        else:
            row = []
            for j in range(len(sizes[i])):
                row.append(sizes[i][j])
            maze.append(row)

    # Append the final maze row
    mazes.append(maze)
    return mazes 

def search_maze(maze, target):
    """
    Function that finds the target node in the maze.

    Parameters:
    maze: 2d array that represents the current maze
    target: string indicating what target attribute you're searching for
            (i.e. "S" for start")
    """
    # Just search until it's found
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == target: 
                return (i,j)
    return "NO SOLUTION"

def show_board(maze):
    """
    Function used to display the current state of the board
    
    Parameters
    maze: 2d array that represents the current maze
    """
	
    for row in maze:
        for space in row:
            print("{} ".format(space), end="")
        print("")

def heuristic(curr_x, curr_y, goal_x, goal_y):
    """
    Function that calculates the heuristic value for each move
    This heuristic implementation utilizes the Euclidean distance.

    Parameters:
    curr_x, curr_y: The current location on the board of the move being considered
    goal_x, goal_y: The location of the goal node in our problem

    """
    # Return the euclidean distance between the points
    return pow(curr_x - goal_x, 2) + pow(curr_y - goal_y, 2)


def get_neighbours(current_x, current_y, max_x, max_y, maze, is_diag):
    """
    Function that returns the list of viable neighbours for a current position in the maze. Has the 
    option of additionally looking at the diagonal neighbours if specified

    Parameters:
    current_x, current_y: x and y coordinates of the current location in the maze
    max_x, max_y: maximum x and y coordinates of the maze to make sure we don't illegally index
    is_diag: (boolean) specify whether diagonal neighbours are looked for
    """
    
    neighbours = []
    # Look at left neighbours if we're not at the left wall
    if (current_x > 0):
        # Only append if it's not a barrier
        if maze[current_x - 1][current_y] != "X":
            neighbours.append((current_x - 1, current_y))
        
        if (is_diag):
            # Looking at top-left neighbour
            if (current_y > 0 and maze[current_x - 1][current_y - 1] != "X"):
                neighbours.append((current_x - 1, current_y - 1))
            # Looking at bottom-left neighbour    
            if (current_y < max_y - 1 and maze[current_x - 1][current_y + 1] != "X"):
                neighbours.append((current_x - 1, current_y + 1))

    # Look at right neighbours only if we're not at the right wall
    if (current_x < max_x - 1):
        # Only append if not a barrier
        if maze[current_x + 1][current_y] != "X":
            neighbours.append((current_x + 1, current_y))
        
        if is_diag:
            # Looking at top-right neighbour
            if (current_y > 0 and maze[current_x + 1][current_y - 1] != "X"):
                neighbours.append((current_x + 1, current_y - 1))
            # Looking at bottom-right neighbour    
            if (current_y < max_y - 1 and maze[current_x + 1][current_y + 1] != "X"):     
                neighbours.append((current_x + 1, current_y + 1))

    # Append above neighbour if not at the top of the maze, and if it's not a barrier 
    if (current_y > 0 and maze[current_x][current_y - 1] != "X"):
        neighbours.append((current_x, current_y - 1))
    # Append below neighbour if not at the bottom of the maze, and if it's not barrier    
    if (current_y < max_y - 1 and maze[current_x][current_y + 1] != "X"):
        neighbours.append((current_x, current_y + 1))
    
    return neighbours

def show_path(start_x, start_y, goal_x, goal_y, came_from, maze):
    """
    Function that updates maze with the path from start to goal.

    Parameters:
    start_x, start_y: x and y coordinates for the start position (used to stop search)
    goal_x, goal_y: x and y coordinates for the goal position (used to start search)
    came_from: dictionary containing where each node has been reached from through index
    maze: current maze
    """

    # Get who got to the goal node
    (current_x, current_y) = came_from[(goal_x, goal_y)]
    # Until we've reached the start
    while (current_x != start_x or current_y != start_y):
        # Update maze with current path
        maze[current_x][current_y] = "P"
        # Find which node was used to reach the current node
        (current_x, current_y) = came_from[(current_x, current_y)]
    
    # Return the reversed path list
    return maze


def write_maze(maze, outfile):
    """
    Function for writing the maze to the outfile

    Parameters:
    maze: maze being written to the file
    outfile: file object being written to

    """
    for row in maze:
        for entry in row:
            outfile.write("{}".format(entry))
        outfile.write("\n")

def output_maze(greedy_maze, a_star_maze, outfile):
    """
    Function to write solved mazes to file. Given a maze, the solution will be computed using
    both greedy and A* algorithm; each of those solutions will be written to file and specified
    with a given header denoting which algorithm was used.

    Parameters:
    greedy_maze: maze solution using the greedy algorithm
    a_star_maze: maze solution using the A* algorithm
    outfile: name of the file being written to

    """
    print("Writing solutions to file...")
    outfile = open(outfile, "a")
    
    outfile.write("Greedy\n")
    write_maze(greedy_maze, outfile)
    outfile.write("A*\n")
    write_maze(a_star_maze, outfile)
    # Append newline after writing in case of future mazes being written
    outfile.write("\n") 
    outfile.close()
    print("File written.\n")


def solve_maze(maze, is_greedy, is_diag):
    """
    Algorithm implementation for pathfinding. This code implements not only the greedy algorithm, but additionally
    the A* algorithm as most of their implementation details are the same.

    Parameters:
    maze: maze being solved
    is_greedy: flag indicating whether the solution will be found using greedy (True) or A* (False)
    is_diag: are diagonal moves allowed

    """
    # Get max sizes for future operations
    max_x = len(maze)
    max_y = len(maze[0])

    # Find the start position
    (start_x, start_y) = search_maze(maze, "S")
    (goal_x, goal_y) = search_maze(maze, "G")

    
    # Initialize the frontier priority queue
    frontier = PriorityQueue()

    # Initialize the "came_from" dict
    came_from = {}
    
    # Initialize the cost_so_far (only used in A*)
    cost_so_far = {}

    # Add the start node to the priority queue
    frontier.put((0, (start_x, start_y)))
    cost_so_far[(start_x, start_y)] = 0

    # Iterate until we've looked at all neighbours, or we've found a solution 
    is_solution = False
    while not(frontier.empty()):
        # Get the current best option from the priority queue
        (_, (current_x, current_y)) = frontier.get()
        # Check to see if we've reached goal
        if (goal_x == current_x) and (goal_y == current_y):
            is_solution = True 
            break
        
        # Get the legal neighbours for the current location
        neighbours = get_neighbours(current_x, current_y, max_x, max_y, maze, is_diag)

        # Add each unseen neighbour to the priority queue
        for (new_x, new_y) in neighbours:

            # Only use when we're running the A* algorithm
            if (not is_greedy):
                # find the cost of moving to the current node by adding 1 to the cost so far
                new_cost = cost_so_far[(current_x, current_y)] + 1

                # If we haven't seen the node yet, or the cost to reach the node is now cheaper
                if ((new_x, new_y) not in cost_so_far) or (new_cost < cost_so_far[(new_x, new_y)]):

                    # Update cost so far with new cost
                    cost_so_far[(new_x, new_y)] = new_cost
                    # Put node in priority queue with updated cost
                    priority = new_cost + heuristic(new_x, new_y, goal_x, goal_y)
                    # Add to queue for selection
                    frontier.put((priority, (new_x, new_y)))
                    came_from[(new_x,new_y)] = (current_x, current_y)
            # When greedy algorithm being run        
            else:
                if (new_x, new_y) not in came_from:
                    cost = heuristic(new_x, new_y, goal_x, goal_y)
                    frontier.put((cost, (new_x, new_y)))
                    came_from[(new_x, new_y)] = (current_x, current_y)

    if is_solution:
        print("Solved!\n")
        maze = show_path(start_x, start_y, goal_x, goal_y, came_from, maze)
    else:
        print("No solution :(")
    
    return maze

def remove_output_files():
    """
    Function for removing the output files before use. Because the files are being appended to,
    we want to start with a fresh output file. Exceptions thrown if files do not exist,
    """
    try:
        os.remove("pathfinding_a_out.txt")
    except:
        pass
    try:
        os.remove("pathfinding_b_out.txt")
    except:
        pass

def maze_solve_iter(mazes, outfile, is_diag):
    """
    Function that iteratively solves mazes from an input file, as input files can contain several
    mazes. Produces solutions using both greedy algorithm and A* algorithm

    Parameters:
    mazes: list of mazes to be solved
    outfile: output file to write maze solutions in
    is_diag: are we allowed to make diagonal moves
    """
    for maze in mazes:
        print("Displaying initial maze...\n")
        show_board(maze)
        print("\nSolving maze using Greedy...")
        greedy  = solve_maze(copy.deepcopy(maze), is_greedy=True, is_diag=is_diag)
        print("Solving maze using A*...")
        a_star = solve_maze(copy.deepcopy(maze), is_greedy=False, is_diag=is_diag)
        output_maze(greedy, a_star, outfile)

def main():
    # Remove the output files so they can be properly appended to
    remove_output_files()
    
    # Read in files that contain mazes
    mazes_a = read_file("pathfinding_a.txt")
    mazes_b = read_file("pathfinding_b.txt")
    
    # Solve the mazes, both with diagonal capabilities and without
    maze_solve_iter(mazes_a, "pathfinding_a_out.txt", is_diag=False)
    maze_solve_iter(mazes_b, "pathfinding_b_out.txt", is_diag=True)

# Run program.
if __name__ == "__main__":
    main()
