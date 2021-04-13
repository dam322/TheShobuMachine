class Player:
    def __init__(self, movimiento_pasivo=True, lado_pasivo=None, value=0, is_machine=False):
        self.is_machine = is_machine
        self.lado_pasivo = lado_pasivo
        self.lado_agresivo = None
        self.value = value
        self.win = False
        if movimiento_pasivo:
            self.movimiento_pasivo = movimiento_pasivo
            self.movimiento_agresivo = not movimiento_pasivo
            self.contador_turno = 2
        else:
            self.movimiento_pasivo = False
            self.movimiento_agresivo = False
            self.contador_turno = 0
        self.enemy_player = None
        self.passive_move_dx = None
        self.passive_move_dy = None
        if is_machine:
            self.nombre = "machine " + str(value)
        else:
            self.nombre = "player " + str(value)

    def update_passive_change(self, piece_to_move, piece_where_is_moved):
        self.passive_move_dx = piece_to_move.x - piece_where_is_moved.x
        self.passive_move_dy = piece_to_move.y - piece_where_is_moved.y

    def on_passive(self, lado_agresivo, piece_to_move, piece_where_is_moved):
        self.contador_turno = 1
        self.movimiento_pasivo = False
        self.movimiento_agresivo = True
        self.update_passive_change(piece_to_move, piece_where_is_moved)
        if lado_agresivo == "IZQUIERDA":
            self.lado_agresivo = "DERECHA"
        else:
            self.lado_agresivo = "IZQUIERDA"

    def on_agressive(self):
        self.contador_turno = 0
        print(f"--> Turno del jugador {self.enemy_player.nombre}")
        self.enemy_player.reset()
        self.movimiento_pasivo = False
        self.movimiento_agresivo = False
        self.passive_move_dx = None
        self.passive_move_dy = None

    def move(self, lado_agresivo, piece_to_move, piece_where_is_moved):
        if self.contador_turno > 0:
            self.contador_turno -= 1
            # Movimiento pasivo
            if self.contador_turno == 1:
                self.on_passive(lado_agresivo, piece_to_move, piece_where_is_moved)
            # Movimiento agresivo
            if self.contador_turno == 0:
                self.on_agressive()
        else:
            self.movimiento_agresivo = False
            self.movimiento_pasivo = False

    def is_playing(self):
        return self.contador_turno > 0

    def reset(self):
        self.contador_turno = 2
        self.movimiento_pasivo = True
        self.movimiento_agresivo = False
        self.passive_move_dx = None
        self.passive_move_dy = None

    def __str__(self):
        return f"Movimiento pasivo : {self.movimiento_pasivo} Movimiento agresivo : {self.movimiento_agresivo} " \
               f"Contador : {self.contador_turno} Name: {self.nombre}, Value: {self.value}"
