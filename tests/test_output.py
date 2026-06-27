import pytest

def calculate_average(numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot calculate average of an empty list")
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average

def test_calculate_average_normal_case():
    numbers = [1, 2, 3, 4, 5]
    expected_average = 3
    assert calculate_average(numbers) == expected_average

def test_calculate_average_single_element():
    numbers = [5]
    expected_average = 5
    assert calculate_average(numbers) == expected_average

def test_calculate_average_negative_numbers():
    numbers = [-1, -2, -3, -4, -5]
    expected_average = -3
    assert calculate_average(numbers) == expected_average

def test_calculate_average_mixed_numbers():
    numbers = [-1, 0, 1, 2, 3]
    expected_average = 1
    assert calculate_average(numbers) == expected_average

def test_calculate_average_empty_list():
    numbers = []
    with pytest.raises(ValueError):
        calculate_average(numbers)

def test_calculate_average_float_numbers():
    numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
    expected_average = 3.0
    assert calculate_average(numbers) == expected_average

def test_calculate_average_large_numbers():
    numbers = [1000000, 2000000, 3000000, 4000000, 5000000]
    expected_average = 3000000
    assert calculate_average(numbers) == expected_average