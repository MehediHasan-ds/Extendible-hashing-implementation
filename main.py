import json
from extendible_hashing.hashing import ExtendibleHashingOptimized

def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    # Initialize
    bucket_capacity = 3
    eh = ExtendibleHashingOptimized(bucket_capacity)

    # Load input data
    data = load_data("data/demo_input.json")

    # Insert records
    for record in data:
        eh.insert(record)

    # Search for a record
    product_id_to_search = 505
    result = eh.search(product_id_to_search)
    print("Search Result:", result)
