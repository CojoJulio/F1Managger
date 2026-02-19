def requestPitStop(car):
    car.state.requestedPit = True

def checkPitEntry(car, track):
    if car.state.requestedPit and car.state.lapProgress < 0.01 and not car.state.inPit:
        startPitStop(car, track)

def startPitStop(car, track):
    
    car.state.inPit = True
    car.state.requestedPit = False
 
    car.state.pitTimeRemaining = track.pitTimeloss

    car.state.speed = 0

def pitTick(car, deltaTime):
    car.state.pitTimeRemaining -= deltaTime
    car.state.totalTime += deltaTime

    if car.state.pitTimeRemaining <= 0:
        endPitStop(car)

def endPitStop(car):
    car.state.inPit = False

    car.tyre = {
        "compound": "soft",
        "grip": 1.05,
        "wear": 100
    }

    car.state.fuel = 100