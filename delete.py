import os
import shutil

# Paths to your directories
first_directory = "Test"
second_directory = "Training"

# Get lists of subdirectories in both directories
first_subdirs = set(os.listdir(first_directory))
second_subdirs = set(os.listdir(second_directory))

# Find directories in the second directory that aren't in the first
directories_to_delete = second_subdirs - first_subdirs

# Delete those directories
for dir_name in directories_to_delete:
    dir_path = os.path.join(second_directory, dir_name)
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print(f"Deleted: {dir_path}")
    else:
        print(f"Skipped (not a directory): {dir_path}")
