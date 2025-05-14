class Calculator {
    private result: number;

    constructor() {
        this.result = 0;
    }

    /**
     * Add two numbers
     * @param x - First number
     * @param y - Second number
     * @returns Sum of x and y
     */
    public add(x: number, y: number): number {
        this.result = x + y;
        return this.result;
    }

    /**
     * Subtract y from x
     * @param x - First number
     * @param y - Second number
     * @returns Difference between x and y
     */
    public subtract(x: number, y: number): number {
        this.result = x - y;
        return this.result;
    }

    /**
     * Multiply two numbers
     * @param x - First number
     * @param y - Second number
     * @returns Product of x and y
     */
    public multiply(x: number, y: number): number {
        this.result = x * y;
        return this.result;
    }

    /**
     * Divide x by y
     * @param x - First number
     * @param y - Second number
     * @returns Quotient of x and y
     * @throws Error if y is zero
     */
    public divide(x: number, y: number): number {
        if (y === 0) {
            throw new Error("Cannot divide by zero");
        }
        this.result = x / y;
        return this.result;
    }
}

// Test the calculator
const calc: Calculator = new Calculator();
console.log("Addition:", calc.add(5, 3));
console.log("Subtraction:", calc.subtract(10, 4));
console.log("Multiplication:", calc.multiply(6, 7));
console.log("Division:", calc.divide(20, 5)); 