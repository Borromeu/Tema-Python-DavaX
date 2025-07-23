
# This method will calculate the fibonacci with the values of parameters
# Fast doubling Fibonacci
def fibonacci(n: int) -> int:
    def helper(n: int) -> tuple[int, int]:
        if n < 0:
            raise ValueError("Negative index not allowed for Fibonacci.")
        if n == 0:
            return 0, 1
        a, b = helper(n // 2)
        c = a * (2 * b - a)
        d = a * a + b * b
        return (c, d) if n % 2 == 0 else (d, c + d)

    return helper(n)[0]