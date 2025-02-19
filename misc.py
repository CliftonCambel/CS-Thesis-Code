import os
import shutil
from math import ceil

def split_json_files(source_dir, target_dir_base):
    # Ensure source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Get all JSON files in the source directory
    json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]

    # Check if there are 1000 files
    total_files = len(json_files)
    if total_files != 1000:
        print(f"Source directory contains {total_files} JSON files, not 1000.")
        return

    # Determine the number of files per directory
    files_per_dir = ceil(total_files / 4)

    # Create target directories and distribute files
    for i in range(4):
        target_dir = f"{target_dir_base}_{i + 1}"
        os.makedirs(target_dir, exist_ok=True)
        
        start_idx = i * files_per_dir
        end_idx = start_idx + files_per_dir

        for json_file in json_files[start_idx:end_idx]:
            source_file = os.path.join(source_dir, json_file)
            target_file = os.path.join(target_dir, json_file)
            shutil.copy(source_file, target_file)

        print(f"Copied files to {target_dir}")

    print("All files have been successfully split into 4 directories.")

# Example usage
if __name__ == "__main__":
    name_directory = "problem_instances_ttp_100c"
    os.makedirs(name_directory, exist_ok=True)

    source_directory = "problem_instances_ttp/json_files_TTP_instances_100_items_100"  # Replace with your base target directory path
    target_directory_base = f'{name_directory}/json_files_TTP_instances_100_items_100'

    split_json_files(source_directory, target_directory_base)

    source_directory = "problem_instances_ttp/json_files_TTP_instances_100_items_200"  # Replace with your base target directory path
    target_directory_base = f'{name_directory}/json_files_TTP_instances_100_items_200'

    split_json_files(source_directory, target_directory_base)

    source_directory = "problem_instances_ttp/json_files_TTP_instances_100_items_300"  # Replace with your base target directory path
    target_directory_base = f'{name_directory}/json_files_TTP_instances_100_items_300'

    split_json_files(source_directory, target_directory_base)

    source_directory = "problem_instances_ttp/json_files_TTP_instances_100_items_400"  # Replace with your base target directory path
    target_directory_base = f'{name_directory}/json_files_TTP_instances_100_items_400'

    split_json_files(source_directory, target_directory_base)