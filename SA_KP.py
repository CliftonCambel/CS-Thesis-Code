import random
import TTP_random_tour_and_packing_list
import Iteration_search
import os
import time
import Hillclimber_TSP_swaping
from multiprocessing import Pool, cpu_count
import logging
from tqdm import tqdm
from functools import partial


import math

def simulated_annealing_KP(ttp, random_sample, iterations, initial_temperature=1000, cooling_rate=0.99):
    #cities = ttp['cities']
    items = ttp['items']
    item_dict = {item['id']: item for item in items}  # Precompute item lookup
    distances = ttp['distances']
    num_items = len(items)
    packinglist = random_sample['random_actual_packing_list']
    total_weight_ttp_instance = sum(item['weight'] for item in items)

    Tr = 0.25
    W = round(Tr * total_weight_ttp_instance)
    vmax, vmin, R = 1.0, 0.1, 1.0

    best_tour = random_sample['random_tour']
    best_fitness = random_sample['OB_value']
    current_tour = best_tour[:]
    current_packinglist = packinglist[:]
    current_fitness = best_fitness

    temperature = initial_temperature

    for _ in range(iterations):
        # Generate a neighboring solution
        new_packinglist = current_packinglist[:]
        random_item_id = random.randint(0, num_items - 1)
        random_item = item_dict.get(random_item_id)

        if random_item and random_item_id not in new_packinglist and sum(item['weight'] for item in items) + random_item['weight'] <= W:
            new_packinglist.append(random_item_id)
        elif new_packinglist:
            new_packinglist.remove(random.choice(new_packinglist))

        # Evaluate the new solution
        new_fitness, _, _ = TTP_random_tour_and_packing_list.objective_function(
            current_tour, new_packinglist, items, distances, vmax, vmin, W, R
        )

        # Calculate change in fitness
        delta_fitness = new_fitness - current_fitness

        # Accept the new solution probabilistically
        if delta_fitness > 0 or random.random() < math.exp(delta_fitness / temperature):
            current_packinglist = new_packinglist
            current_fitness = new_fitness

        # Update the best solution
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_tour = current_tour[:]
            best_knapsack = current_packinglist[:]

        # Update temperature
        temperature *= cooling_rate

        # Optional: Stop if the temperature is too low
        if temperature < 1e-3:
            break

    return best_tour, best_knapsack, best_fitness

