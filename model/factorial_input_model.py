from pydantic import BaseModel


# This represents the structure model for factorial input
class FactorialInput(BaseModel):
    n: int
