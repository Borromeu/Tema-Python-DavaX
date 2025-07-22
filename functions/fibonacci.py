
# This method will calculate the fibonacci with the values of parameters
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Negative index not allowed for Fibonacci.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a