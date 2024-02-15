# Maze terminology:
# Cell: Any pixel in maze which can be either wall or passage
# Passage: 'p'
# Wall: 'w'

import random

class Maze(object):
    def __init__(self, w, h):
        self.rows = []
        for i in range(h):
            self.rows.append(Column(col_length=w, col_no=i))

    def __getitem__(self, index):
        return self.rows[index]

    def __setitem__(self, index, value):
        assert isinstance(value, Column), 'Items in maze should be an instance of Column class.'
        self.rows[index] = value
    
    def __len__(self):
        return len(self.rows)

    def __str__(self):
        ret = ''
        for i in self.rows:
            ret += str(i) + '\n'
        return ret

class Column(object):
    def __init__(self, col_length, col_no):
        self.cell_list = []
        self.col_no = col_no
        for i in range(col_length):
            self.cell_list.append(Cell(x=i, y=self.col_no))

    def __getitem__(self, index):
        return self.cell_list[index]

    def __setitem__(self, index, value):
        assert isinstance(value, Cell), 'Items in maze columns should be an instance of Cell class.'
        self.cell_list[index] = value
    
    def __len__(self):
        return len(self.cell_list)

    def __str__(self):
        ret = '['
        for i in self.cell_list:
            ret += str(i) + ', '
        return ret + ']'

class Cell(object):
    def __init__(self, x, y, state='w', visited=False):
        self.x = x
        self.y = y
        self.visited = visited
        self.state = 'w' # either 'w'(wall) or 'p'(passage)

    def __str__(self):
        return self.state

def main(w=20, h=20):
    maze = Maze(w, h)
    maze[1][9].state = 'p'
    maze[1][8].state = 'p'
    print(maze)
    start_x = random.randint(1, w-1)
    start_y = random.randint(1, h-1)
    print(start_x, start_y)
    walls_list = [maze[start_x-1][start_y], maze[start_x][start_y-1], maze[start_x][start_y+1], maze[start_x+1][start_y]]

    for i in walls_list:
        print(i.x, i.y)

def is_on_border_h_v(cell, w, h):
    """
    checks if the selected cell is on a bordering wall.
    Return 2 values in a list.
    Bool: returns true if on top or bottom border
    Bool: returns true if on left or vertical border
    """
    ret = [False, False]
    # if(cell)

# def initialize_maze(w, h):
#     visited = []
#     maze = []
#     for i in range(h):
#         maze_row = []
#         visited_row = []
#         for j in range(w):
#             maze_row.append('w')
#             visited_row.append(False)
#         maze.append(maze_row)
#         visited_row.append(visited_row)
#     return maze, visited_row

if __name__ == '__main__':
    main()
