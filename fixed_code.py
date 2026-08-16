numbers = [10, 20, 30]
try:
    print(numbers[5])
except IndexError:
    print("Index out of range error: The list has only", len(numbers), "elements")