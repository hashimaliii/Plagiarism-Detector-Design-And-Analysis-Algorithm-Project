def calculate_sum(numbers):
    # This function adds up all the numbers in a list
    total = 0
    for num in numbers:
        total += num
    return total

# Example usage
if __name__ == "__main__":
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(test_numbers)
    print(f"Sum of {test_numbers} is {result}") 