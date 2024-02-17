# Maze terminology:
# Cell: Any pixel in maze which can be either wall or passage
# Passage: 'p'
# Wall: 'w'

import random
import argparse

class Maze(object):
    def __init__(self, w, h):
        self.columns = []
        for i in range(w):
            self.columns.append(Column(col_length=h, col_no=i))

    def __getitem__(self, index):
        return self.columns[index]

    def __setitem__(self, index, value):
        assert isinstance(value, Column), 'Items in maze should be an instance of Column class.'
        self.columns[index] = value
    
    def __len__(self):
        return len(self.columns)

    def __str__(self):
        ret = ''
        for i in self.columns:
            ret += str(i) + '\n'
        return ret

class Column(object):
    def __init__(self, col_length, col_no):
        self.cell_list = []
        self.col_no = col_no
        for i in range(col_length):
            self.cell_list.append(Cell(x=self.col_no, y=i))

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
        self._visited = visited
        self._state = state # either 'w'(wall) or 'p'(passage)

    def __str__(self):
        return self._state
        # return f'({self.x},{self.y},{self._state})'

    def get_state(self):
        return self._state

    def set_state(self, value):
        assert value=='w' or value=='p', 'State value should be either w or p.'
        self._state = value

    def is_visited(self):
        return self._visited

    def set_visited(self, value):
        assert value==True or value==False, 'Visited value should be either True or False.'
        self._visited = value

def prims_algo(w=20, h=20):
    def get_surronding_cells(maze, cell, w, h):
        ret = []
        if(cell.x!=0): ret.append(maze[cell.x-1][cell.y])
        if(cell.x!=w-1): ret.append(maze[cell.x+1][cell.y])
        if(cell.y!=0): ret.append(maze[cell.x][cell.y-1])
        if(cell.y!=h-1): ret.append(maze[cell.x][cell.y+1])
        # print(ret)
        return ret

    if(w<4 or h<4):
        print("Width or Height should be more than 4. Exiting")
        exit
    maze = Maze(w, h)
    start_x = random.randint(1, w-2)
    start_y = random.randint(1, h-2)
    maze[start_x][start_y].set_state('p')
    maze[start_x][start_y].set_visited(True)
    # print('start:', maze[start_x][start_y])
    walls_list = [maze[start_x-1][start_y], maze[start_x][start_y-1], maze[start_x][start_y+1], maze[start_x+1][start_y]]

    while walls_list:
        cell = random.choice(walls_list)
        # print("random cell:",cell)
        cell.set_visited(True)

        surr_cells = get_surronding_cells(maze, cell, w, h)
        visit_count = 0
        for i in surr_cells:
            if(i.get_state()=='p'):
                visit_count += 1
                visited_cell = i
        if(visit_count==1):
            cell.set_state('p')
            surr_cells.remove(visited_cell)
            walls_list.extend(surr_cells)

        walls_list.remove(cell)
    print(maze)

def is_on_border_h_v(cell, w, h):
    """
    checks if the selected cell is on a bordering wall.
    Return 2 values in a list.
    Bool: returns true if on top or bottom border
    Bool: returns true if on left or vertical border
    """
    ret = [False, False]
    if(cell.x==w-1 or cell.x==0): ret[0] = True
    if(cell.y==h-1 or cell.y==0): ret[1] = True
    return ret

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
    parser = argparse.ArgumentParser(description='An example script with command-line arguments.')
    parser.add_argument('--height', type=int, default=25, help='Height of the maze')
    parser.add_argument('--width', type=int, default=20, help='Width of the maze')
    args = parser.parse_args()
    prims_algo(args.width, args.height) # Iterative Randomized Prim's Algo
