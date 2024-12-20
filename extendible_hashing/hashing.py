from .bucket import Bucket
class ExtendibleHashingOptimized:
    def __init__(self, bucket_capacity):
        self.global_depth = 1  # Moderate starting global depth
        self.bucket_capacity = bucket_capacity
        self.directory = [Bucket(self.bucket_capacity, 1) for _ in range(2 ** self.global_depth)]

    def hash_key(self, key):
        """Compute a compact hash value of the key."""
        return bin(hash(key) & ((1 << self.global_depth) - 1))[2:].zfill(self.global_depth)  # Binary string

    def get_index(self, hash_value):
        """Get the directory index using the global depth."""
        return int(hash_value[:self.global_depth], 2)

    def insert(self, record):
        key = record["ProductID"]
        hash_value = self.hash_key(key)
        index = self.get_index(hash_value)
        bucket = self.directory[index]
    
        #print(f"Inserting {record} -> Hash: {hash_value}, Index: {index}")
    
        if bucket.is_full():
            #print(f"Bucket at index {index} is full. Splitting...")
            self.split_bucket(index)
            self.insert(record)  # Reinsert the record after splitting
        else:
            bucket.add_record(record)
            #print(f"Added record to Bucket {index}. Current Records: {bucket.records}")
    
    def split_bucket(self, index):
        old_bucket = self.directory[index]
        old_local_depth = old_bucket.local_depth
    
        # Case 1: Local Depth equals Global Depth
        if old_local_depth == self.global_depth:
            self.double_directory()
    
        # Increment the local depth of the bucket
        old_bucket.local_depth += 1
    
        # Create a new bucket with the same capacity
        new_bucket = Bucket(self.bucket_capacity, old_bucket.local_depth)
        split_bit = 1 << (old_bucket.local_depth - 1)
    
        # Update directory to point to the new bucket where needed
        for i in range(len(self.directory)):
            if (i & split_bit) == split_bit and self.directory[i] == old_bucket:
                self.directory[i] = new_bucket
    
        # Redistribute records between the old and new buckets
        records_to_redistribute = old_bucket.records[:]
        old_bucket.records.clear()
    
        for record in records_to_redistribute:
            record_hash = self.hash_key(record["ProductID"])
            record_index = self.get_index(record_hash)
            self.directory[record_index].add_record(record)

    def double_directory(self):
        """Expand the directory when global depth increases."""
        size = len(self.directory)
        self.directory += [None] * size  # Double the directory size
    
        # Copy existing bucket pointers
        for i in range(size):
            self.directory[i + size] = self.directory[i]
    
        # Increment global depth
        self.global_depth += 1


    def reassign_records(self, index):
        """Reassign records between the old and new bucket."""
        old_bucket = self.directory[index]
        records = old_bucket.records[:]
        old_bucket.records.clear()
        for record in records:
            self.insert(record)

    def calculate_load_factor(self):
        """Calculate and return the load factor of the hash table."""
        total_records = sum(len(bucket.records) for bucket in self.directory if bucket is not None)
        #print("total records:",total_records)
        total_buckets = len(self.directory)
        #print("total directories:",total_buckets)
        load_factor = total_records / total_buckets
        return load_factor
        

    def search_and_modify(self, product_id):
        """Search for a record by ProductID and allow Update/Delete operations."""
        hash_value = self.hash_key(product_id)
        index = self.get_index(hash_value)
        bucket = self.directory[index]
        
        for record in bucket.records:
            if record["ProductID"] == product_id:
                print(f"Product found: {record}")
                while True:
                    print("\nOptions:")
                    print("1. Update Product")
                    print("2. Delete Product")
                    print("3. Exit Menu")
                    choice = input("Enter your choice (1/2/3): ")
                    
                    if choice == "1":
                        self.update_record(record)
                        return
                    elif choice == "2":
                        self.delete_record(bucket, record)
                        return
                    elif choice == "3":
                        print("Exiting menu.")
                        return
                    else:
                        print("Invalid choice. Please try again.")
        print("Product not found.")

    def update_record(self, record):
        """Update the details of a record."""
        print("Enter new details for the product (leave blank to keep existing value):")
        new_name = input(f"Product Name [{record['ProductName']}]: ") or record["ProductName"]
        new_category = input(f"Category [{record['Category']}]: ") or record["Category"]
        new_quantity = input(f"Quantity [{record['Quantity']}]: ") or record["Quantity"]
        
        # Update the record
        record["ProductName"] = new_name
        record["Category"] = new_category
        try:
            record["Quantity"] = int(new_quantity)
        except ValueError:
            print("Invalid quantity. Keeping existing value.")
        
        print(f"Product updated successfully: {record}")

    def delete_record(self, bucket, record):
        """Delete a record from the bucket."""
        bucket.records.remove(record)
        print(f"Product with ProductID {record['ProductID']} deleted successfully.")


    def display(self):
        """Display the directory and buckets."""
        print(f"Global Depth: {self.global_depth}")
        for i, bucket in enumerate(self.directory):
            # if bucket is not None:
                print(f"Directory[{i}]: Local Depth={bucket.local_depth}, Records={bucket.records}")
