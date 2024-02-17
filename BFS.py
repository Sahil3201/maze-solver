import maze_generator

def bfs():
    maze = maze_generator.prims_algo(w=40, h=40)
    maze_generator.visualize_maze(maze)
    print(maze)

if __name__=='__main__':
    bfs()
