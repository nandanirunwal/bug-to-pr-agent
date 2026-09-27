marks = []

total = sum(marks)
count = len(marks)

if count:
    average = total / count
else:
    average = 0  # or None, or raise a custom exception

print(average)