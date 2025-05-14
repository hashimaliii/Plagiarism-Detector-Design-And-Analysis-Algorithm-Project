class Calculator {
    constructor() {
        this.result = 0;
    }

    /**
     * Add two numbers
     * @param {number} x - First number
     * @param {number} y - Second number
     * @returns {number} Sum of x and y
     */
    add(x, y) {
        this.result = x + y;
        return this.result;
    }

    /**
     * Subtract y from x
     * @param {number} x - First number
     * @param {number} y - Second number
     * @returns {number} Difference between x and y
     */
    subtract(x, y) {
        this.result = x - y;
        return this.result;
    }

    /**
     * Multiply two numbers
     * @param {number} x - First number
     * @param {number} y - Second number
     * @returns {number} Product of x and y
     */
    multiply(x, y) {
        this.result = x * y;
        return this.result;
    }

    /**
     * Divide x by y
     * @param {number} x - First number
     * @param {number} y - Second number
     * @returns {number} Quotient of x and y
     * @throws {Error} If y is zero
     */
    divide(x, y) {
        if (y === 0) {
            throw new Error("Cannot divide by zero");
        }
        this.result = x / y;
        return this.result;
    }
}

// Test the calculator
const calc = new Calculator();
console.log("Addition:", calc.add(5, 3));
console.log("Subtraction:", calc.subtract(10, 4));
console.log("Multiplication:", calc.multiply(6, 7));
console.log("Division:", calc.divide(20, 5)); 