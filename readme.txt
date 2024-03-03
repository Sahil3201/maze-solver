Run `pip install -r requirements.txt` to install the requirements for this project.

To create a maze of side length 50 and width 50 and visualize it use:
`python .\maze_generator.py -l 50 -w 150`

Command to run algorithms with maze side length specified
by -l flag and width specified by -w and visualization flag
-v. Visualization can be switched off by not passing the -v flag

`python .\DFS.py -l 50 -w 100 -v Y`

`python .\BFS.py -l 50 -w 100 -v Y`

`python .\astar.py -l 50 -w 100 -v Y`

`python .\MdpPolicyIteration.py -l 50 -w 50 -v Y `

`python .\MdpValueIteration.py -l 50 -w 50 -v Y `


For more help, run:
`python <algo-filename> --help`
