import json
import random
import math
import os
import matplotlib.pyplot as plt
import time

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def objective_function(tour,packinglist, items, distances, vmax, vmin, W, R): #check formula again
    total_value = 0
    total_weight = 0
    total_distance = 0
    for i in range(len(tour)):
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        total_distance += distances[current_city][next_city]
        for item in items:
            if total_weight <= W:
                if item['city'] == current_city:
                    if item['id'] in packinglist:
                        total_value += item['value']        
                        total_weight += item['weight']
            
    speed = vmax - (vmax - vmin) * (total_weight / W)
    travel_time = total_distance / speed
    cost = travel_time * R
    return total_value - cost

def random_tour_and_packing(ttp):
    cities = ttp['cities']
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    num_items = len(items)

    
    vmax = 1.0
    vmin = 0.1
    W = num_items*50/2 #might change.
    R = 1.0 #might change

    random_tour = list(range(1, num_cities))  # Exclude starting city (0) for shuffling
    random.shuffle(random_tour)
    random_tour = [0] + random_tour + [0]  # Ensure tour starts and ends at city 0
    random_packing_list = random.sample(range(num_items), num_items)
    OB_value = objective_function(random_tour, random_packing_list, items, distances, vmax, vmin, W, R)
    return random_tour, random_packing_list, OB_value
 

def process_ttp_instances_results(input_folder, output_file,iteration):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as f:
                ttp = json.load(f)
            start_time = time.time()    
            random_tour, random_packing_list, OB_value = random_tour_and_packing(ttp)
            end_time = time.time()
            computing_time = end_time - start_time
            results.append({
                'filename': filename,
                'Iteration': iteration,
                'random_tour': random_tour,
                'random_packing_list':random_packing_list,
                'OB_value': OB_value ,
                'computing_time': computing_time
            })
    save_to_json(results, output_file)

os.makedirs('tour_results', exist_ok=True)

for cities in range(20, 120, 20):
    for n in range (1,5,1):     
        items=n*cities          
        input_folder = f'json_files_TTP_instances_{cities}_items_{items}'

# Process the TTP instances and save results
        output_file = f'tour_results/results_random_cities_{cities}_items{items}.json'
        process_ttp_instances_results(input_folder, output_file,1)

        print(f"Results saved to {output_file}")

