public class Calculator {
    private double result;
    
    public Calculator() {
        this.result = 0;
    }
    
    /**
     * Add two numbers
     * @param x First number
     * @param y Second number
     * @return Sum of x and y
     */
    public double add(double x, double y) {
        this.result = x + y;
        return this.result;
    }
    
    /**
     * Subtract y from x
     * @param x First number
     * @param y Second number
     * @return Difference between x and y
     */
    public double subtract(double x, double y) {
        this.result = x - y;
        return this.result;
    }
    
    /**
     * Multiply two numbers
     * @param x First number
     * @param y Second number
     * @return Product of x and y
     */
    public double multiply(double x, double y) {
        this.result = x * y;
        return this.result;
    }
    
    /**
     * Divide x by y
     * @param x First number
     * @param y Second number
     * @return Quotient of x and y
     * @throws ArithmeticException if y is zero
     */
    public double divide(double x, double y) {
        if (y == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        this.result = x / y;
        return this.result;
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        System.out.println("Addition: " + calc.add(5, 3));
        System.out.println("Subtraction: " + calc.subtract(10, 4));
        System.out.println("Multiplication: " + calc.multiply(6, 7));
        System.out.println("Division: " + calc.divide(20, 5));
    }
} 