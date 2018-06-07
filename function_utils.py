def compose( g, f ):
    return lambda x: g( f(x) )

def create_scale(max):
    def func(x):
        return (max * x) / 100
    return func

#Newton's Method
def inverse(f, delta=1e-9):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negative numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def derivative(func): return lambda y: (func(y+delta) - func(y)) / delta
    def root(y): return lambda x: f(x) - y
    def newton(y, iters=100):
        guess = float(y)/2
        rootfunc = root(y)
        derifunc = derivative(rootfunc)
        for _ in range(iters):
            guess = guess - (rootfunc(guess)/derifunc(guess))
        return guess
    return newton

def polynomial_function( vec ):
    def f(x):
        total = vec[0]
        term = x
        for coef in vec[1:]:
            total += term * coef
            term *= x
            
        return total
    
    return f

def zero_intercept( f ):
    
    def zi(x):
        if not x:
            return 0

        return f(x)

    return zi

