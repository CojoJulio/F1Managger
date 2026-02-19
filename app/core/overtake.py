import random

def tryOvertake(behind, ahead, sector, track):
    if not sector.canOvertake:
        return False
    
    gap = progressDelta(behind.state, ahead.state, track)
    if gap > 5 or gap < 0:
        return False
    
    speedDiff =  behind.state.speed - ahead.state.speed
    if speedDiff <=1:
        return False
    
    chance = 0.3 + (behind.pilot.skill - 50) * 0.005 + (behind.pilot.agresividad - 50) * 0.004

    return random.random() < chance

def executeOvertake(behind, ahead):
    tempProgress = behind.state.lapProgress
    behind.state.lapProgress = ahead.state.lapProgress + 0.001
    ahead.state.lapProgress = tempProgress + 0.001



def progressDelta(a, b, track):
    aTotal = (a.lap - 1) * track.lapLength + a.lapProgress * track.lapLength
    bTotal = (b.lap - 1) * track.lapLength + b.lapProgress * track.lapLength

    return aTotal - bTotal

def updateDRS(car, carAhead, sector, track):
    if not carAhead:
        car.state.drsActive = False
        return
    
    deltaMeters = progressDelta(car.state, carAhead.state, track)
    deltaSeconds = deltaMeters / car.state.speed

    car.state.drsActive = sector.drsZone and deltaSeconds < 1 and deltaSeconds > 0
