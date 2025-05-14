from functools import reduce

def calculate_sum(numbers):
    """
    Calculate sum using reduce function
    """
    return reduce(lambda x, y: x + y, numbers)

if __name__ == "__main__":
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(test_numbers)
    print(f"Sum of {test_numbers} is {result}") 