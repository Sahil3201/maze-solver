import maze_generator
import argparse
import matplotlib.pyplot as plt
import time

class MdpCell(maze_generator.Cell):
    def __init__(self,  x, y, state='w', visited=False):
        super().__init__(x, y, state, visited)
        self.policy = 'U'
        self.value = 0
        self.new_value = -1
        self.reward = -0.1

    def __str__(self):
        # return str(self.value)[:5] if self._state!='w' else '    w'
        return self.policy if self._state != 'w' else ' '


def get_neighbours(maze, cell, w, h):
    ret = {}
    if (cell.x != 0):
        ret['L'] = maze[cell.y][cell.x-1]
    else:
        ret['L'] = maze[cell.y][cell.x]
    if (cell.x != w-1):
        ret['R'] = maze[cell.y][cell.x+1]
    else:
        ret['R'] = maze[cell.y][cell.x]
    if (cell.y != 0):
        ret['U'] = maze[cell.y-1][cell.x]
    else:
        ret['U'] = maze[cell.y][cell.x]
    if (cell.y != h-1):
        ret['D'] = maze[cell.y+1][cell.x]
    else:
        ret['D'] = maze[cell.y][cell.x]
    ret['N'] = maze[cell.y][cell.x]
    # print(cell.get_state())
    # if (cell.x==5 and cell.y==5):
    #     for i in ret.keys():
    #         print(ret[i])
    return ret


class MdpMaze(maze_generator.Maze):
    def __init__(self, w, h):
        super().__init__(w, h, CellDef=MdpCell)
        self.maze = maze_generator.prims_algo(w, h, self)

    def complete_iteration(self):
        for i in maze:
            for cell in i:
                cell.value = cell.new_value

    def __str__(self):
        ret = ''
        for i in self.rows:
            ret += str(i) + '\n'
        return ret

    def visualize_maze_matplotlib(self, optimal_path=None):
        arrow_symbols = {'U': '↑', 'D': '↓', 'R': '→', 'L': '←'}

        for row in self.maze.rows:
            for cell in row:
                if cell.get_state() == 'w':
                    plt.fill_between([cell.x, cell.x + 1],
                                     cell.y, cell.y + 1, color='black')
                else:
                    plt.fill_between([cell.x, cell.x + 0.5], cell.y,
                                     cell.y + 1, color='white', edgecolor='black')
                    plt.fill_between([cell.x + 0.5, cell.x + 1], cell.y,
                                     cell.y + 1, color='white', edgecolor='black')

                    value_text = str(round(cell.value, 5))
                    policy_text = arrow_symbols.get(
                        cell.policy, str(cell.policy))

                    plt.text(cell.x + 0.66, cell.y + 0.5, value_text,
                             fontsize=4, ha='center', va='center', color='black')

                    if optimal_path and cell in optimal_path:
                        plt.fill_between([cell.x, cell.x + 1],
                                         cell.y, cell.y + 1, color='yellow')

        plt.title('MDP Policy Iteration Maze Visualization')
        plt.xlabel('X-axis')
        plt.gca().invert_yaxis()
        plt.ylabel('Y-axis')
        plt.show()
        plt.get_current_fig_manager().full_screen_toggle()


def policy_iteration(maze: MdpMaze, w, h, start, end, gamma=0.9, error=1e-15):
    is_policy_changed = True

    # policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['U', 'D', 'L', 'R']

    iterations = 0

    # Policy iteration
    while is_policy_changed:
        is_policy_changed = False
        is_converging = True
        while is_converging:
            is_converging = False
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
                            is_converging = True
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
                        is_policy_changed = True
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
    return maze, optimal_path


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
    maze, optimal_path = policy_iteration(
        maze, args.width, args.height, start, end)
    print("time taken for Policy Iteration:", time.time()-start_time)

    # Print maze and visualize with optimal path
    print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    if (args.visualize == 'Y'):
        maze.visualize_maze_matplotlib(optimal_path)
