from .team import Team
from pydantic import BaseModel
from .pilot import Pilot
from .car import Car
from .tyre import Tyre

class RaceCarState(BaseModel):
    lap: int = 1
    lapProgress: float = 0
    totalTime: float = 0
    fuel: float = 100
    speed: float = 0
    sector: int | None = None
    sector_start_time: float = 0
    sectors_times: list[float] = []
    position: int = 0
    in_pit: bool = False
    pit_time_remaining: float = 0
    drsActive: bool = False
    requestedPit: bool = False
    gap_to_leader: float = 0
    last_lap_time: float | None = None
    lap_start_time: float = 0

class RaceCar(BaseModel):
    id: int
    pilot: Pilot
    car: Car
    team: Team
    tyre: Tyre
    state: RaceCarState = RaceCarState()
    lap_history: list[float] = []
    sector_history: list[float] = []