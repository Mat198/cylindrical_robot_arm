# --- Interface Tkinter ---
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np # Importando numpy para a simulação do getCurrentPosition

class RobotControlApp:
    def __init__(self, master, robot):
        self.master = master
        self.robot = robot
        master.title("Controle de Robô Simples")

        # --- Frames para organização ---
        self.joint_frame = ttk.LabelFrame(master, text="Controle de Juntas")
        self.joint_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.cartesian_frame = ttk.LabelFrame(master, text="Controle Cartesiano")
        self.cartesian_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.position_frame = ttk.LabelFrame(master, text="Posição Atual")
        self.position_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # --- Widgets para jointMove ---
        ttk.Label(self.joint_frame, text="Joint 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.joint1_entry = ttk.Entry(self.joint_frame)
        self.joint1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.joint_frame, text="Joint 2:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.joint2_entry = ttk.Entry(self.joint_frame)
        self.joint2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.joint_frame, text="Joint 3:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.joint3_entry = ttk.Entry(self.joint_frame)
        self.joint3_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.joint_move_button = ttk.Button(self.joint_frame, text="Mover Juntas", command=self._call_joint_move)
        self.joint_move_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Configura as colunas para expandir
        self.joint_frame.grid_columnconfigure(1, weight=1)

        # --- Widgets para cartesianMove ---
        ttk.Label(self.cartesian_frame, text="X:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.x_entry = ttk.Entry(self.cartesian_frame)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.x_entry.insert(tk.END, '-0.75')

        ttk.Label(self.cartesian_frame, text="Y:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.y_entry = ttk.Entry(self.cartesian_frame)
        self.y_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.y_entry.insert(tk.END, '-0.25')

        ttk.Label(self.cartesian_frame, text="Z:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.z_entry = ttk.Entry(self.cartesian_frame)
        self.z_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.z_entry.insert(tk.END, '0.75')
        ttk.Label(self.cartesian_frame, text="Duração:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self.cartesian_frame)
        self.duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.duration_entry.insert(tk.END, '4')

        self.cartesian_move_button = ttk.Button(self.cartesian_frame, text="Mover Cartesiano", command=self._call_cartesian_move)
        self.cartesian_move_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.refresh_position_button = ttk.Button(self.position_frame, text="Atualizar Posição", command=self._update_current_position_display)
        self.refresh_position_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Configura as colunas para expandir
        self.cartesian_frame.grid_columnconfigure(1, weight=1)

        # --- Widget para getCurrentPosition ---
        ttk.Label(self.position_frame, text="Posição Atual:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.position_label = ttk.Label(self.position_frame, text="Pos = [?, ?, ?]", font=("Arial", 12, "bold"))
        self.position_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.fk_label = ttk.Label(self.position_frame, text="FK = [?, ?, ?]", font=("Arial", 12, "bold"))
        self.fk_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Configura a coluna para expandir
        self.position_frame.grid_columnconfigure(1, weight=1)

        # Inicializa a exibição da posição
        self._update_current_position_display()

    def _call_joint_move(self):
        """Chama jointMove com os valores dos campos de entrada."""
        joint1 = self.joint1_entry.get()
        joint2 = self.joint2_entry.get()
        joint3 = self.joint3_entry.get()

        # Atualiza a posição simulada e o display
        try:
            target = [float(joint1), float(joint2), float(joint3)]
        except ValueError:
            messagebox.showinfo("Erro", "Valor invalido para posição das juntas")
            return # Ignora se a entrada não for numérica, a mensagem de erro já foi mostrada
        
        self.robot.jointMove(target[0], target[1], target[2])
        position = self.robot.fk(target[0], target[1], target[2])
        self.fk_label.config(text=f"FK = [{position[0]:.3f}, {position[1]:.3f}, {position[2]:.3f}]")

    def _call_cartesian_move(self):
        """Chama cartesianMove com os valores dos campos de entrada."""
        x = self.x_entry.get()
        y = self.y_entry.get()
        z = self.z_entry.get()
        duration = self.duration_entry.get()

        # Atualiza a posição simulada e o display
        try:
            target = [float(x), float(y), float(z)]
            duration = float(duration)
        except ValueError:
            messagebox.showinfo("Erro", "Valor invalido para posição alvo")
            return # Ignora se a entrada não for numérica, a mensagem de erro já foi mostrada

        self.robot.cartesianMove(target[0], target[1], target[2], duration)

    def _update_current_position_display(self):
        """Atualiza o Label com a posição atual."""
        position = self.robot.getCurrentPosition()
        self.position_label.config(text=f"Pos = [{position[0]:.3f}, {position[1]:.3f}, {position[2]:.3f}]")


# --- Cria e executa a aplicação ---
if __name__ == "__main__":

    from coppeliasim_zmqremoteapi_client import RemoteAPIClient
    from scripts.connect import connect
    # Classe para interface com o robô
    from robot import CylindricRobot

    client = RemoteAPIClient()
    sim = connect()

    print("Simulação iniciada")
    sim.startSimulation()

    # Cria objeto para interface com o robô
    robot = CylindricRobot("/P0_ST", sim)

    # Cria a interface de usuário
    root = tk.Tk()
    app = RobotControlApp(root, robot)
    root.mainloop()

    sim.stopSimulation()
    print("Simulação encerrada")