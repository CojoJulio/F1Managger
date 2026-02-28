from models.team import Team
from state.race_state import race_state
from models.car import Car
from models.track import Track, Sector
from models.pilot import Pilot
from models.tyre import Tyre
from models.race_car import RaceCar


def load_test_data():
    # Load test data for track

    race_state.track = Track(
        id=1,
        name="Circuit de Monaco",
        lapLength=5000,
        baseLapTime=100,
        pitTimeloss=22,
        sectors=[
            Sector(id=1, name="S1", start=0, end=0.25, type="straight", lenght=1000, canOvertake=True, drsZone=True),
            Sector(id=2, name="S2", start=0.25, end=0.66, type="slow_corner", lenght=1668, canOvertake=False, drsZone=False),
            Sector(id=3, name="S3", start=0.66, end=1, type="fast_corner", lenght=669, canOvertake=False, drsZone=False)])
    
    
    def createRaceCarState(id, pilot, car, tyre, team):
        return RaceCar(
            id=id,
            pilot=Pilot(**pilot),
            car=Car(**car),
            team=Team(**team),
            tyre=Tyre(**tyre),
            state={
                "lap": 0,
                "lapProgress": 0.0,
                "totalTime": 0.0,
                "speed": 0.0,
                "inPit": False,
                "fuel": 100.0,
                "drsActive": False
            }
        )

    raceCars = [
        createRaceCarState(1, {"id": 1, "name": "Checo Perez", "number": 11, "skill": 70, "agresividad": 60}, {"id": 1, "performance": 60
        }, {"id": 1,"compound": "soft", "grip": 1.05, "wear": 100}, {"id": 1, "name": "Red Bull Racing", "team_color": "#1E40AF"}),
        createRaceCarState(2, {"id": 2, "name": "Max Verstappen", "number": 33, "skill": 85, "agresividad": 80}, {"id": 2, "performance": 75
        }, {"id": 2,"compound": "medium", "grip": 1.02, "wear": 100}, {"id": 2, "name": "Red Bull Racing", "team_color": "#1E40AF"}),
        createRaceCarState(3, {"id": 3, "name": "Lewis Hamilton", "number": 44, "skill": 90, "agresividad": 90}, {"id": 3, "performance": 80
        }, {"id": 3,"compound": "hard", "grip": 0.98, "wear": 100}, {"id": 3, "name": "Mercedes", "team_color": "#00AEEF"}),
        createRaceCarState(4, {"id": 4, "name": "Carlos Sainz", "number": 55, "skill": 75, "agresividad": 70}, {"id": 4, "performance": 65
        }, {"id": 4,"compound": "soft", "grip": 1.05, "wear": 100}, {"id": 4, "name": "Ferrari", "team_color": "#DC0000"}),
        createRaceCarState(5, {"id": 5, "name": "Charles Leclerc", "number": 16, "skill": 80, "agresividad": 75}, {"id": 5, "performance": 70
        }, {"id": 5,"compound": "medium", "grip": 1.02, "wear": 100}, {"id": 5, "name": "Ferrari", "team_color": "#DC0000"}),
        createRaceCarState(6, {"id": 6, "name": "Lando Norris", "number": 4, "skill": 78, "agresividad": 65}, {"id": 6, "performance": 68
        }, {"id": 6,"compound": "hard", "grip": 0.98, "wear": 100}, {"id": 6, "name": "McLaren", "team_color": "#FF8700"})
    ]

    race_state.raceCars = raceCars

    
    



