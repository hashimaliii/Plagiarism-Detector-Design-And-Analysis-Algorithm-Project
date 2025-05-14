
# Unique file
def product_of_numbers(nums):
    product = 1
    for num in nums:
        product *= num
    return product

numbers = [1, 2, 3, 4, 5]
print(product_of_numbers(numbers))
