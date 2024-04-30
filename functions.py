from math import sqrt, exp, cos, sin, pi, e

def Griewank(*args):
    sum_sq = sum(x ** 2 for x in args)
    prod_cos = 1
    for i, x in enumerate(args, 1):
        prod_cos *= cos(x / sqrt(i))
    return sum_sq / 4000 - prod_cos + 1
