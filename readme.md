# Maze Solver

## Overview

This repository contains algorithms for maze generation and various pathfinding algorithms to solve the maze. The implemented pathfinding algorithms include:

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Algorithm
- Markov Decision Process (MDP) Value Iteration
- Markov Decision Process (MDP) Policy Iteration

## Getting Started

To explore and use this project, follow these steps:

1. Clone the repository using the following command:
    ```bash
    git clone https://github.com/Sahil3201/maze-solver
    ```

2. Change the directory to the cloned repository:
    ```bash
    cd maze-solver
    ```

3. Install the required dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a maze with a specified side length (50) and width (150) and visualize it:
    ```bash
    python .\maze_generator.py -l 50 -w 150
    ```

5. Run pathfinding algorithms with visualization:
    ```bash
    python .\dfs.py -l 50 -w 100 -v Y
    python .\bfs.py -l 50 -w 100 -v Y
    python .\astar.py -l 50 -w 100 -v Y
    python .\MdpValueIteration.py -l 50 -w 50 -v Y
    python .\MdpPolicyIteration.py -l 50 -w 50 -v Y
    ```

6. For more information on each algorithm, run:
    ```bash
    python <algo-filename> --help
    ```

Feel free to explore and contribute to the project!

## Author

Sahil Lunawat<br>
MSc in Computer Science<br>
Trinity College Dublin
