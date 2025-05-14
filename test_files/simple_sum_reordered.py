def calculate_sum(numbers):
    # Initialize the result
    total = 0
    
    # Add each number to the total
    for num in numbers:
        total += num
    
    # Return the final sum
    return total

def main():
    # Test the function
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(test_numbers)
    print(f"Sum of {test_numbers} is {result}")

if __name__ == "__main__":
    main() 