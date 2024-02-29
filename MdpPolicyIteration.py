import maze_generator
import argparse
# import matplotlib.pyplot as plt


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


def policy_iteration(maze: MdpMaze, w, h, start, end, gamma=0.9, error=1e-9):
    is_policy_changed = True

    # policy = [['up' for i in range(len(grid[0]))] for j in range(len(grid))]
    actions = ['U', 'D', 'L', 'R']

    iterations = 0

    # Policy iteration
    while is_policy_changed:
        is_policy_changed = False
        # Policy evaluation
        # Transition probabilities not shown due to deterministic setting
        is_value_changed = True
        while is_value_changed:
            is_value_changed = False
            # Run value iteration for each state
            for row in maze:
                for cell in row:
                    if cell.get_state() == 'w':
                        cell.policy = 'w'
                    else:
                        neighbours = get_neighbours(maze, cell, w, h)
                        neighbour = neighbours[cell.policy]
                        v = cell.reward + gamma * neighbour.value
                        # Compare to previous iteration
                        if v != cell.value:
                            is_value_changed = True
                            cell.value = v

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

    return maze


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a maze and use Policy Iteration to create a policy to solve it.')
    parser.add_argument('--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('--width', type=int, default=60,
                        help='Width of the maze')
    args = parser.parse_args()

    maze = MdpMaze(w=args.width, h=args.height)
    start, end = maze.set_start_end_points()
    start.reward = -100
    end.reward = 100
    end.set_state('e')
    # maze = value_iteration(maze, args.width, args.height)
    # print(maze)
    # print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    # maze.visualize_maze_matplotlib()
    #     # Run value iteration
    maze = policy_iteration(maze, args.width, args.height, start, end)

    # Print maze and visualize with optimal path
    print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    # maze.visualize_maze_matplotlib(optimal_path)
    print(maze)


# if __name__ == '__main__':
#     maze

#     test_maze = AldousBroder(3, 3).generate()
#     test_mdp = maze_to_mdp(test_maze)
#     test_policy = policy_iteration(test_mdp, .9)
#     test_policy_str = prettify_policy(test_policy)

#     print(test_maze)
#     print(test_policy_str)
