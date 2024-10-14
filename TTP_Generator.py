import json
import random
import math
import matplotlib.pyplot as plt
import os
import numpy as np

def generate_tsp(num_cities):
    cities = []
    for i in range(num_cities):
        x, y = random.randint(0, 100), random.randint(0, 100)
        cities.append((x, y))
    return cities

def euclidean_distance(city1, city2):
    return round(math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2))            #should I round it up?

def generate_items(num_cities, num_items):
    items = []
    for _ in range(num_items):
        city_index = random.randint(1, num_cities - 1)
        weight = random.randint(1, 1000)                                                    #might change again
        random_number = random.uniform(0, 1)
        value = weight+500*random_number                                                    #might change this again
        items.append((city_index, value, weight))
    return items

def generate_ttp(num_cities, num_items):
    cities = generate_tsp(num_cities)
    items = generate_items(num_cities, num_items)
    
    distance_matrix = [[0]*num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = euclidean_distance(cities[i], cities[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    
    ttp = {
        "cities": [{"id": i, "coordinates": cities[i]} for i in range(num_cities)],
        "items": [{"id": i, "city": item[0], "value": item[1], "weight": item[2]} for i, item in enumerate(items)],
        "distances": distance_matrix
    }
    return ttp

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Parameters for the problem
#num_cities = 20
#num_items = 20

# Generate TTP and save to JSON
#ttp_data = generate_ttp(num_cities, num_items)
#save_to_json(ttp_data, 'traveling_thief_problem.json')

def plot_tsp_matrix_and_items(cities, distance_matrix, items, filename):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 30))

    # Plot the cities and items on the first subplot
    for i, city in enumerate(cities):
        ax1.scatter(city[0], city[1], c='blue')
        city_items = [item for item in items if item["city"] == i]
        item_info = "\n".join([f'Item: {item["id"]} ({item["value"]},{item["weight"]})' for item in city_items])
        ax1.text(city[0], city[1], f'{i}\n{item_info}', fontsize=10, ha='right', va='bottom', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            if distance_matrix[i][j] > 0:
                ax1.plot([cities[i][0], cities[j][0]], [cities[i][1], cities[j][1]], 'k-', alpha=0.3)
                mid_x = (cities[i][0] + cities[j][0]) / 2
                mid_y = (cities[i][1] + cities[j][1]) / 2
                ax1.text(mid_x, mid_y, f'{distance_matrix[i][j]}', fontsize=8, ha='center', va='center', bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))

    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.set_title('Traveling Thief Problem')
    ax1.grid(True)

    # Create the distance matrix on the second subplot
    ax2.axis('tight')
    ax2.axis('off')
    table = ax2.table(cellText=np.round(distance_matrix, 2),
                      colLabels=[f'City {i}' for i in range(len(cities))],
                      rowLabels=[f'City {i}' for i in range(len(cities))],
                      cellLoc='center',
                      loc='center')
    table.scale(1, 2)
    ax2.set_title('Distance Matrix')

    # Create the item information table on the third subplot
    items_data = [[item["id"], item["value"], item["weight"], item["city"]] for item in items]
    items_columns = ["ID", "Value", "Weight", "City"]
    
    ax3.axis('tight')
    ax3.axis('off')
    item_table = ax3.table(cellText=items_data,
                           colLabels=items_columns,
                           cellLoc='center',
                           loc='center')
    item_table.scale(1, 2)
    ax3.set_title('Items Information')

    plt.savefig(filename)
    plt.close()

def plot_matrix_and_items2(distance_matrix, items, filename):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 20))

    # Create the distance matrix on the first subplot
    ax1.axis('tight')
    ax1.axis('off')
    table = ax1.table(cellText=np.round(distance_matrix, 2),
                      colLabels=[f'City {i}' for i in range(len(distance_matrix))],
                      rowLabels=[f'City {i}' for i in range(len(distance_matrix))],
                      cellLoc='center',
                      loc='center')
    table.scale(1, 2)
    ax1.set_title('Distance Matrix')

    # Create the item information table on the second subplot
    items_data = [[item["id"], item["value"], item["weight"], item["city"]] for item in items]
    items_columns = ["ID", "Value", "Weight", "City"]
    
    ax2.axis('tight')
    ax2.axis('off')
    item_table = ax2.table(cellText=items_data,
                           colLabels=items_columns,
                           cellLoc='center',
                           loc='center')
    item_table.scale(1, 2)
    ax2.set_title('Items Information')

    plt.savefig(filename)
    plt.close()

# Ensure directories exist
#name_directory = f'json_files_TTP_{num_cities}_items_{num_items}'
#os.makedirs('json_files', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Run 1000 iterations
def TTP_Instances(num_cities,num_items):
    name_directory = f'json_files_TTP_instances_{num_cities}_items_{num_items}'
    os.makedirs(name_directory, exist_ok=True)
    for iteration in range(1000):
    # Generate TTP
        ttp_data = generate_ttp(num_cities, num_items)
    
    # Save to JSON
        json_filename = f'{name_directory}/traveling_thief_problem_cities_{num_cities}_items_{num_items}_{iteration + 1}.json'
        save_to_json(ttp_data, json_filename)
    
    # Plot the TSP and save the graph
    #image_filename = f'images/traveling_thief_problem_{num_cities}_{num_items}_{iteration + 1}.png'
    #plot_tsp_matrix_and_items([city["coordinates"] for city in ttp_data["cities"]], ttp_data["distances"], ttp_data["items"], image_filename)
    #plot_matrix_and_items2(ttp_data["distances"],ttp_data["items"],image_filename)
    print(f"Iteration {iteration + 1}: Saved JSON")

    print("Completed 1000 iterations for ",num_cities," cities and ",num_items, " items")

#the number of cities is can be changed by changing the start, end and step values of the first range function ,
# and the second the n multiplier of amount of items. 
for cities in range(20, 120, 20):
    for n in range (1,5,1):     
        items=n*cities          
        TTP_Instances(cities,items)









#print("Traveling Thief Problem saved to traveling_thief_problem.json")
