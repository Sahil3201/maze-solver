import dfs, bfs, astar
import maze_generator
import copy, time
import psutil

maze_sizes = [(10,10), (100,100), (500,500)]



def memory_usage(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        result = func(*args, **kwargs)
        end_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        memory_used = end_memory - start_memory
        print(f"Memory used by {func.__name__}: {memory_used:.2f} MB")
        return result

    return wrapper

@memory_usage
def run_algo(algo, *args):
    algo(*args)
    return




for i in maze_sizes:
    input_maze = maze_generator.prims_algo(w=i[0], h=i[1])
    
    for algo in [bfs.bfs, dfs.dfs, astar.a_star]:
        maze = copy.deepcopy(input_maze)
        start, end = maze.set_start_end_points()
        args = [maze, i[0], i[1], start, end]

        start_time = time.time()
        run_algo(algo, *args)
        time_taken = time.time() - start_time
        cells_visited = sum(cell.is_visited() for row in maze for cell in row)
        print(f"{str(i):>15} -> {algo.__name__:<10}{time_taken:<20.5f}{cells_visited:<15}")
