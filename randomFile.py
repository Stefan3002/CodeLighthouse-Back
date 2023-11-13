import random

def random_function():
    random_tuples = []
    
    for _ in range(45):
        random_num1 = random.uniform(0, 1)  # Generate a random floating-point number between 0 and 1
        random_num2 = random.uniform(0, 1)
        
        random_tuples.append((random_num1, random_num2))
    
    return random_tuples