class Player:
    def __init__(self, turno=2, movimiento_pasivo=True, otro_player=None, lado_pasivo=None):
        self.contador_turno = turno
        self.lado_pasivo = lado_pasivo
        self.lado_agresivo = None
        if movimiento_pasivo:
            self.movimiento_pasivo = movimiento_pasivo
            self.movimiento_agresivo = not movimiento_pasivo
        else:
            self.movimiento_pasivo = False
            self.movimiento_agresivo = False
        self.otro_player = otro_player
        self.new_x = None
        self.new_y = None

    def move(self, lado_agresivo):

        if self.contador_turno > 0:
            self.contador_turno -= 1
            if self.contador_turno == 1:
                self.movimiento_pasivo = not self.movimiento_pasivo
                self.movimiento_agresivo = not self.movimiento_pasivo
                if lado_agresivo == "IZQUIERDA":
                    self.lado_agresivo = "DERECHA"
                else:
                    self.lado_agresivo = "IZQUIERDA"
            if self.contador_turno == 0:
                print("Turno del otro jugador")
                self.otro_player.reset()
                self.movimiento_pasivo = False
                self.movimiento_agresivo = False
                self.new_x = None
                self.new_y = None
        else:
            self.movimiento_agresivo = False
            self.movimiento_pasivo = False

    def is_playing(self):
        return self.contador_turno > 0

    def reset(self):
        self.contador_turno = 2
        self.movimiento_pasivo = True
        self.movimiento_agresivo = False

    def __str__(self):
        return f"Movimiento pasivo : {self.movimiento_pasivo} Movimiento agresivo : {self.movimiento_agresivo} " \
               f"Contador : {self.contador_turno} NewX: {self.new_x} NewY: {self.new_y}  "
