import random
import numpy as np
import TTP_random_tour_and_packing_list
import Hillclimber_TSP_swaping

def initialize_pheromone(ttp):
    num_cities = len(ttp['cities'])
    
    num_items = len(ttp['items'])
    pheromone_cities = np.ones((num_cities, num_cities))
    #print(pheromone_cities)
    pheromone_items = np.ones(num_items)
    #print(pheromone_items)
    return pheromone_cities, pheromone_items

def calculate_probabilities(current_city, visited_cities, pheromone_matrix, distances, alpha, beta):
    probabilities = []
    num_cities = len(pheromone_matrix)
    #print(f"Current City: {current_city}")
    #print(f"Visited Cities: {visited_cities}")
    #print(f"Pheromone Matrix: {pheromone_matrix}")
    #print(f"Distances: {distances}")
    #print(f"Alpha: {alpha}, Beta: {beta}")
    for city in range(num_cities):
        if city not in visited_cities:
            pheromone = pheromone_matrix[current_city][city] ** alpha
            distance = 1 / (distances[current_city][city] + 1e-5) ** beta  # Avoid division by zero
            probabilities.append(pheromone * distance)
        else:
            probabilities.append(0)  # Already visited cities get 0 probability
    
    total = sum(probabilities)
    if total <= 0:
        # If total is zero or negative, fallback to uniform probabilities for unvisited cities
        probabilities = [1 if city not in visited_cities else 0 for city in range(num_cities)]
        total = sum(probabilities)
    
    return [p / total for p in probabilities]

def construct_solution(ttp, W ,pheromone_cities, pheromone_items, alpha, beta):
    city_ids = [city['id'] for city in ttp['cities']]
    tour = [0]  # Start at city 0
    while len(tour) < len(city_ids):
        current_city = tour[-1]
        probabilities = calculate_probabilities(
            current_city, tour, pheromone_cities, ttp['distances'], alpha, beta
        )
        #print(f"Probabilities: {probabilities}")
        next_city = np.random.choice(city_ids, p=probabilities)
        tour.append(next_city)
    tour.append(0)  # End the tour at city 

    packing_list = []
    remaining_capacity = W
    for item in ttp['items']:
        # Check if the item's city is in the tour and if it fits in the remaining capacity
        if item['city'] in tour and remaining_capacity >= item['weight']:
            prob = pheromone_items[item['id']] ** alpha
            if random.random() < prob:
                packing_list.append(item['id'])
                remaining_capacity -= item['weight']

    return tour, packing_list


def update_pheromones(pheromone_cities, pheromone_items, solutions, evaporation_rate, q):
    # Evaporate pheromones (apply decay)
    pheromone_cities *= (1 - evaporation_rate)
    pheromone_items *= (1 - evaporation_rate)

    # Ensure non-negative values after evaporation
    pheromone_cities = np.maximum(pheromone_cities, 1e-5)
    pheromone_items = np.maximum(pheromone_items, 1e-5)

    # Deposit pheromones based on solutions
    for tour, packing_list, fitness in solutions:
        if fitness > 0:  # Only deposit pheromones for positive fitness
            # Update pheromones for cities
            for i in range(len(tour) - 1):
                pheromone_cities[tour[i]][tour[i + 1]] += q * fitness

            # Update pheromones for items
            for item in packing_list:
                pheromone_items[item] += q * fitness

    # Optional: Clamp pheromone levels to prevent extremes
    pheromone_cities = np.clip(pheromone_cities, 1e-5, 100)  # Adjust upper bound as needed
    pheromone_items = np.clip(pheromone_items, 1e-5, 100)    # Adjust upper bound as needed

    return pheromone_cities, pheromone_items


def ant_colony_optimization(ttp, num_ants, alpha, beta, evaporation_rate, q, iterations):
    pheromone_cities, pheromone_items = initialize_pheromone(ttp)
    best_tour, best_packing_list, best_fitness = None, None, float('-inf')
    items = ttp['items']
    total_weight_ttp_instance = sum(item['weight'] for item in items)
    Tr = 0.25  # Tightness ratio interval [0,1], suggested 0.25,0.5,0.75
    W = round(Tr * total_weight_ttp_instance)
    distances = ttp['distances']
    vmax=1 
    vmin=0.1
    R=1
    for _ in range(iterations):
        solutions = []
        for _ in range(num_ants):
            tour, packing_list = construct_solution(ttp, W,pheromone_cities, pheromone_items, alpha, beta)
            fitness,_,_ =TTP_random_tour_and_packing_list.objective_function(tour, packing_list, items, distances, vmax, vmin, W, R)
            solutions.append((tour, packing_list, fitness))
            if fitness > best_fitness:
                best_fitness = fitness
                best_tour = tour
                best_packing_list = packing_list
        
        update_pheromones(pheromone_cities, pheromone_items, solutions, evaporation_rate, q)

    return best_tour, best_packing_list, best_fitness

if __name__ == "__main__":

    # Example usage
    ttp = Hillclimber_TSP_swaping.load_json('problem_instances_ttp/json_files_TTP_instances_20_items_20/traveling_thief_problem_cities_20_items_20_1.json')
    #C:\Users\ccroo\OneDrive\Bureaublad\CS-Thesis-Code\problem_instances_ttp\json_files_TTP_instances_20_items_20\traveling_thief_problem_cities_20_items_20_1.json
    best_tour, best_packing_list, best_fitness = ant_colony_optimization(
        ttp, num_ants=40, alpha=1, beta=2, evaporation_rate=0.5, q=100, iterations=100
    )

    print(f"Best Tour: {best_tour}")
    print(f"Best Packing List: {best_packing_list}")
    print(f"Best Fitness: {best_fitness}")