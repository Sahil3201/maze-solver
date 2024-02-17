import maze_generator
import argparse
from collections import deque

def bfs(w, h):
    maze = maze_generator.prims_algo(w=w, h=h)
    start, end = maze.set_start_end_points()
    maze.visualize_maze()
    queue = deque([(start, [start])])
    while queue:
        curr, path = queue.popleft()

        if curr==end:
            print("FOUND THE PATH")
            for i in path:
                i.set_state('r')
            maze.visualize_maze(path=path)
            return path

        if curr.is_visited():
            continue

        curr.set_visited(True)
        neighbours = maze_generator.get_surrounding_cells(maze, curr, w, h)

        for ngh in neighbours:
            if ngh.get_state() in ['p', 'e'] and ngh.is_visited:
                queue.append((ngh, path+[ngh]))
    return []

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Generate a maze and use DFS to solve it.')
    parser.add_argument('--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('--width', type=int, default=60,
                        help='Width of the maze')
    args = parser.parse_args()

    path = bfs(w=args.width, h=args.height)
