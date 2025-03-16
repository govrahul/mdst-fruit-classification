import os

def get_directories(directory):
    """
    Retrieve all subdirectories (fruit names) within our test/training file
    """
    try:
        # Get the fruit names:
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        
        # Sort alphabetically
        subdirs.sort()
        
        # Create dictionary with numerical keys (to match up to your predicted index)
        subdir_dict = {i: subdirs[i] for i in range(len(subdirs))}
        
        return subdir_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}

# TODO: Replace "Training" with the path to your training directory
directory_path = "Training"
dict = get_directories(directory_path)
print(dict)
