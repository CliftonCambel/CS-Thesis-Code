import json
import random
import math
import os
import matplotlib.pyplot as plt

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def objective_function(tour, items, distances, vmax, vmin, W, R):
    total_value = 0
    total_weight = 0
    total_distance = 0
    for i in range(len(tour)):
        current_city = tour[i]
        next_city = tour[(i + 1) % len(tour)]
        total_distance += distances[current_city][next_city]
        for item in items:
            if item['city'] == current_city:
                total_value += item['value']
                total_weight += item['weight']
    speed = vmax - (vmax - vmin) * (total_weight / W)
    travel_time = total_distance / speed
    cost = travel_time * R
    return total_value - cost

def hillclimber_ttp(ttp, iterations):
    cities = ttp['cities']
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    
    vmax = 1.0
    vmin = 0.1
    W = 500 
    R = 1.0

    # Initial random tour
    best_tour = list(range(num_cities))
    random.shuffle(best_tour)
    best_value = objective_function(best_tour, items, distances, vmax, vmin, W, R)

    for _ in range(iterations):
        # Generate a new tour by swapping two cities
        new_tour = best_tour[:]
        i, j = random.sample(range(num_cities), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_value = objective_function(new_tour, items, distances, vmax, vmin, W, R)
        
        if new_value > best_value:
            best_tour, best_value = new_tour, new_value

    return best_tour, best_value

# Read TTP instances from JSON files and save results
def process_ttp_instances(input_folder, output_file, iterations):
    results = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as f:
                ttp = json.load(f)
            best_tour, best_value = hillclimber_ttp(ttp, iterations)
            results.append({
                'filename': filename,
                'best_tour': best_tour,
                'best_value': best_value
            })
    save_to_json(results, output_file)


iterations = 1000

input_folder = 'json_files'

# Process the TTP instances and save results
output_file = 'results.json'
process_ttp_instances(input_folder, output_file, iterations)

print(f"Results saved to {output_file}")