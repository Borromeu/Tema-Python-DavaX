from pydantic import BaseModel


# This represents the structure model for fibonacci input
class FibonacciInput(BaseModel):
    n: int
