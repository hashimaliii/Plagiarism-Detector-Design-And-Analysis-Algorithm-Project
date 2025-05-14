def calculate_sum(values):
    # This function adds up all the numbers in a list
    total_val = 0
    for val in values:
        total_val += val
    return total_val

# Example usage
if __name__ == "__main__":
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(test_numbers)
    print(f"Sum of {test_numbers} is {result}") 