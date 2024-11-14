import json
import random
import math
import os
import matplotlib.pyplot as plt
import time
import numpy as np
from multiprocessing import Pool, cpu_count
import TTP_Generator



def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def objective_function(tour,packinglist, items, distances, vmax, vmin, W, R): #check formula again
    total_value = 0
    W_c = 0 #This keep track of the the total weight what is in the knapsack
    travel_time = 0
    #total_distance = 0
    random_actual_packing_list=[]
    for i in range(len(tour)):
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        distance_current_next = distances[current_city][next_city] 
        #total_distance += distances[current_city][next_city]        # Total distance needed in the for loop item in items
        for item in items:
            if item['city'] == current_city:
                if item['id'] in packinglist:
                    if W_c + item['weight']<= W:
                        total_value += item['value']        
                        W_c += item['weight']
                        random_actual_packing_list.append(item['id'])
        if W_c > W:
            raise ValueError("Current weight (W_c) exceeds knapsack capacity (W).")                      
        speed = max(vmin, vmax - W_c * (vmax - vmin) / W)
        travel_time += distance_current_next/speed
  #  if W_c > W:
  #      raise ValueError("Current weight (W_c) exceeds knapsack capacity (W).")        
   #speed = max(vmin, vmax - W_c * (vmax - vmin) / W) 
    #travel_time = total_distance / speed                            #Travel time need calculated also in for loop
    cost = travel_time * R
    #print(cost,total_distance)
    OB = total_value - cost
    random_actual_packing_list.sort()
    return OB, random_actual_packing_list, cost

def random_tour_and_packing(ttp):
    cities = ttp['cities']
    items = ttp['items']
    distances = ttp['distances']
    total_weight_ttp_instance = 0
    num_cities = len(cities)
    num_items = len(items)
   # max_value_item=0
    for item in items:
        total_weight_ttp_instance += item['weight']
    #    if item['value']>max_value_item:
    #        max_value_item = item['value']
   # distance_matrix = np.array(distances)
   # min_distance = np.min(distance_matrix[distance_matrix > 0])
    vmax = 1.0
    vmin = 0.1
    Tr=0.25 #Tightness ratio interval [0,1], suggested 0.25,0.5,0.75
    W = round(Tr*total_weight_ttp_instance)                #num_items*50/2 #might change.
   # r=0.05 # r is a random number in the interval [0.05,0.25], this will be fixed in this experiment to 0.15, to keep it more consistent and keeping it in the middle, for abitritary reasons
   # E_p=Tr*num_items*max_value_item
   # E_t = min_distance*num_cities/vmax #vague formula, don't understand why divided by vmax considering it is 1
    R = 1.0#r*(E_p/E_t)#1.0 #might change

    random_tour = list(range(1, num_cities))  # Exclude starting city (0) for shuffling
    random.shuffle(random_tour)
    random_tour = [0] + random_tour + [0]  # Ensure tour starts and ends at city 0
    random_packing_binary_list= generate_binary_list_with_probability(num_items,Tr)
    random_packing_integer_list = read_binary_list_as_integers(random_packing_binary_list)
    OB_value, random_actual_packing_list, cost = objective_function(random_tour, random_packing_integer_list, items, distances, vmax, vmin, W, R)
    return random_tour, random_packing_integer_list, random_actual_packing_list, OB_value, W, R

def generate_binary_list_with_probability(num_items, probability):
    result = []
    for i in range(num_items):
        # 50% chance for each position to be 1 or 0
        result.append(1 if random.random() < probability else 0)
    return result

def read_binary_list_as_integers(binary_list):
    integers = []
    for i, bit in enumerate(binary_list):
        if bit == 1:  # If the bit is 1, include the index as the integer
            integers.append(i)
    return integers


def process_ttp_instances_results(input_folder, output_file,iteration):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as f:
                ttp = json.load(f)
            start_time = time.time()    
            random_tour, random_packing_list,random_actual_packing_list ,OB_value, W, R = random_tour_and_packing(ttp)
            end_time = time.time()
            computing_time = end_time - start_time
            results.append({
                'problem_instance_filename': f'{input_folder}/{filename}',
                'Iteration': iteration,
                'random_tour': random_tour,
                'random_packing_list':random_packing_list,
                'random_actual_packing_list': random_actual_packing_list,
                'OB_value': OB_value ,
                'W_capacity': W,
                'rent_rate': R,
                'computing_time': computing_time
            })
    save_to_json(results, output_file)

def parallel_process_ttp(input_folders, output_files, iterations):
    try:
        num_cores = cpu_count()
        with Pool(num_cores) as pool:
            pool.starmap(process_ttp_instances_results, zip(input_folders, output_files, iterations))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pool.close()
        pool.join()

if __name__ == "__main__":
    os.makedirs('tour_results', exist_ok=True)
    os.makedirs('tour_results/random_results', exist_ok=True)
    #iteration = 1

    input_folders = []
    output_files = []
    iterations = []
    
    for i in range(1, 3):
        #name_directory = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
         #       os.makedirs(name_directory, exist_ok=True)  
       # name_directory = f'tour_results/random_results/iteration_{i}'
        #os.makedirs(name_directory, exist_ok=True)
        for cities in range(20, 120, 20):
            for n in range(1, 5):     
                items = n * cities
                name_directory = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
                os.makedirs(name_directory, exist_ok=True)
                input_folder = f'problem_instances_ttp/json_files_TTP_instances_{cities}_items_{items}'
                output_file = f'{name_directory}/results_random_iteration_{i}_cities_{cities}_items_{items}.json'

                input_folders.append(input_folder)
                output_files.append(output_file)
                iterations.append(i)

    # Process the TTP instances in parallel
    parallel_process_ttp(input_folders, output_files, iterations)