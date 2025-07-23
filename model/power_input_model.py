from pydantic import BaseModel

# This represents the structure model for power input
class PowerInput(BaseModel):
    base: float
    exp: float

