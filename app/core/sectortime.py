from core.track import getCurrentSector

def sectorTimeTick(raceCar, track, dt):
    state = raceCar.state

    if state.in_pit:
        return

    current_sector = getCurrentSector(track, state)
    if current_sector is None:
        return

    current_sector_id = current_sector.id
    previous_sector_id = state.sector

    # 🚀 PRIMER TICK (inicialización)
    if previous_sector_id is None:
        state.sector = current_sector_id
        state.sector_start_time = state.totalTime
        state.sectors_times = []
        return

    # 🔄 CAMBIO DE SECTOR
    if current_sector_id != previous_sector_id:

        # Calcular tiempo del sector anterior
        sector_time = state.totalTime - state.sector_start_time
        state.sectors_times.append(sector_time)

        # Guardar histórico por sector
        if len(raceCar.sector_history) <= previous_sector_id:
            raceCar.sector_history.extend(
                [0] * (previous_sector_id - len(raceCar.sector_history) + 1)
            )

        raceCar.sector_history[previous_sector_id] = sector_time

        # Resetear inicio del nuevo sector
        state.sector_start_time = state.totalTime
        state.sector = current_sector_id