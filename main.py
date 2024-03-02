# TODO: Remove
import playsound 
import dfs, bfs, astar
import maze_generator
import copy, time
import psutil
import matplotlib.pyplot as plt

maze_sizes = [(10, 10), (50, 50), (100, 100)]#, (250, 250), (500, 500), (1000, 1000)]

# Lists to store metrics
time_taken_data = {'bfs': [], 'dfs': [], 'a_star': []}
cells_visited_data = {'bfs': [], 'dfs': [], 'a_star': []}
memory_used_data = {'bfs': [], 'dfs': [], 'a_star': []}

def memory_usage(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        result = func(*args, **kwargs)
        end_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        memory_used = end_memory - start_memory
        print(f"Memory used by {func.__name__}: {memory_used:.2f} MB")
        return result, memory_used

    return wrapper

@memory_usage
def run_algo(algo, *args):
    algo(*args)

for i in maze_sizes:
    input_maze = maze_generator.prims_algo(w=i[0], h=i[1])
    
    for algo in [bfs.bfs, dfs.dfs, astar.a_star]:
        maze = copy.deepcopy(input_maze)
        start, end = maze.set_start_end_points()
        args = [maze, i[0], i[1], start, end]

        start_time = time.time()
        run_result, memory_used = run_algo(algo, *args)
        time_taken = time.time() - start_time
        cells_visited = sum(cell.is_visited() for row in maze for cell in row)
        
        # Store metrics
        time_taken_data[algo.__name__].append(time_taken)
        cells_visited_data[algo.__name__].append(cells_visited)
        memory_used_data[algo.__name__].append(memory_used)

# Plotting
for metric_name, metric_data in zip(['Time Taken', 'Cells Visited', 'Memory Used'],
                                    [time_taken_data, cells_visited_data, memory_used_data]):
    plt.figure(figsize=(10, 6))
    for algo_name, algo_values in metric_data.items():
        plt.plot([str(size) for size in maze_sizes], algo_values, label=algo_name)

    plt.xlabel('Maze Size')
    plt.ylabel(metric_name)
    plt.title(f'{metric_name} Comparison for Algorithms')
    plt.legend()
    plt.show()

print("\nResults Table:")
print(f"{'Maze Size':<15}{'Algorithm':<15}{'Time Taken':<15}{'Cells Visited':<15}{'Memory Used':<15}")
for size in maze_sizes:
    for algo in [bfs.bfs, dfs.dfs, astar.a_star]:
        print(f"{str(size):<15}{algo.__name__:<15}{time_taken_data[algo.__name__].pop(0):<15.5f}"
              f"{cells_visited_data[algo.__name__].pop(0):<15}{memory_used_data[algo.__name__].pop(0):<15.2f}")


playsound.playsound('beep_3.mp3')
