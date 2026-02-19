import random
# Variables

track = {
    "name": "Circuito Demo",
    "lapLenght": 5000,
    "BaseLapTime": 100,
    "pitTimeLoss": 22,
    "sectores": [
        { "id": 1, "name": "Recta Principal", "start": 0, "end": 0.20, "type": "straight", "lenght": 1000, "canOvertake": True, "drsZone": True},
        { "id": 2, "name": "Curvas Rapidas", "start": 0.20, "end": 0.45, "type": "fast_corner", "lenght": 1250, "canOvertake": True, "drsZone": False},
        { "id": 3, "name": "Chicana", "start": 0.45, "end": 0.55, "type": "chicana", "lenght": 500, "canOvertake": False, "drsZone": False},
        { "id": 4, "name": "Curvas Lentas", "start": 0.55, "end": 0.80, "type": "slow_corner", "lenght": 1250, "canOvertake": False, "drsZone": False},
        { "id": 4, "name": "Sector Mixto", "start": 0.80, "end": 1, "type": "fast_corner", "lenght": 1000, "canOvertake": False, "drsZone": False},
    ]
}

pilot = {
    "name": "Checo Perez",
    "skill": 70,
    "agresividad": 60
}

car = {
    "performance": 60
}

tyre = {
    "compound": "soft",
    "grip": 1.05,
    "wear": 100
}


sector_speed_modifiers = {
    "straight": {
        "baseMultiplier": 1.15,
        "maxSpeed": 95
    },
    "fast_corner": {
        "baseMultiplier": 1.00,
        "maxSpeed": 75
    },
    "chicana": {
        "baseMultiplier": 0.80,
        "maxSpeed": 55
    },
    "slow_corner": {
        "baseMultiplier": 0.70,
        "maxSpeed": 45
    }
}

sector_wear_multiplier = {
    "straight": 0.6,
    "fast_corner": 1.2,
    "slow_corner": 1.4,
    "chicana": 1.8
}





# Funcion para crear piloto con auto

def createRaceCarState(id, pilot, car, tyre):
    raceCar = {
        "id": id,
        "pilot": pilot,
        "car": car,
        "tyre": tyre,
        "state": {
            "lap": 1,
            "lapProgress": random.randint(0, 1) * 0.01,
            "totalTime": 0,
            "fuel": 100,
            "speed": 0,
            "position": 0,
            "drsActive": False,
            "inPit": False,
            "pitTimeRemaining": 0,
            "requestedPit": False
        }
    }
    return raceCar

raceCars = [
    createRaceCarState(1, {"name": "Checo Perez", "skill": 70, "agresividad": 60}, {"performance": 60
    }, {"compound": "soft", "grip": 1.05, "wear": 100}),
    createRaceCarState(2, {"name": "Max Verstappen", "skill": 85, "agresividad": 80}, {"performance": 75
    }, {"compound": "medium", "grip": 1.02, "wear": 100}),
    createRaceCarState(3, {"name": "Lewis Hamilton", "skill": 90, "agresividad": 90}, {"performance": 80
    }, {"compound": "hard", "grip": 0.98, "wear": 100}),
    createRaceCarState(4, {"name": "Valtteri Bottas", "skill": 75, "agresividad": 70}, {"performance": 65
    }, {"compound": "soft", "grip": 1.05, "wear": 100})
]

drs_multiplier = 1.08