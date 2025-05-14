def calculate_product(numbers):
    """
    Calculate the product of all numbers in the input list.
    """
    product = 1
    for num in numbers:
        product *= num
    return product

if __name__ == "__main__":
    test_numbers = [1, 2, 3, 4, 5]
    result = calculate_product(test_numbers)
    print(f"Product of {test_numbers} is {result}") 