import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import os

def connect():

    SCENE_PATH = "../sim/cilyndric_robot_scene.ttt"
    scenePath = os.path.abspath(SCENE_PATH)

    for attempt in range(20):
        try:
            client = RemoteAPIClient()
            sim = client.getObject('sim')
            print(f"[SUCCESS] Conectado ao CoppeliaSim")
            return sim
        except Exception:
            print(f"[WAITING] Tentando conectar... ({attempt + 1}/20)")
            time.sleep(1)
        try:
            sim.loadScene(scenePath)
        except Exception:
            raise RuntimeError("Não foi possível abrir a cena do CoppeliaSim.")
    raise TimeoutError("Não foi possível conectar ao CoppeliaSim.")