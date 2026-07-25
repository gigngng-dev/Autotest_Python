import math

def square(side):
    area = side * side
    return math.ceil(area)

acreage = input("Введите длину стороны квадрата: ")
print(square(float(acreage)))