import os
from concurrent.futures import ThreadPoolExecutor


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")
    if n == 0 or n == 1:
        return 1

    num_threads = os.cpu_count()  # Use the whole threads of the system!
    chunk_size = n // num_threads  # Chunk the data for the threads to work
    ranges = []

    # Create thread-safe chunks (Last chunk is going to be a bit larger,
    # due to the separation of the last items)
    for i in range(num_threads):
        start = i * chunk_size + 1
        if i != num_threads - 1:
            end = (i + 1) * chunk_size
        else:
            end = n
        ranges.append((start, end))

    def partial_product(start: int, end: int) -> int:
        result = 1
        for i in range(start, end + 1):
            result *= i
        return result

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(partial_product, start, end)
                   for start, end in ranges]
        partials = [f.result() for f in futures]

    # Bring partial results to full factorial
    result = 1
    for p in partials:
        result *= p
    return result
