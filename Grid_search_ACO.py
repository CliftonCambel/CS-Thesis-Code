import ACO
import random
import itertools
import pandas as pd
import os
import Hillclimber_TSP_swaping
from multiprocessing import Pool, cpu_count



# Load problem instance file paths
def load_problem_instances(base_dir, size_group_dir):
    group_path = os.path.join(base_dir, size_group_dir)
    files = [os.path.join(group_path, f) for f in os.listdir(group_path) if f.endswith('.json')]
    return files


def run_aco_on_instance(args):
    """Run ACO on a single problem instance."""
    ttp, params = args
    num_ants, alpha, beta, evaporation_rate, q_percentage, iterations = params
    total_item_value = sum(item["value"] for item in ttp["items"])
    q = q_percentage * total_item_value

    # Run ACO and return fitness
    _, _, fitness = ACO.ant_colony_optimization(
        ttp, num_ants=num_ants, alpha=alpha, beta=beta,
        evaporation_rate=evaporation_rate, q=q, iterations=iterations
    )
    return fitness

def calculate_variance(fitness_scores):
    """Calculate variance of fitness scores."""
    mean = sum(fitness_scores) / len(fitness_scores)
    variance = sum((x - mean) ** 2 for x in fitness_scores) / len(fitness_scores)
    return variance

def grid_search_ACO():
    # Parameter ranges
    alpha_range = [0.5, 1.5]
    beta_range = [1.0, 3.0]
    evaporation_rate_range = [0.3, 0.7]
    q_range = [0.1, 0.2]
    iterations_range = [50, 100]


    # All parameter combinations
    #parameter_grid = list(itertools.product(num_ants_range, alpha_range, beta_range, evaporation_rate_range, q_range))
    # Global parameter grid
    global_parameter_grid = list(itertools.product(
        alpha_range, beta_range, evaporation_rate_range, q_range, iterations_range
    ))

# Randomly sample from each group
    size_groups = {
    "20x20": "json_files_TTP_instances_20_items_20",
    "20x40": "json_files_TTP_instances_20_items_40",
    "20x60": "json_files_TTP_instances_20_items_60",
    "20x80": "json_files_TTP_instances_20_items_80",
    "40x40": "json_files_TTP_instances_40_items_40",
    "40x80": "json_files_TTP_instances_40_items_80",
    "40x120": "json_files_TTP_instances_40_items_120",
    "40x160": "json_files_TTP_instances_40_items_160",
    "60x60": "json_files_TTP_instances_60_items_60",
    "60x120": "json_files_TTP_instances_60_items_120",
    "60x180": "json_files_TTP_instances_60_items_180",
    "60x240": "json_files_TTP_instances_60_items_240",
    "80x80": "json_files_TTP_instances_80_items_80",
    "80x160": "json_files_TTP_instances_80_items_160",
    "80x240": "json_files_TTP_instances_80_items_240",
    "80x320": "json_files_TTP_instances_80_items_320",
    "100x100": "json_files_TTP_instances_100_items_100",
    "100x200": "json_files_TTP_instances_100_items_200",
    "100x300": "json_files_TTP_instances_100_items_300",
    "100x400": "json_files_TTP_instances_100_items_400"
    }

    base_dir = "problem_instances_ttp"
    problem_files = {group: load_problem_instances(base_dir, dir_name) for group, dir_name in size_groups.items()}

    sampled_instances = {
        group: random.sample(files, k=min(len(files), 5)) for group, files in problem_files.items()
    }

    sampled_problems = {
        group: [Hillclimber_TSP_swaping.load_json(file) for file in files]
        for group, files in sampled_instances.items()
    }

    # Results storage
    results = []

    # Grid search over sampled instances
    for group, problems in sampled_problems.items():
        for ttp in problems:
            num_cities = len(ttp["cities"])
            num_ants_range = [max(1, num_cities // 2), num_cities, 2 * num_cities]

            # Batch parallel processing
            args_list = [
                (ttp, (num_ants, *params))
                for num_ants in num_ants_range
                for params in global_parameter_grid
            ]

            # Parallel execution
            cpu_count_sys = cpu_count()
            num_cores = min(cpu_count_sys, len(args_list))
            with Pool(num_cores) as pool:
                fitness_scores = pool.map(run_aco_on_instance, args_list)

            # Record results
            for (params, fitness) in zip(args_list, fitness_scores):
                ttp_params = params[1]
                results.append({
                    "group": group,
                    "num_ants": ttp_params[0],
                    "alpha": ttp_params[1],
                    "beta": ttp_params[2],
                    "evaporation_rate": ttp_params[3],
                    "q_percentage": ttp_params[4],
                    "iterations": ttp_params[5],
                    "avg_fitness": fitness
                })

        # Save intermediate results to avoid data loss
        with open("aco_intermediate_results.json", "w") as f:
            json.dump(results, f)

    return results

if __name__ == "__main__":
    results=grid_search_ACO()
    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Find the best parameters for each group
    best_params = df.groupby("group").apply(lambda x: x.nlargest(1, "avg_fitness"))
    print(best_params)

    # Save results to a CSV file for later analysis
    df.to_csv("aco_grid_search_results.csv", index=False)