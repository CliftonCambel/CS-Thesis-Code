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


def simulated_annealing_hybrid(ttp, random_sample, iterations, initial_temperature=10000, cooling_rate=0.99):
    cities = ttp['cities']
    items = ttp['items']
    distances = ttp['distances']
    num_cities = len(cities)
    num_items = len(items)
    packinglist = random_sample['random_actual_packing_list']
    total_weight_ttp_instance = sum(item['weight'] for item in items)

    Tr = 0.25  # Tightness ratio interval [0,1], suggested 0.25,0.5,0.75
    W = round(Tr * total_weight_ttp_instance)  # Example formula, may be adjusted
    vmax = 1.0
    vmin = 0.1
    R = 1.0

    best_tour = random_sample['random_tour']
    best_fitness = random_sample['OB_value']
    current_tour = best_tour[:]
    current_packinglist = packinglist[:]
    current_fitness = best_fitness

    if not isinstance(best_tour, list):
        raise ValueError("Expected `random_tour` to be a list, but got an integer or other non-iterable object.")

    # Ensure the initial tour starts and ends at node 0
    if best_tour[0] != 0 or best_tour[-1] != 0:
        best_tour = [0] + [city for city in best_tour if city != 0] + [0]

    temperature = initial_temperature

    for iteration in range(iterations):
        # Generate a neighboring solution by swapping two cities
        new_tour = current_tour[:]
        if num_cities > 2:  # Ensure there's enough to swap
            i, j = random.sample(range(1, num_cities - 1), 2)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        # Generate a neighboring solution by changing the knapsack content
        new_packinglist = current_packinglist[:]
        random_item_id = random.randint(0, num_items - 1)
        random_item = [item for item in items if item['id'] == random_item_id]

        if random_item_id not in new_packinglist and random_item and \
           sum(item['weight'] for item in new_packinglist) + random_item[0]['weight'] <= W:
            new_packinglist.append(random_item_id)
        elif new_packinglist:
            new_packinglist.remove(random.choice(new_packinglist))

        # Evaluate the new solution
        new_fitness, _, _ = TTP_random_tour_and_packing_list.objective_function(
            new_tour, new_packinglist, items, distances, vmax, vmin, W, R
        )

        # Calculate change in fitness
        delta_fitness = new_fitness - current_fitness

        # Accept the new solution probabilistically
        if delta_fitness > 0 or random.random() < math.exp(delta_fitness / temperature):
            current_tour = new_tour
            current_packinglist = new_packinglist
            current_fitness = new_fitness

        # Update the best solution found
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_tour = current_tour[:]
            best_knapsack = current_packinglist[:]

        # Decrease the temperature
        temperature *= cooling_rate

        # Optional: Stop early if the temperature is very low
        if temperature < 1e-3:
            break

    return best_tour, best_knapsack, best_fitness
