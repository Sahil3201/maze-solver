import maze_generator
import argparse
import matplotlib.pyplot as plt
import time
from mdp_maze_generator import *

# MDP value iteration algorithm
def value_iteration(maze: MdpMaze, w, h, start, end, gamma=0.9, error=1e-15):
    iterations = 0
    is_converging = True
    # iterate values until convergence
    while is_converging:
        is_converging = False
        for row in maze:
            for cell in row:
                if cell.get_state() != 'w':
                    action_values = {}
                    q = []
                    neighbours = get_neighbours(maze, cell, w, h)
                    for action in neighbours:
                        # Get coordinates of neighboring cell
                        neighbour = neighbours[action]
                        action_values[action] = cell.reward + gamma * neighbour.value
                        q.append(cell.reward + gamma *neighbour.value)
                    v = max(q)

                    if error < abs(v-cell.value):
                        cell.policy = max(action_values, key=action_values.get)
                        cell.new_value = v
                        is_converging = True

            # print(maze)
        maze.complete_iteration()
        iterations += 1
    
    print(f"Convergence complete in {iterations} iterations")
    optimal_path = []
    current_cell = start
    while current_cell.get_state() != 'e':
        optimal_path.append(current_cell)
        action = current_cell.policy
        current_cell = get_neighbours(maze, current_cell, w, h)[action]
    if current_cell.get_state() == 'e':
        optimal_path.append(current_cell)
    return maze, optimal_path, iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a maze and use Value Iteration to create a policy to solve it.')
    parser.add_argument('-l', '--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('-w', '--width', type=int, default=60,
                        help='Width of the maze')
    parser.add_argument('-v','--visualize', type=str, default='N',
                        help='Visualize the maze? [Y/N]')
    args = parser.parse_args()

    maze = MdpMaze(w=args.width, h=args.height)
    start, end = maze.set_start_end_points()
    start.reward = -100
    end.reward = 100
    end.set_state('e')

    start_time = time.time()
    maze, optimal_path, iterations = value_iteration(maze, args.width, args.height, start=start, end=end)
    print("time taken for Value Iteration: {} seconds".format(round(time.time()-start_time, 3)))
    
    print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    if(args.visualize=='Y'):
        maze.visualize_maze_matplotlib(optimal_path)
