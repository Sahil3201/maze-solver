# Maze terminology:
# Cell: Any pixel in maze which can be either wall or passage
# Passage: 'p'
# Wall: 'w'
#
# Maze generation algo implemented: Iterative Randomized Prim's Algo
################

import random
import argparse
import pygame
import numpy as np

class Maze(object):
    def __init__(self, w, h):
        self.rows = []
        for i in range(h):
            self.rows.append(Row(row_length=w, row_no=i))

    def __getitem__(self, index):
        return self.rows[index]

    def __setitem__(self, index, value):
        assert isinstance(
            value, Row), 'Items in maze should be an instance of Row class.'
        self.rows[index] = value

    def __len__(self):
        return len(self.rows)

    def __str__(self):
        ret = ''
        for i in self.rows:
            ret += str(i) + '\n'
        return ret


class Row(object):
    def __init__(self, row_length, row_no):
        self.cell_list = []
        self.row_no = row_no
        for i in range(row_length):
            self.cell_list.append(Cell(x=i, y=self.row_no))

    def __getitem__(self, index):
        return self.cell_list[index]

    def __setitem__(self, index, value):
        assert isinstance(
            value, Cell), 'Items in maze rows should be an instance of Cell class.'
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
        self._state = state  # either 'w'(wall) or 'p'(passage)

    def __str__(self):
        return self._state
        # return f'({self.x},{self.y},{self._state})'

    def get_state(self):
        return self._state

    def set_state(self, value):
        assert value in ['w', 'p', 's',
                         'e'], 'State value should be either w or p.'
        self._state = value

    def is_visited(self):
        return self._visited

    def set_visited(self, value):
        assert value == True or value == False, 'Visited value should be either True or False.'
        self._visited = value


def prims_algo(w=20, h=20):
    def get_surronding_cells(maze, cell, w, h):
        ret = []
        if (cell.x != 0):
            ret.append(maze[cell.y][cell.x-1])
        if (cell.x != w-1):
            ret.append(maze[cell.y][cell.x+1])
        if (cell.y != 0):
            ret.append(maze[cell.y-1][cell.x])
        if (cell.y != h-1):
            ret.append(maze[cell.y+1][cell.x])
        # print(ret)
        return ret

    if (w < 4 or h < 4):
        print("Width or Height should be more than 4. Exiting")
        exit
    maze = Maze(w, h)
    start_x = random.randint(1, w-2)
    start_y = random.randint(1, h-2)
    maze[start_y][start_x].set_state('p')
    maze[start_y][start_x].set_visited(True)
    walls_list = [maze[start_y][start_x-1], maze[start_y-1][start_x],
                  maze[start_y+1][start_x], maze[start_y][start_x+1]]

    while walls_list:
        cell = random.choice(walls_list)
        # print("random cell:",cell)
        cell.set_visited(True)

        surr_cells = get_surronding_cells(maze, cell, w, h)
        visit_count = 0
        for i in surr_cells:
            if (i.get_state() == 'p'):
                visit_count += 1
                visited_cell = i
        if (visit_count == 1):
            cell.set_state('p')
            surr_cells.remove(visited_cell)
            walls_list.extend(surr_cells)

        walls_list.remove(cell)
    return maze
    

def visualize_maze(maze):
    pygame.init()
    h = len(maze)
    w = len(maze[0])
    size = (w*10, h*10)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze Visualization")

    colors = {'p': (255, 255, 255), 'w': (0, 0, 0),
              'e': (255, 0, 0), 's': (0, 0, 255)}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                pygame.draw.rect(
                    screen, colors[str(cell)], (j * 10, i * 10, 10, 10))

        pygame.display.flip()


def get_start_end_points(maze):
    start = None
    end = None
    h = len(maze)
    w = len(maze[0])
    for i in range(0, w):
        if start == None and maze[0][i].get_state() == 'p':
            start = maze[0][i]
        if end == None and maze[h-1][w-1-i].get_state() == 'p':
            end = maze[h-1][w-1-i]
    return start, end


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='An example script with command-line arguments.')
    parser.add_argument('--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('--width', type=int, default=60,
                        help='Width of the maze')
    args = parser.parse_args()
    print("Printing maze:")
    maze = prims_algo(args.width, args.height)
    start, end = get_start_end_points(maze)
    start.set_state('s')
    end.set_state('e')
    visualize_maze(maze)
