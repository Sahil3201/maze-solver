import matplotlib.pyplot as plt
import maze_generator


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
        for i in self.maze:
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
                    plt.fill_between([cell.x, cell.x + 1],
                                     cell.y, cell.y + 1, color='black')
                else:
                    plt.fill_between([cell.x, cell.x + 1], cell.y,
                                     cell.y + 1, color='white', edgecolor='black')

                    # value_text = str(round(cell.value, 3))
                    policy_text = arrow_symbols.get(
                        cell.policy, str(cell.policy))

                    plt.text(cell.x + 0.5, cell.y + 0.5, policy_text,
                             fontsize=8, ha='center', va='center', color='black')

                    if optimal_path and cell in optimal_path:
                        plt.fill_between([cell.x, cell.x + 1],
                                         cell.y, cell.y + 1, color='yellow')

        plt.title('MDP Maze Visualization')
        plt.xlabel('X-axis')
        plt.gca().invert_yaxis()
        plt.ylabel('Y-axis')
        plt.show()
