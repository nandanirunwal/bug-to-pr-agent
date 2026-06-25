def calculate_average(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot calculate average of an empty list")
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average

try:
    result = calculate_average([])
    print(result)
except ValueError as e:
    print(e)