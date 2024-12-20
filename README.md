# Extendible Hashing Optimized

## Table of Contents

1. [Report](#project-report)
2. [Installation and Setup](#installation-and-setup)
3. [File Structure](#file-structure)
4. [How to Run](#how-to-run)
 
---

## Report

### 1. Complex Use Case Scenario

#### Inventory Management System for a Warehouse

In a large-scale warehouse handling thousands of products across multiple categories, ensuring efficient storage and retrieval of product data is crucial. The challenge lies in maintaining optimal storage utilization while allowing for rapid search, update, and insertion of records. The system must be scalable to accommodate significant increases in data volume over time.

A traditional hash table approach fails in this scenario due to fixed-size buckets, leading to frequent overflow and inefficient data handling. Dynamic resizing techniques like extendible hashing provide a better alternative.

### 2. Requirement Analysis

#### Functional Requirements:
- **Insertion:** Efficiently add new product records.
- **Search:** Quickly retrieve product details using the ProductID.
- **Load Factor Management:** Maintain a balanced load factor to optimize memory usage.
- **Scalability:** Dynamically adjust to accommodate growing data.

#### Non-Functional Requirements:
- **Performance:** Ensure low latency for operations.
- **Data Integrity:** Prevent loss of records during operations like bucket splitting.
- **Ease of Use:** Provide clear methods to interact with the hash table.

#### Constraints:
- Fixed bucket capacity.
- Limited initial memory allocation to simulate a real-world constraint.

### 3. Plan to Solve the Use Case Scenario

#### Solution: Extendible Hashing

Extendible Hashing dynamically adjusts the hash table size using a directory and local/global depth mechanisms. This approach minimizes collisions and reduces memory wastage by splitting buckets only when needed.

#### Why This Plan Is Better:
- **Scalability:** Only affected buckets are split, reducing unnecessary memory usage.
- **Dynamic Resizing:** The directory doubles in size only when global depth increases, unlike traditional approaches that require complete rehashing.
- **Efficient Load Management:** Load factor is automatically balanced by redistributing records during bucket splits.

### 4. Step-by-Step Solution

#### Step 1: Initialize the Hash Table
- Define a directory with a global depth of 1 and buckets with a fixed capacity.

#### Step 2: Insert Records
- Hash the ProductID to compute an index.
- Add the record to the corresponding bucket.
- If the bucket is full, split it and redistribute the records.

#### Step 3: Handle Bucket Splitting
- Increment the local depth of the bucket.
- Create a new bucket and update the directory pointers.
- Redistribute the records based on updated hashes.

#### Step 4: Expand Directory
- If a bucket’s local depth exceeds the global depth, double the directory size.
- Copy existing pointers to the new directory slots.

#### Step 5: Search for a Record
- Compute the hash of the ProductID and locate the bucket using the directory.
- Retrieve the record from the bucket.

#### Step 6: Monitor Load Factor
- Calculate the ratio of total records to total buckets.

### 5. Optimization Using OOP and Data Structures

#### Object-Oriented Programming (OOP):
- **Encapsulation:** The `Bucket` and `ExtendibleHashingOptimized` classes encapsulate data and methods, ensuring modularity.
- **Inheritance:** Extend the base classes to introduce specialized behaviors for different scenarios.
- **Polymorphism:** Use method overriding to customize bucket behaviors if needed.

#### Data Structure Optimization:
- **Dynamic Directory:** The directory is implemented as a list, allowing efficient doubling and indexing.
- **Buckets:** Use lists to manage records, ensuring O(1) insertion and retrieval.
- **Hashing:** Optimize the hash function for uniform distribution of keys.

---
**Here I will explain only ExtendibleHashingOptimized Class as it is the main part of this solution**
# ExtendibleHashingOptimized Class

The `ExtendibleHashingOptimized` class implements an efficient dynamic hashing algorithm called **Extendible Hashing**. This algorithm is designed to handle data growth by dynamically splitting buckets and expanding the directory as needed, ensuring efficient storage and retrieval of records.

This implementation is particularly useful for database systems or applications with unpredictable data size and ensures minimal collisions and optimal performance.

---

- **Dynamic Growth**: Automatically grows the hash table by splitting buckets and expanding the directory when full.
- **Efficient Data Access**: Uses hash values to map records to specific buckets, allowing fast insertion and search operations.
- **Load Balancing**: Redistributes records during bucket splits to maintain even data distribution, preventing performance issues from overfull buckets.

---

## Key Methods

### 1. `__init__(self, bucket_capacity)`
Initializes the hash table with the following:
- **`global_depth`**: The number of bits used for hashing, starting at 1.
- **`bucket_capacity`**: The maximum number of records a bucket can hold.
- **`directory`**: An initial list of buckets, with the size determined by `2^global_depth`.

---

### 2. `hash_key(self, key)`
Generates a binary hash value for a given key:
- Uses Python’s `hash()` function and the current `global_depth` to determine the number of bits in the hash.
- Ensures that hash values are compact and suitable for dynamic growth.

---

### 3. `get_index(self, hash_value)`
Converts the binary hash value into a directory index by extracting the first `global_depth` bits. This index identifies the bucket where the record should be placed.

---

### 4. `insert(self, record)`
Handles the insertion of new records into the hash table.

#### Process:
1. Computes the hash value for the `ProductID` in the record.
2. Finds the directory index corresponding to the hash value.
3. If the target bucket has space, the record is added directly.
4. If the bucket is full:
   - Calls the `split_bucket()` method to create a new bucket and redistribute records.
   - Reinserts the current record into the updated structure.

This method ensures that no record is lost during bucket splits.

---

### 5. `split_bucket(self, index)`
The `split_bucket` method is the most critical part of the dynamic hashing mechanism. It handles bucket overflows by splitting full buckets and redistributing records.

#### Detailed Explanation:

1. **Identify the Full Bucket**:
   - Locate the bucket at the given `index` in the directory.
   - Store its current `local_depth` (the number of bits this bucket uses for hashing).

2. **Check Depths**:
   - If the bucket’s `local_depth` equals the `global_depth`, the directory must be expanded by calling `double_directory()`.

3. **Increase Local Depth**:
   - Increment the `local_depth` of the full bucket to indicate it now uses one more bit for hashing.

4. **Create a New Bucket**:
   - A new bucket is created with the same capacity as the full bucket.
   - This bucket will hold records that differ from the full bucket in the bit corresponding to the new `local_depth`.

5. **Update Directory**:
   - Identify which directory indices should point to the new bucket based on the updated hash values.
   - Update the directory to reflect this split.

6. **Redistribute Records**:
   - Move all records from the full bucket into their correct buckets (either the original or the new bucket) by recalculating their hash values and indices.
   - Clear the full bucket before redistributing to avoid duplicate records.

#### Why Redistribute Records?
When a bucket is split, the additional bit in the `local_depth` determines which bucket each record should go into. Redistributing records ensures that the hash table maintains its structural integrity and efficiency.

#### Example of Splitting:
- Assume a bucket has `local_depth = 2` and holds records that hash to `00` and `10`.
- After splitting, `local_depth` becomes `3`.
- Records with hash `000` and `001` stay in the original bucket, while records with `010` and `011` move to the new bucket.

This method ensures that the hash table dynamically adjusts to growing data without requiring manual resizing.

---

### 6. `double_directory(self)`
When all buckets in the directory are full, the directory size needs to be doubled to accommodate new buckets.

#### Process:
1. The directory size is doubled by copying the existing structure.
2. For each bucket in the original directory, add a duplicate entry to the new slots.
3. Increment the `global_depth` to reflect the increased number of bits used for hashing.

This method ensures that the hash table can handle more buckets and supports future splits.

---

### 7. `calculate_load_factor(self)`
Computes the load factor, which is the ratio of total records to the total number of buckets. A high load factor indicates efficient bucket usage, while a low value suggests underutilization.

---

### 8. `search(self, product_id)`
Searches for a record based on its `ProductID`.

#### Steps:
1. Calculates the hash value and identifies the corresponding bucket.
2. Scans the bucket for a matching `ProductID`.
3. Returns the record if found; otherwise, returns `None`.

---

### 9. `display(self)`
Prints the current structure of the hash table, including:
- **Global Depth**
- Each bucket’s **Local Depth** and stored records.

This is useful for debugging and understanding the internal state of the hash table.

---

## Why Extendible Hashing?

Extendible hashing ensures:
1. **Scalability**: The hash table grows dynamically as data increases.
2. **Collision Handling**: Splits buckets instead of resizing the entire table, minimizing disruptions.
3. **Resource Efficiency**: Uses memory only when needed, unlike traditional hash tables with fixed sizes.

---

## Dynamic Behavior

- **Bucket Overflow**: Triggers the `split_bucket()` method, which may also trigger `double_directory()` if the global depth needs to be increased.
- **Dynamic Adjustment**: Ensures the hash table remains efficient even with unpredictable data sizes.
---

# TEST SETUP
## File Structure

```plaintext
ExtendibleHashingProject/
│
├── extendible_hashing/
│   ├── __init__.py          # Package initializer
│   ├── bucket.py            # Bucket class
│   ├── hashing.py           # Extendible Hashing class
│
├── data/
│   └── demo_input.json      # Input data in JSON format
│
├── main.py                  # Entry point to run the program
├── requirements.txt         # Dependencies file
├── README.md                # Project documentation
```

---

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Input Data:**
   - Place the product records in the `data/products.json` file in the following format:
     ```json
     [
         {"ProductID": 101, "ProductName": "Steel Rod", "Category": "Construction", "Quantity": 500},
         {"ProductID": 202, "ProductName": "Copper Wire", "Category": "Electronics", "Quantity": 300}
     ]
     ```

---

## How to Run

1. **Navigate to the Main Directory:**
   ```bash
   cd src
   ```

2. **Run the Application:**
   ```bash
   python main.py
   ```

3. **Test the Application:**
   ```bash
   pytest ../tests
   ```

---

## Contributing
Feel free to open an issue or submit a pull request for improvements or bug fixes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

