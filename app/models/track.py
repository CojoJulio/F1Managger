from pydantic import BaseModel
from typing import List

class Sector(BaseModel):
    id: int
    name: str
    start: float
    end: float
    type: str
    lenght: int
    canOvertake: bool
    drsZone: bool

class Track(BaseModel):
    id: int
    name: str
    lapLength: int
    baseLapTime: int
    pitTimeloss: int
    sectors: List[Sector]
