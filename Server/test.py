from random import randint
def randomList(m, n):
    arr = [0] * m
    for i in range(n) :
        arr[randint(0, n) % m] += 1
    return arr

print(randomList(4,9))