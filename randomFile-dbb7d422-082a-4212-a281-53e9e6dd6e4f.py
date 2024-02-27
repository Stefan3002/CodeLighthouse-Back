import random
def random_function():
    tests = []
    for i in range(60):
        random_num = random.randint(0, 100)
        tests.append((random_num,))
    return tests