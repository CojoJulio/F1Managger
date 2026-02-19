def getCurrentSector(track, raceCarState):
    for sector in track.sectors:
        if raceCarState.lapProgress >= 1:
            return track.sectors[-1]
        if raceCarState.lapProgress >= sector.start and raceCarState.lapProgress < sector.end:
            return sector
    return None