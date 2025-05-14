
# Unique file
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a = 56
b = 98
print(gcd(a, b))
