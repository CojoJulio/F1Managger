from fastapi import APIRouter
from core.engine import run_engine
from state.race_state import race_state
from core.bootstrap import load_test_data
import threading
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from core.ws_manager import manager

router = APIRouter()

@router.post("/start")
def start_race():
    if race_state.running:
        return {"status": "already running"}
    
    load_test_data()
    race_state.running = True
    thread = threading.Thread(target=run_engine, daemon=True)
    thread.start()
    return {"status": "race started"}

@router.post("/stop")
def stop_race():
    race_state.running = False
    return {"status": "race stopped"}

@router.get("/state")
def get_race_state():
    track_name = race_state.track.name if race_state.track else None
    first_car = race_state.raceCars[0] if race_state.raceCars else None
    return {"running": race_state}

@router.get("/api_status")
def api_status():
    return {"status": "API is running"}

# WebSocket endpoint for real-time updates

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.add_connection(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            manager.handle_ws_command(data)
            # await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.remove_connection(websocket)

@router.on_event("startup")
async def startup_event():
    manager.loop = asyncio.get_running_loop()
