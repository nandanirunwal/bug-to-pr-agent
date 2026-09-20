marks = []

total = sum(marks)
count = len(marks)

if count:
    average = total / count
else:
    average = None  # Handle empty list case

print(average)