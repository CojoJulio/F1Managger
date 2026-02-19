from pydantic import BaseModel

class Pilot(BaseModel):
    id: int
    name: str
    number: int
    skill: int
    agresividad: int
