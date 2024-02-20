# Citations: https://levelup.gitconnected.com/a-star-a-search-for-solving-a-maze-using-python-with-visualization-b0cae1c3ba92

import maze_generator
import argparse
from queue import PriorityQueue

class AStarMaze(maze_generator.Maze):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.maze = maze_generator.prims_algo(w, h, self)

    def h_func(self, cell):
        return abs(cell.x-self.end.x)-abs(cell.y-self.end.y)


def a_star(maze: AStarMaze, start, end, w, h):
    maze.visualize_maze()
    start.g_score = 0
    start.f_score = maze.h_func(start)

    pqu = PriorityQueue()
    # pqu.put((f-score, h-score, cell))
    pqu.put((maze.h_func(start), maze.h_func(start), start.x, start.y))
    a_path = {} # Stores the address of the previous cell of a cell
    while not pqu.empty():
        # print(pqu.queue)
        _ele = pqu.get()
        _x = _ele[2]
        _y = _ele[3]
        curr_cell = maze[_y][_x]
        if curr_cell==end:
            break
        surr_cells = maze_generator.get_surrounding_cells(maze, curr_cell, w, h)
        for next_cell in surr_cells:
            if next_cell.get_state() not in ['p', 'e', 'r']:
                continue
            temp_next_cell_g_score = curr_cell.g_score + 1
            temp_next_cell_f_score = temp_next_cell_g_score + maze.h_func(next_cell)
            # print(next_cell)
            # print(temp_next_cell_g_score)
            # print(temp_next_cell_f_score)

            if temp_next_cell_f_score < next_cell.f_score:
                next_cell.g_score = temp_next_cell_g_score
                next_cell.f_score = temp_next_cell_f_score
                pqu.put((next_cell.f_score, maze.h_func(next_cell), next_cell.x, next_cell.y))
                a_path[next_cell] = curr_cell
    print(len(a_path))
    fwd_path = {}
    cell = end
    while cell != start:
        fwd_path[a_path[cell]] = cell
        cell = a_path[cell]
    return fwd_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a maze and use A-Star to solve it.')
    parser.add_argument('--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('--width', type=int, default=60,
                        help='Width of the maze')
    args = parser.parse_args()

    maze = AStarMaze(w=args.width, h=args.height)
    maze = maze_generator.prims_algo(w=args.width, h=args.height, maze=maze)
    start, end = maze.set_start_end_points()
    path = a_star(maze, start, end, args.width, args.height)
    maze.visualize_maze(path)
