def calculate_sum(values):
    # This function adds up all the numbers in a list
    result = 0
    for value in values:
        result += value
    return result

# Test the function
if __name__ == "__main__":
    sample_data = [1, 2, 3, 4, 5]
    sum_result = calculate_sum(sample_data)
    print(f"The total is: {sum_result}") 