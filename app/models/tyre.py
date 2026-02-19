from pydantic import BaseModel

class Tyre(BaseModel):
    id: int
    compound: str
    grip: float
    wear: float = 100