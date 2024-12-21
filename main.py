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
    
    while True:
        print("\nOptions:")
        print("1. Enter a New Product")
        print("2. Search for a Product")
        print("3. Exit Menu")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            ProductId = input("Enter Product ID: ")
            ProductName = input("Enter Product Name: ")
            Category = input("Enter Category: ")
            Quantity = input("Quantity: ")
            
            try:
                new_record = {
                    "ProductID": int(ProductId), 
                    "ProductName": ProductName, 
                    "Category": Category, 
                    "Quantity": int(Quantity)
                }
                print(new_record)
                eh.insert(new_record)
                print("Product added successfully.")
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")
            
        elif choice == "2":
            try:
                product_id_to_search = int(input("Enter ProductID to search: "))
                eh.search_and_modify(product_id_to_search)
            except ValueError:
                print("Invalid ProductID format. Please enter a valid number.")
            
        elif choice == "3":
            print("Exiting menu. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
