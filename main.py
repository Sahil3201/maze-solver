import maze_generator, mdp_maze_generator
import bfs, dfs, astar
import MdpPolicyIteration, MdpValueIteration
import copy, time
import psutil
import matplotlib.pyplot as plt

def memory_usage(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        result = func(*args, **kwargs)
        end_memory = process.memory_info().rss / 1024.0 / 1024.0  # in MB
        memory_used = end_memory - start_memory
        # print(f"Memory used by {func.__name__}: {memory_used:.2f} MB")
        return result, memory_used

    return wrapper

def plot_metrics(metric_names, metric_data, maze_size):
    for metric_name, metric_data in zip(metric_names, metric_data):
        plt.figure(figsize=(10, 6))
        for algo_name, algo_values in metric_data.items():
            plt.plot([str(size) for size in maze_size], algo_values, label=algo_name)

        plt.xlabel('Maze Size')
        plt.ylabel(metric_name)
        plt.title(f'{metric_name} Comparison for Algorithms')
        plt.legend()
        plt.show()

def compare_search_algos(maze_sizes_search_algo):
    # Lists to store metrics
    time_taken_data = {'bfs': [], 'dfs': [], 'a_star': []}
    cells_visited_data = {'bfs': [], 'dfs': [], 'a_star': []}
    memory_used_data = {'bfs': [], 'dfs': [], 'a_star': []}


    @memory_usage
    def run_algo(algo, *args):
        algo(*args)

    for i in maze_sizes_search_algo:
        print(f"Maze size: {i}")
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

    metric_names = ['Time Taken', 'Cells Visited', 'Memory Used']
    metric_data = [time_taken_data, cells_visited_data, memory_used_data]
    plot_metrics(metric_names, metric_data, maze_sizes_search_algo)


    print("\nResults Table:")
    print(f"{'Maze Size':<15}{'Algorithm':<15}{'Time Taken':<15}{'Cells Visited':<15}{'Memory Used':<15}")
    for size in maze_sizes_search_algo:
        for algo in [bfs.bfs, dfs.dfs, astar.a_star]:
            print(f"{str(size):<15}{algo.__name__:<15}{time_taken_data[algo.__name__].pop(0):<15.5f}"
                f"{cells_visited_data[algo.__name__].pop(0):<15}{memory_used_data[algo.__name__].pop(0):<15.2f}")

def compare_mdp_algos(maze_sizes_mdp_algo):
    # Lists to store metrics
    time_taken_data = {'value_iteration': [], 'policy_iteration': []}
    iterations_data = {'value_iteration': [], 'policy_iteration': []}
    memory_used_data = {'value_iteration': [], 'policy_iteration': []}


    @memory_usage
    def run_algo(algo, *args):
        return algo(*args)

    for i in maze_sizes_mdp_algo:
        print(f"Maze size: {i}")
        input_maze = mdp_maze_generator.MdpMaze(w=i[0], h=i[1])
        
        for algo in [MdpValueIteration.value_iteration, MdpPolicyIteration.policy_iteration]:
            maze = copy.deepcopy(input_maze)
            start, end = maze.set_start_end_points()
            start.reward = -100
            end.reward = 100
            end.set_state('e')
            args = [maze, i[0], i[1], start, end]

            start_time = time.time()
            run_result, memory_used = run_algo(algo, *args)
            _, __, iterations = run_result
            time_taken = time.time() - start_time
            
            # Store metrics
            time_taken_data[algo.__name__].append(time_taken)
            iterations_data[algo.__name__].append(iterations)
            memory_used_data[algo.__name__].append(memory_used)

    metric_names = ['Time Taken', 'Iterations Needed', 'Memory Used']
    metric_data = [time_taken_data, iterations_data, memory_used_data]
    plot_metrics(metric_names, metric_data, maze_sizes_mdp_algo)


    print("\nResults Table:")
    print(f"{'Maze Size':<15}{'Algorithm':<25}{'Time Taken':<15}{'Iterations Needed':<25}{'Memory Used':<15}")
    for size in maze_sizes_mdp_algo:
        for algo in [MdpValueIteration.value_iteration, MdpPolicyIteration.policy_iteration]:
            print(f"{str(size):<15}{algo.__name__:<25}{time_taken_data[algo.__name__].pop(0):<15.5f}"
                f"{iterations_data[algo.__name__].pop(0):<25}{memory_used_data[algo.__name__].pop(0):<15.2f}")


if __name__ == '__main__':
    # maze_sizes_search_algo = [(50, 50), (100, 100), (250, 250), (500, 500), (1000, 1000)]
    # compare_search_algos(maze_sizes_search_algo)

    maze_sizes_mdp_algo = [(10, 10), (50, 50)]#, (100, 100)]
    compare_mdp_algos(maze_sizes_mdp_algo)
