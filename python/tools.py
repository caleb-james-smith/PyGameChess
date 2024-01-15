import os

# Creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# Round using a base
def round_using_base(number, base):
    result = number - (number % base)
    return result

# Get integers between two integers
def get_numbers_between_numbers(a, b):
    numbers = []
    if a == b:
        return numbers
    elif a < b:
        numbers = [x for x in range(a + 1, b)]
    elif a > b:
        numbers = [x for x in range(b + 1, a)]
    return numbers
