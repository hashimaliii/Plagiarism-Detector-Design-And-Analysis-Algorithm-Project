def sum_numbers(nums):
    total = 0
    # Loop through each number in the list
    for num in nums:
        total += num   # Add the current number to the total
    return total

# List of numbers to sum
numbers = [1, 2, 3, 4, 5]
print(sum_numbers(numbers))  # Output the result