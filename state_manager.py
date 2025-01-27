# state_manager.py

class BotStateManager:
    def __init__(self):
        self.state = "START"
        self.body_part = None

    def set_state(self, new_state):
        """Cambia el estado actual del bot."""
        print(f"Transición de estado: {self.state} -> {new_state}")
        self.state = new_state

    def get_state(self):
        """Obtiene el estado actual del bot."""
        return self.state

    def set_body_part(self, body_part):
        """Define la parte del cuerpo mencionada por el usuario."""
        self.body_part = body_part

    def get_body_part(self):
        """Obtiene la parte del cuerpo mencionada por el usuario."""
        return self.body_part

    def reset(self):
        """Resetea los estados y variables."""
        self.state = "START"
        self.body_part = None
