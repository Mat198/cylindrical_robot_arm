import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import os

def connect():

    SCENE_PATH = "sim/cilyndric_robot_scene.ttt"
    scenePath = os.path.abspath(SCENE_PATH)

    for attempt in range(20):
        try:
            client = RemoteAPIClient()
            sim = client.getObject('sim')
            print(f"[SUCCESS] Conectado ao CoppeliaSim")
            result = sim.loadScene(scenePath)
            if not result:
                raise RuntimeError("Não foi possível abrir a cena do CoppeliaSim.")
            return sim
        except Exception:
            print(f"[WAITING] Tentando conectar... ({attempt + 1}/20)")
            time.sleep(1)
    raise TimeoutError("Não foi possível conectar ao CoppeliaSim.")