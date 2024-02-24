def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error! Division by zero."

operations = {
    '1': add,
    '2': sub,
    '3': multiply,
    '4': divide
}

print("Select an operation:")
print(" 1. ADDITION")
print(" 2. SUBTRACTION")
print(" 3. MULTIPLICATION")
print(" 4. DIVISION")

while True:
    choice = input("Enter your choice (1/2/3/4): ")
    if choice not in operations:
        print("Invalid input! Please enter a valid choice (1/2/3/4).")
        continue
    
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Please enter a proper number.")
        continue
    
    result = operations[choice](num1, num2)
    print(f"Result: {result}")
    
    next_calculation = input("Do you want to perform another calculation? (Yes/No): ").lower()
    if next_calculation != "yes":
        break
