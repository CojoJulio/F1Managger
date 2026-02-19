from pydantic import BaseModel

class Team(BaseModel):
    id: int
    name: str
    team_color: str
