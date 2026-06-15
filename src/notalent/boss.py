import pyxel

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.is_visible = True  # Usaremos isso mais para a frente para fazê-lo sumir

    def draw(self):
        if self.is_visible:
            # Desenha o Boss pegando o sprite em U=0, V=16 (linha 16) com tamanho 16x16
            pyxel.blt(self.x, self.y, 0, 0, 16, self.width, self.height, colkey=0)