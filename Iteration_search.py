import os
import json
import TTP_random_tour_and_packing_list

def load_iteration_results(input_folder):
    all_results = []

    # Loop through all JSON files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as f:
                results = json.load(f)
                all_results.extend(results)  # Add all results from this file to the main list
    
    return all_results

def get_best_ob_value_from_existing_files(all_results):
    best_results = {}

    # Iterate over all the results collected from the JSON files
    for result in all_results:
        filename = result['problem_instance_filename']
        current_ob_value = result['OB_value']

        # Check if this is the best OB value so far for this problem instance
        if (filename not in best_results or 
            current_ob_value > best_results[filename]['OB_value']):
            best_results[filename] = result  # Store only the best result

    return best_results

def get_lowest_ob_value_from_existing_files(all_results):
    lowest_results = {}

    # Iterate over all the results collected from the JSON files
    for result in all_results:
        filename = result['problem_instance_filename']
        current_ob_value = result['OB_value']

        # Check if this is the lowest OB value so far for this problem instance
        if (filename not in lowest_results or 
            current_ob_value < lowest_results[filename]['OB_value']):
            lowest_results[filename] = result  # Store only the lowest result

    return lowest_results

def save_best_results_to_json(best_results, output_file):
    # Convert dictionary to a list of best results
    best_results_list = list(best_results.values())

    with open(output_file, 'w') as f:
        json.dump(best_results_list, f, indent=4)

if __name__ == "__main__":
    name_directory = f'tour_results/best_random_results'
    os.makedirs(name_directory, exist_ok=True)
    for cities in range(20, 120, 20):
        for n in range(1, 5):
            items = n * cities
            input_folder = f'tour_results/random_results/TTP_instances_{cities}_items_{items}'
            #input_folder = 'name_directory'  # Folder where iteration results are stored
            output_file = f'tour_results/best_random_results/best_random_results_cities_{cities}_items_{items}.json'

            # Step 1: Load all iteration results from the saved JSON files
            all_results = load_iteration_results(input_folder)

            # Step 2: Find the best OB value for each problem instance
            best_results = get_best_ob_value_from_existing_files(all_results)

            # Step 3: Save only the best OB values to a new JSON file
            save_best_results_to_json(best_results, output_file)

            print(f"Best OB values saved to {output_file}")