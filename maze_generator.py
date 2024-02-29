""" Maze terminology:
    Cell: Any pixel in maze which can be either wall or passage
    Passage: 'p'
    Wall: 'w'
    Start: 's'
    End: 'e'
    Route: 'r'

    Maze generation algo implemented: Iterative Randomized Prim's Algo
"""

import random
import argparse
# import numpy as np
import threading
import os
# To suppress a welcome message from pygame when we import pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class Cell(object):
    def __init__(self, x, y, state='w', visited=False):
        self.x = x
        self.y = y
        self._visited = visited
        self._state = state  # either 'w'(wall) or 'p'(passage)
        self.g_score = float('inf')
        self.f_score = float('inf')

    def __str__(self):
        return f'({self.y},{self.x},{self._state})'
        # return self._state

    def get_state(self):
        return self._state

    def set_state(self, value):
        assert value in ['w', 'p', 's',
                         'e', 'r'], 'State value should be w, p, s, e, r.'
        self._state = value

    def is_visited(self):
        return self._visited

    def set_visited(self, value):
        assert value == True or value == False, 'Visited value should be either True or False.'
        self._visited = value


class Row(object):
    def __init__(self, row_length, row_no, CellDef):
        self.cell_list = []
        self.row_no = row_no
        for i in range(row_length):
            self.cell_list.append(CellDef(x=i, y=self.row_no))

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


class Maze(object):
    def __init__(self, w, h, CellDef=Cell):
        self.w = w
        self.h = h
        self.rows = []
        self.start = None
        self.end = None
        for i in range(h):
            self.rows.append(Row(row_length=w, row_no=i, CellDef=CellDef))

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

    def set_start_end_points(self):
        start = None
        end = None
        for i in range(0, self.w):
            if start == None and self[0][i].get_state() == 'p':
                start = self[0][i]
            if end == None and self[self.h-1][self.w-1-i].get_state() == 'p':
                end = self[self.h-1][self.w-1-i]
        start.set_state('s')
        end.set_state('e')
        self.start = start
        self.end = end
        return start, end

    def visualize_maze(self, path=None):
        cell_size = 6
        pygame.init()
        size = (self.w*cell_size, self.h*cell_size)

        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Maze Visualization")

        colors = {'p': (255, 255, 255), 'w': (0, 0, 0),
                  'e': (255, 0, 0), 's': (13, 158, 8), 'r': (13, 158, 8)}

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            for i, row in enumerate(self):
                for j, cell in enumerate(row):
                    color = colors[cell.get_state()]
                    if path and cell in path:
                        color = colors['r']
                    pygame.draw.rect(
                        screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

            pygame.display.flip()


def get_surrounding_cells(maze, cell, w, h):
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


def prims_algo(w=20, h=20, maze=None):
    if (w < 4 or h < 4):
        print("Width or Height should be more than 4. Exiting")
        exit()
    if not maze:
        maze = Maze(w, h)
    start_x = random.randint(1, w-2)
    start_y = random.randint(1, h-2)
    maze[start_y][start_x].set_state('p')
    # maze[start_y][start_x].set_visited(True)
    walls_list = [maze[start_y][start_x-1], maze[start_y-1][start_x],
                  maze[start_y+1][start_x], maze[start_y][start_x+1]]

    while walls_list:
        cell = random.choice(walls_list)
        # print("random cell:",cell)
        # cell.set_visited(True)

        surr_cells = get_surrounding_cells(maze, cell, w, h)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a maze')
    parser.add_argument('--height', type=int, default=45,
                        help='Height of the maze')
    parser.add_argument('--width', type=int, default=60,
                        help='Width of the maze')
    args = parser.parse_args()

    maze = prims_algo(args.width, args.height)
    maze.visualize_maze()
