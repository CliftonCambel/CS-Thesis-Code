import random
import TTP_random_tour_and_packing_list
import Iteration_search
import os
import time
import Hillclimber_TSP_swaping
from multiprocessing import Pool, cpu_count
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def hill_climb_hybrid(ttp, random_sample, iterations):
    cities = ttp['cities']
    #print(cities)
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    #print(num_cities)
    num_items = len(items)
    packinglist = random_sample['random_actual_packing_list']
    total_weight_ttp_instance = 0
    
    # Calculate the total weight of all items in the TTP instance
    for item in items:
        total_weight_ttp_instance += item['weight']

    Tr = 0.25  # Tightness ratio interval [0,1], suggested 0.25,0.5,0.75
    W = round(Tr * total_weight_ttp_instance)  # Example formula, may be adjusted
    vmax = 1.0
    vmin = 0.1
    R = 1.0
    # Initial random tour
    best_tour = random_sample['random_tour']
    best_fitness = random_sample['OB_value']
    #print(best_tour)
    # Ensure that `best_tour` is a list and correctly formatted
    if not isinstance(best_tour, list):
        raise ValueError("Expected `random_tour` to be a list, but got an integer or other non-iterable object.")

    # Ensure the initial tour starts and ends at node 0
    if best_tour[0] != 0 or best_tour[-1] != 0:
        best_tour = [0] + [city for city in best_tour if city != 0] + [0]
    for _ in range(iterations):
        # Generate a neighboring solution by swapping two cities
        new_tour = best_tour[:]
        if num_cities > 2:  # Ensure there's enough to swap
            i, j = random.sample(range(1, num_cities - 1), 2)
            
            # Swap the two cities
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            # Evaluate the new tour

        # Generate a neighboring solution by changing the knapsack content
        new_packinglist = packinglist[:]
        if random.random() < 0.5:  # 50% chance to add or remove an item
            # Try adding a random item
            random_item_id = random.randint(0, num_items - 1)
            random_item = [item for item in items if item['id'] == random_item_id]
            if random_item_id not in new_packinglist and random_item and sum(item['weight'] for item in items) + random_item[0]['weight'] <= W:
                new_packinglist.append(random_item_id)
            # Or try removing a random item
            elif new_packinglist:
                new_packinglist.remove(random.choice(new_packinglist))

        # Evaluate the new solution
        new_fitness, _, _ = TTP_random_tour_and_packing_list.objective_function(new_tour, new_packinglist, items, distances, vmax, vmin, W, R)

        # Accept the new solution if it's better
        if new_fitness > best_fitness:
            best_fitness = new_fitness
            best_route = new_tour
            best_knapsack = new_packinglist

    return best_route, best_knapsack, best_fitness


def process_ttp_instances_results_hill_hybride( input_folders_results_random, output_file):
    results = []
    iterations = 1000
    random_results=Iteration_search.load_iteration_results(input_folders_results_random)
    #print('okay')
    for idx, result in enumerate(random_results, start=1):
        filename_problem_instance = result['problem_instance_filename']
        if not os.path.exists(filename_problem_instance):
            print(f"Error: {filename_problem_instance} does not exist.")
            return
        #print(result)
        ttp_problem_instance = Hillclimber_TSP_swaping.load_json(filename_problem_instance)
        #cities = ttp_problem_instance.get("cities", [])
        #items = ttp_problem_instance.get("items", [])
    #for filename in os.listdir(input_folder):
    #    if filename.endswith('.json'):
    #        with open(os.path.join(input_folder, filename), 'r') as f:
    #            ttp = json.load(f)
        start_time = time.time()  
        best_tour, best_knapsack, best_value = hill_climb_hybrid(ttp_problem_instance, result,iterations)
        end_time = time.time()
        computing_time = end_time - start_time
        results.append({
                'filename': filename_problem_instance,
                'Iteration_random_sample':result['Iteration'],
                'old_random_tour':result['random_tour'],
                'best_new_tour': best_tour,
                'old_actual_fixed_packinglist':result['random_actual_packing_list'],
                'old_actual_fixed_packinglist':best_knapsack,
                'initial_OB_value':result['OB_value'],
                'new_OB_value': best_value,
                'computing_time': computing_time
            })
   #     logging.info(f"Processed {idx}/{len(random_results)} tasks in {input_folder_results_random}")
   # Hillclimber_TSP_swaping.save_to_json(results, output_file)
   # logging.info(f"Finished processing for {input_folder_results_random} -> {output_file}")
        if idx % 10 == 0 or idx == len(random_results):
            Hillclimber_TSP_swaping.save_to_json(results, output_file)
            logging.info(f"Saved intermediate results to {output_file} (processed {idx}/{len(random_results)} tasks)")


def parallel_process_ttp(input_folders_results_random, output_files):
    try:
        num_tasks = len(list(zip(input_folders_results_random, output_files)))
        cpu_count_sys=cpu_count()
        num_cores = min(cpu_count_sys, num_tasks)
        print("number of cores avaiable in the system ", cpu_count())
        print("number of cores avaiable in the system ", num_cores)


                # Manager for shared state (progress tracking)
        #manager = Manager()
        #progress = manager.Value('i', 0)  # Shared integer to track progress
        #total_tasks = len(input_folders_results_random)
        progress_bar = tqdm(total=num_tasks, desc="Processing TTP Instances")
        start_time = time.time()

        
        def track_progress(input_folder, output_file):
            #nonlocal progress
            process_ttp_instances_results_hill_hybride(input_folder, output_file)
            elapsed_time = time.time() - start_time
            avg_time_per_task = elapsed_time / progress_bar.n if progress_bar.n > 0 else 0
            remaining_time = avg_time_per_task * (num_tasks - progress_bar.n)
            progress_bar.set_postfix({"ETA (s)": f"{remaining_time:.2f}"})
            progress_bar.update(1)
        
        with Pool(num_cores) as pool:
            pool.starmap(track_progress, zip(input_folders_results_random, output_files))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        progress_bar.close()


if __name__ == "__main__":
    iterations = 1000
    os.makedirs('tour_results/hillclimber_hybride_results', exist_ok=True)
    input_folders_problem_instances = []
    input_folders_results_random = []
    output_files = []

    for cities in range(20, 120, 20):
        #print(cities)
        for n in range(1, 5): 
            #print(n)    
            items = n * cities
            name_directory = f'tour_results/hillclimber_hybride_results/TTP_instances_{cities}_items_{items}'
            os.makedirs(name_directory, exist_ok=True)
            #input_folder_problem_instances = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'
            input_folder_results_random = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
           # input_folders_problem_instances.append(input_folder_problem_instances)
            input_folders_results_random.append(input_folder_results_random)
            output_file=f'{name_directory}/results_hillclimber_tsp_cities_{cities}_items_{items}.json'
            output_files.append(output_file)
    # Process the TTP instances and save results
    #output_file = 'results.json'
    #print("okay")
    parallel_process_ttp(input_folders_results_random, output_files, iterations)

    #print(f"Results saved to {output_file}")