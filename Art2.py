"""A simple command-line calculator.

Supports addition, subtraction, multiplication and division.
Run it with:  python Art2.py
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def calculate(a, operator, b):
    """Apply the operator to a and b and return the result."""
    if operator not in OPERATIONS:
        raise ValueError(f"Unknown operator: {operator}")
    return OPERATIONS[operator](a, b)


def read_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("That is not a valid number. Please try again.")


def main():
    print("Simple Calculator")
    print("Operators: +  -  *  /")

    while True:
        a = read_number("Enter first number: ")
        operator = input("Enter operator (+, -, *, /): ").strip()
        b = read_number("Enter second number: ")

        try:
            result = calculate(a, operator, b)
            print(f"Result: {a:g} {operator} {b:g} = {result:g}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")

        again = input("Do another calculation? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
