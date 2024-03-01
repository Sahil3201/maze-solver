import maze_generator
import argparse
from queue import PriorityQueue
import time

class AStarMaze(maze_generator.Maze):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.maze = maze_generator.prims_algo(w, h, self)

    def h_func(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)


def a_star(maze: AStarMaze, w, h, start, end):
    start.g_score = 0
    start.f_score = maze.h_func(start)

    pqu = PriorityQueue()
    pqu.put((start.f_score, start))
    a_path = {}  # Stores the address of the previous cell of a cell
    visited_cells = set()

    while not pqu.empty():
        _, curr_cell = pqu.get()
        curr_cell.set_visited(True)
        visited_cells.add(curr_cell)

        if curr_cell == end:
            break

        surr_cells = maze_generator.get_surrounding_cells(maze, curr_cell, w, h)
        for next_cell in surr_cells:
            if next_cell not in visited_cells and next_cell.get_state() in ['p', 'e', 'r']:
                temp_next_cell_g_score = curr_cell.g_score + 1
                temp_next_cell_f_score = temp_next_cell_g_score + maze.h_func(next_cell)

                if temp_next_cell_f_score < next_cell.f_score:
                    next_cell.g_score = temp_next_cell_g_score
                    next_cell.f_score = temp_next_cell_f_score
                    pqu.put((next_cell.f_score, next_cell))
                    a_path[next_cell] = curr_cell

    fwd_path = {}
    cell = end
    while cell != start:
        fwd_path[a_path[cell]] = cell
        cell = a_path[cell]

    return fwd_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a maze and use A-Star to solve it.')
    parser.add_argument('-l', '--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('-w', '--width', type=int, default=60,
                        help='Width of the maze')
    parser.add_argument('-v', '--visualize', type=str, default='N',
                        help='Visualize the maze? [Y/N]')
    args = parser.parse_args()

    maze = AStarMaze(w=args.width, h=args.height)
    maze = maze_generator.prims_algo(w=args.width, h=args.height, maze=maze)
    start, end = maze.set_start_end_points()

    if args.visualize == 'Y':
        maze.visualize_maze()

    start_time = time.time()
    path = a_star(maze, args.width, args.height, start, end)
    print("time taken:", time.time() - start_time)

    cells_visited = sum(cell.is_visited() for row in maze for cell in row)
    print("cells_visited:", cells_visited)

    if args.visualize == 'Y':
        maze.visualize_maze(path)
