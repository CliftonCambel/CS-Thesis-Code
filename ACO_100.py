import ACO
import random
import numpy as np
import TTP_random_tour_and_packing_list
import Hillclimber_TSP_swaping
import os
from multiprocessing import Pool, cpu_count
import time
import Iteration_search
import json

if __name__ == "__main__":
    os.makedirs('tour_results/aco_results_100c', exist_ok=True)
  #  input_folders_problem_instances = []
  #  input_folders_results_random = []
    input_folders = []
    output_files = []

    for n in range(1, 5): 
        for i in range(1, 5): 
            items = n * 100
            name_directory = f'tour_results/aco_results_100c/TTP_instances_100_items_{items}_{i}'
            os.makedirs(name_directory, exist_ok=True)
            input_folder = f'problem_instances_ttp_100c/json_files_TTP_instances_100_items_{items}'
            output_file=f'{name_directory}/results_aco_100_items_{items}_{i}.json'
            input_folders.append(input_folder)
            output_files.append(output_file)
    ACO.parallel_process_ttp(input_folders, output_files)