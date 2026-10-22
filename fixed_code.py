a = 10
b = 0

try:
    result = a / b
except ZeroDivisionError:
    result = None  # handle division by zero gracefully

print(result)