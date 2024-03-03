import maze_generator
import argparse
import matplotlib.pyplot as plt
import time
from mdp_maze_generator import *

def policy_iteration(maze: MdpMaze, w, h, start, end, gamma=0.9, error=1e-15):
    policy_changing = True

    # policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['U', 'D', 'L', 'R']

    iterations = 0

    # Policy iteration
    while policy_changing:
        policy_changing = False
        is_value_converging = True
        while is_value_converging:
            is_value_converging = False
            # Running value iteration for each state
            for row in maze:
                for cell in row:
                    if cell.get_state() == 'w':
                        cell.policy = 'w'
                    else:
                        neighbours = get_neighbours(maze, cell, w, h)
                        neighbour = neighbours[cell.policy]
                        v = cell.reward + gamma * neighbour.value
                        # Compare to previous iteration
                        if error < abs(v-cell.value):
                            is_value_converging = True
                            cell.new_value = v
            maze.complete_iteration()

        # Policy improvement and policy evaluation
        # Once values have converged for the policy, update policy with greedy actions
        for row in maze:
            for cell in row:
                if cell.get_state() != 'w':
                    # Dictionary comprehension to get value associated with each action
                    neighbours = get_neighbours(maze, cell, w, h)
                    action_values = {a: neighbours[a].value for a in actions}
                    best_action = max(action_values, key=action_values.get)
                    # Compare to previous policy
                    if best_action != cell.policy:
                        policy_changing = True
                        cell.policy = best_action
        iterations += 1

    print(f"Convergence complete in {iterations} iterations")
    optimal_path = []
    current_cell = start
    while current_cell.get_state() != 'e':
        optimal_path.append(current_cell)
        action = current_cell.policy
        if (action == 'w'):
            print("Something went wrong!")
            break
        current_cell = get_neighbours(maze, current_cell, w, h)[action]
    if current_cell.get_state() == 'e':
        optimal_path.append(current_cell)
    return maze, optimal_path, iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a maze and use Policy Iteration to create a policy to solve it.')
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
    maze, optimal_path, iterations = policy_iteration(
        maze, args.width, args.height, start, end)
    print("time taken for Policy Iteration: {} seconds".format(round(time.time()-start_time, 3)))

    # Print maze and visualize with optimal path
    print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    if (args.visualize == 'Y'):
        maze.visualize_maze_matplotlib(optimal_path)
