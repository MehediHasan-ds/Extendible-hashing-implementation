class Bucket:
    def __init__(self, bucket_capacity, local_depth):
        self.bucket_capacity = bucket_capacity
        self.local_depth = local_depth
        self.records = []

    def is_full(self):
        """Check if the bucket is full."""
        return len(self.records) >= self.bucket_capacity

    def add_record(self, record):
        """Add a record to the bucket."""
        self.records.append(record)
