#include <iostream>
#include <stdexcept>

class Calculator {
private:
    double result;

public:
    Calculator() : result(0) {}

    /**
     * Add two numbers
     * @param x First number
     * @param y Second number
     * @return Sum of x and y
     */
    double add(double x, double y) {
        result = x + y;
        return result;
    }

    /**
     * Subtract y from x
     * @param x First number
     * @param y Second number
     * @return Difference between x and y
     */
    double subtract(double x, double y) {
        result = x - y;
        return result;
    }

    /**
     * Multiply two numbers
     * @param x First number
     * @param y Second number
     * @return Product of x and y
     */
    double multiply(double x, double y) {
        result = x * y;
        return result;
    }

    /**
     * Divide x by y
     * @param x First number
     * @param y Second number
     * @return Quotient of x and y
     * @throw std::runtime_error if y is zero
     */
    double divide(double x, double y) {
        if (y == 0) {
            throw std::runtime_error("Cannot divide by zero");
        }
        result = x / y;
        return result;
    }
};

int main() {
    Calculator calc;
    
    std::cout << "Addition: " << calc.add(5, 3) << std::endl;
    std::cout << "Subtraction: " << calc.subtract(10, 4) << std::endl;
    std::cout << "Multiplication: " << calc.multiply(6, 7) << std::endl;
    std::cout << "Division: " << calc.divide(20, 5) << std::endl;
    
    return 0;
} 