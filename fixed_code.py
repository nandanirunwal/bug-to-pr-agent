marks = []

total = sum(marks)
count = len(marks)

if count:
    average = total / count
else:
    average = None  # No marks to average

print(average)