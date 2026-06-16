import pyxel

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.is_visible = True  # Usaremos isso mais para a frente para fazê-lo sumir
        self.u_offset = 0

    def draw(self):
        if self.is_visible:
            # Usa self.u_offset dinamicamente (0 para frente, 16 para o lado)
            pyxel.blt(self.x, self.y, 0, self.u_offset, 16, self.width, self.height, colkey=0)