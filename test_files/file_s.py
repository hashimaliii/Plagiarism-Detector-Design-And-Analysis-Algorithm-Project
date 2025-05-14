
# Unique file
def factorial_of_number(n):
    if n == 0:
        return 1
    return n * factorial_of_number(n - 1)

number = 5
print(factorial_of_number(number))
