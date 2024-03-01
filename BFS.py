import time
import maze_generator
import argparse
from collections import deque

def bfs(maze, w, h, start, end):
    queue = deque([(start, [start])])
    while queue:
        curr, path = queue.popleft()

        if curr==end:
            print("FOUND THE PATH")
            for i in path:
                i.set_state('r')
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
    parser.add_argument('-l','--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('-w','--width', type=int, default=60,
                        help='Width of the maze')
    parser.add_argument('-v','--visualize', type=str, default='N',
                        help='Visualize the maze? [Y/N]')
    args = parser.parse_args()



    maze = maze_generator.prims_algo(w=args.width, h=args.height)
    start, end = maze.set_start_end_points()
    if(args.visualize=='Y'):
        maze.visualize_maze()

    start_time = time.time()
    path = bfs(maze, w=args.width, h=args.height)
    print("time taken:", time.time()-start_time)
    
    cells_visited=0
    for row in maze:
        for cell in row:
            if(cell.is_visited()):
                cells_visited+=1
    print("cells_visited:",cells_visited)

    if(args.visualize=='Y'):
        maze.visualize_maze(path=path)
