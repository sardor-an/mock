from random import randint

def generate_product_code():
    code = ''.join([str(randint(0,1000) % 10) for _ in range(0, 6)])
    return code