import asyncio
import time
from  state.race_state import race_state
from core.simulation import raceTick
from core.ws_manager import manager

def build_race_snapshot():
    return {
        "race": {
            "time_scale": race_state.time_scale,
            "fastest_lap": race_state.fastest_lap,
            "fastest_lap_car": race_state.fastest_lap_car
        },
        "cars": [car.model_dump() for car in race_state.raceCars]
    }

def run_engine():
    last_time = time.time()
    broadcast_timer = 0

    while True:
        now = time.time()
        raw_delta = now - last_time
        last_time = now

        delta_time = raw_delta * race_state.time_scale

        if delta_time > 0:
            raceTick(race_state.raceCars, race_state.track, delta_time)

        broadcast_timer += raw_delta

        if broadcast_timer >= 0.1:
            payload = {
                "type": "telemetry",
                "payload": build_race_snapshot()
            }

            if manager.loop:
                asyncio.run_coroutine_threadsafe(
                    manager.broadcast(payload),
                    manager.loop
                )

            broadcast_timer = 0

        time.sleep(0.01)
