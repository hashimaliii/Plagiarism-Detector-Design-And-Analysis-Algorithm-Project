import os
from plagiarism_detector import PlagiarismDetector

def create_test_files():
    """Create test files with different levels of similarity."""
    # Create test directory if it doesn't exist
    if not os.path.exists('test_files'):
        os.makedirs('test_files')
    
    # Original code
    with open('test_files/original.py', 'w') as f:
        f.write('''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
''')
    
    # Exact copy
    with open('test_files/exact_copy.py', 'w') as f:
        f.write('''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
''')
    
    # Modified copy (variable names changed)
    with open('test_files/modified_copy.py', 'w') as f:
        f.write('''
def calculate_sum(values):
    result = 0
    for value in values:
        result += value
    return result
''')
    
    # Different code
    with open('test_files/different.py', 'w') as f:
        f.write('''
def calculate_product(numbers):
    product = 1
    for num in numbers:
        product *= num
    return product
''')

def main():
    # Create test files
    create_test_files()
    
    # Initialize plagiarism detector
    detector = PlagiarismDetector(similarity_threshold=0.7, window_size=5)
    
    # Process test files
    processed_count = detector.process_directory('test_files')
    print(f"Processed {processed_count} files")
    
    # Find plagiarism clusters
    clusters = detector.find_plagiarism_clusters()
    
    # Print results
    print("\nPlagiarism Clusters:")
    for cluster in clusters:
        print(f"\nCluster {cluster['cluster_id']}:")
        print("Submissions:", cluster['submissions'])
        print("Representatives:", cluster['representatives'])
        print("Metadata:")
        for metadata in cluster['metadata']:
            print(f"  - {metadata['file_name']}")
    
    # Get similarity matrix
    submission_ids, similarity_matrix = detector.get_similarity_matrix()
    print("\nSimilarity Matrix:")
    print("Submissions:", submission_ids)
    print("Matrix:")
    for row in similarity_matrix:
        print(row)

if __name__ == '__main__':
    main() 