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
        return self.policy if self._state!='w' else ' '

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

    # def visualize_maze(self, path=None):
    #     cell_size = 10
    #     pygame.init()
    #     size = (self.w*cell_size, self.h*cell_size)

    #     screen = pygame.display.set_mode(size)
    #     pygame.display.set_caption("MDP Value Iteration Maze Visualization")

    #     colors = {'p': (255, 255, 255), 'w': (0, 0, 0),
    #               'e': (255, 0, 0), 's': (13, 158, 8), 'r': (13, 158, 8)}

    #     while True:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #                 return
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.K_ESCAPE:
    #                     pygame.quit()
    #                     return

    #         for i, row in enumerate(self):
    #             for j, cell in enumerate(row):
    #                 color = colors[cell.get_state()]
    #                 if path and cell in path:
    #                     color = colors['r']
    #                 pygame.draw.rect(
    #                     screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    #         pygame.display.flip()

    # def visualize_maze_matplotlib(self):
    #     for row in self.maze.rows:
    #         for cell in row:
    #             if cell.get_state() == 'w':
    #                 plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='black')
    #             else:
    #                 plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='white', edgecolor='black')
    #                 plt.text(cell.x + 0.5, cell.y + 0.5, round(cell.value, 3), color='black', ha='center', va='center')

    #     plt.title('Maze Visualization')
    #     plt.xlabel('X-axis')
    #     plt.ylabel('Y-axis')
    #     plt.gca().invert_yaxis()
        # plt.show()

    # def visualize_maze_matplotlib(self):
    #     arrow_symbols = {'U': '↑', 'D': '↓', 'R': '→', 'L': '←'}

    #     for row in self.maze.rows:
    #         for cell in row:
    #             if cell.get_state() == 'w':
    #                 plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='black')
    #             else:
    #                 plt.fill_between([cell.x, cell.x + 0.5], cell.y, cell.y + 1, color='white', edgecolor='black')
    #                 plt.fill_between([cell.x + 0.5, cell.x + 1], cell.y, cell.y + 1, color='white', edgecolor='black')

    #                 value_text = str(round(cell.value, 3))
    #                 policy_text = arrow_symbols.get(cell.policy, str(cell.policy))

    #                 # plt.text(cell.x + 0.33, cell.y + 0.5, value_text, fontsize=8, ha='center', va='center', color='black')
    #                 plt.text(cell.x + 0.66, cell.y + 0.5, policy_text, fontsize=8, ha='center', va='center', color='black')

    #     plt.title('MDP Value Iteration Maze Visualization')
    #     plt.xlabel('X-axis')
    #     plt.gca().invert_yaxis()
    #     plt.ylabel('Y-axis')
    #     plt.show()

    def visualize_maze_matplotlib(self, optimal_path=None):
        arrow_symbols = {'U': '↑', 'D': '↓', 'R': '→', 'L': '←'}

        for row in self.maze.rows:
            for cell in row:
                if cell.get_state() == 'w':
                    plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='black')
                else:
                    plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='white', edgecolor='black')
                    # plt.fill_between([cell.x + 0.5, cell.x + 1], cell.y, cell.y + 1, color='white', edgecolor='black')

                    value_text = str(round(cell.value, 3))
                    policy_text = arrow_symbols.get(cell.policy, str(cell.policy))

                    # plt.text(cell.x + 0.33, cell.y + 0.5, value_text, fontsize=5, ha='center', va='center', color='black')
                    plt.text(cell.x + 0.5, cell.y + 0.5, policy_text, fontsize=8, ha='center', va='center', color='black')

                    if optimal_path and cell in optimal_path:
                        plt.fill_between([cell.x, cell.x + 1], cell.y, cell.y + 1, color='yellow')

        plt.title('MDP Value Iteration Maze Visualization')
        plt.xlabel('X-axis')
        plt.gca().invert_yaxis()
        plt.ylabel('Y-axis')
        plt.show()



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


# MDP value iteration algorithm
def value_iteration(maze: MdpMaze, w, h, start, end, gamma=0.9, error=1e-15, living_reward=-0.1, noise=0.2):
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
    return maze, optimal_path


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
    maze, optimal_path = value_iteration(maze, args.width, args.height, start=start, end=end)
    print("time taken for Value Iteration:", time.time()-start_time)
    
    print(f"({start.x}, {start.y})", f"({end.x}, {end.y})")
    if(args.visualize=='Y'):
        maze.visualize_maze_matplotlib(optimal_path)
