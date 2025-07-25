import os

from concurrent.futures import ThreadPoolExecutor

from functions.factorial import factorial


def pow(base: float, exp: float, n_terms: int = 100) -> float:
    if base <= 0 or exp <= 0:
        raise ValueError("Base and exponent must be positive "
                         "for logarithmic exponentiation.")

    x = exp * log_pure(base)  # b * ln(a)

    num_threads = os.cpu_count()
    chunk_size = n_terms // num_threads
    ranges = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size - 1 if i != num_threads - 1 else n_terms - 1
        ranges.append((start, end))

    def taylor_chunk(start, end):
        partial = 0.0
        for k in range(start, end + 1):
            try:
                term = (x ** k) / factorial(k)
            except OverflowError:
                term = 0.0
            partial += term
        return partial

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(taylor_chunk, start, end)
                   for start, end in ranges]
        partials = [f.result() for f in futures]

    return sum(partials)


def log_pure(x: float, terms: int = 50) -> float:
    if x <= 0:
        raise ValueError("log(x) is undefined for non-positive values")

    # Decompose x into m * 2^k so that m in [1, 2)
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1

    # Now x is in [1, 2), so we use ln(x) = ln(1 + y) with y = x - 1
    y = x - 1
    result = 0.0
    sign = 1
    for n in range(1, terms + 1):
        term = (y ** n) / n
        result += sign * term
        sign *= -1  # alternate signs

    # ln(x) = series + k * ln(2)
    LN2 = 0.6931471805599453  # precomputed ln(2)
    return result + k * LN2
