import random
import time
import os

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

# Funciones

def simulationTick(raceCar, track, deltaTime = 1):

    if raceCar['state']['inPit']:
        pitTick(raceCar, deltaTime)
        return
    
    checkPitEntry(raceCar)


    sector = getCurrentSector(track, raceCar['state'])

    speed = calculateSpeed(track, raceCar['pilot'], raceCar['car'], raceCar['tyre'], raceCar['state'])

    raceCar['state']['speed'] = speed

    avance = speed * deltaTime
    raceCar['state']['lapProgress'] += avance / track['lapLenght']
    raceCar['state']['totalTime'] += deltaTime

    updateTyreWear(raceCar['tyre'], raceCar['pilot'], deltaTime, track, raceCar['state'])
    updateFuel(raceCar['state'], raceCar['pilot'], deltaTime)

    if raceCar['state']['lapProgress'] >= 1:
        raceCar['state']['lap'] += 1
        raceCar['state']['lapProgress'] = 0


def raceTick(raceCars, track, deltaTime = 1):
    for raceCar in raceCars:
        simulationTick(raceCar, track, deltaTime)

    raceCars.sort(key=lambda x: x['state']['lapProgress'], reverse=True)

    for i, raceCar in enumerate(raceCars):
        raceCar['state']['position'] = i + 1

    for i in range(len(raceCars)):
        behind = raceCars[i]
        ahead = raceCars[i - 1]

        sector = getCurrentSector(track, behind['state'])

        updateDRS(behind, ahead, sector)

        if tryOvertake(behind, ahead, sector, track):
            executeOvertake(behind, ahead)


def calculateSpeed(track, pilot, car, tyre, raceCarState):

    velocidadBase = track["lapLenght"] / track["BaseLapTime"]

    sector = getCurrentSector(track, raceCarState)

    sectorData = sector_speed_modifiers[sector["type"]]

    pilotFactor = 1 + (pilot['skill'] - 50) * 0.002
    carFactor = 1 + (car['performance'] - 50) * 0.002
    tyreFactor = tyre['grip']

    desgasteFactor = 0.7 + (tyre['wear'] / 100) * 0.3
    fuelFactor = 0.9 + (raceCarState['fuel'] / 100) * 0.1

    randomFactor = 1 + (random.uniform(-0.02, 0.02))

    speed = velocidadBase * pilotFactor * carFactor * tyreFactor * desgasteFactor * fuelFactor * randomFactor * sectorData["baseMultiplier"]

    if speed > sectorData["maxSpeed"]:
        speed = sectorData["maxSpeed"]

    if raceCarState['drsActive']:
        speed *= drs_multiplier
    
    return speed


def updateTyreWear(tyre, pilot, deltaTime, track, raceCarState):

    sector = getCurrentSector(track, raceCarState)

    desgasteBase = 0.12
    tyre['wear'] -= desgasteBase * sector_wear_multiplier[sector['type']] * (1 + pilot['agresividad'] / 100) * deltaTime

    if tyre['wear'] < 0:
        tyre['wear'] = 0

def updateFuel(raceCarState, pilot, deltaTime):
    consumoBase = 0.05
    raceCarState['fuel'] -= consumoBase * (1 + pilot['agresividad'] / 100) * deltaTime

    if raceCarState['fuel'] < 0:
        raceCarState['fuel'] = 0


def getCurrentSector(track, raceCarState):
    for sector in track['sectores']:
        if raceCarState['lapProgress'] >= 1:
            return track['sectores'][-1]
        if raceCarState['lapProgress'] >= sector['start'] and raceCarState['lapProgress'] < sector['end']:
            return sector
    return None

# Overtake Logic

def tryOvertake(behind, ahead, sector, track):
    if not sector['canOvertake']:
        return False
    
    gap = progressDelta(behind['state'], ahead['state'], track)
    if gap > 5 or gap < 0:
        return False
    
    speedDiff =  behind['state']['speed'] - ahead['state']['speed']
    if speedDiff <=1:
        return False
    
    chance = 0.3 + (behind['pilot']['skill'] - 50) * 0.005 + (behind['pilot']['agresividad'] - 50) * 0.004

    return random.random() < chance

def executeOvertake(behind, ahead):
    tempProgress = behind['state']['lapProgress']
    behind['state']['lapProgress'] = ahead['state']['lapProgress'] + 0.001
    ahead['state']['lapProgress'] = tempProgress + 0.001



def progressDelta(a, b, track):
    aTotal = (a['lap'] - 1) * track['lapLenght'] + a['lapProgress'] * track['lapLenght']
    bTotal = (b['lap'] - 1) * track['lapLenght'] + b['lapProgress'] * track['lapLenght']

    return aTotal - bTotal

def updateDRS(car, carAhead, sector):
    if not carAhead:
        car['state']['drsActive'] = False
        return
    
    deltaMeters = progressDelta(car['state'], carAhead['state'], track)
    deltaSeconds = deltaMeters / car['state']['speed']

    car['state']['drsActive'] = sector['drsZone'] and deltaSeconds < 1 and deltaSeconds > 0;


def requestPitStop(car):
    car['state']['requestedPit'] = True

def checkPitEntry(car):
    if car['state']['requestedPit'] and car['state']['lapProgress'] < 0.01 and not car['state']['inPit']:
        startPitStop(car)

def startPitStop(car):
    
    car['state']['inPit'] = True
    car['state']['requestedPit'] = False

    car['state']['pitTimeRemaining'] = track['pitTimeLoss']

    car['state']['speed'] = 0

def pitTick(car, deltaTime):
    car['state']['pitTimeRemaining'] -= deltaTime
    car['state']['totalTime'] += deltaTime

    if car['state']['pitTimeRemaining'] <= 0:
        endPitStop(car)

def endPitStop(car):
    car['state']['inPit'] = False

    car['tyre'] = {
        "compound": "soft",
        "grip": 1.05,
        "wear": 100
    }

    car['state']['fuel'] = 100


# Herramientas

def raceGraph(raceCars, track):
    for raceCar in raceCars:
        line = '-'
        progress = round(raceCar['state']['lapProgress'] * 10)
        firstLetter = raceCar['pilot']['name'][0]

        # print(raceCar['state']['lapProgress'])
        print(line * progress, end='')
        print(firstLetter, end='')

        print(line * (10 - progress))

def timeCalc(ticks):

    minutos = ticks // 60
    segundos = ticks % 60
    tiempo = f"{minutos:02d}:{segundos:02d}"

    return tiempo


# Bucle Principal

for i in range(600):
    os.system('cls')
    # simulationTick(track, pilot, car, tyre, raceCarState, 1)
    # sector = getCurrentSector(track, raceCarState)

    raceTick(raceCars, track, 1)
    raceGraph(raceCars, track)

    print(f'Lap: {raceCars[0]["state"]["lap"]}')
    print(f'Tiempo: {timeCalc(raceCars[0]["state"]["totalTime"])}')

    for i in range(len(raceCars)):
        raceCar = raceCars[i]

        print(f'POS: {raceCar["state"]["position"]} - {raceCar["pilot"]["name"]} - DRS: {raceCar["state"]["drsActive"]} - Speed: {raceCar["state"]["speed"] * 3.6:.0f} km/h - Fuel: {raceCar["state"]["fuel"] *1:.0f}%')



    print()
    time.sleep(0.05)
