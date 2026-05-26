import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.is_sleeping = True
        self.direction = "down"  # 'up', 'down', 'left', 'right'
        
        # Dimensões do personagem (um quadrado simples por enquanto)
        self.width = 8
        self.height = 8

    def update(self):
        if self.is_sleeping:
            return

        # Movimentação restrita a 4 direções (estilo Pokémon)
        # Prioriza uma direção por vez para impedir movimento diagonal
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.speed
            self.direction = "up"
        elif pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
            self.direction = "down"
        elif pyxel.btn(pyxel.KEY_A):
            self.x -= self.speed
            self.direction = "left"
        elif pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
            self.direction = "right"

        # Limites da tela (160x120)
        self.x = max(0, min(self.x, 160 - self.width))
        self.y = max(0, min(self.y, 120 - self.height))

    def draw(self):
        if self.is_sleeping:
            # Desenha o personagem deitado (invertendo largura/altura visualmente)
            pyxel.rect(self.x, self.y, self.height, self.width - 4, 9)  # Retângulo laranja deitado
        else:
            # Desenha o personagem em pé
            pyxel.rect(self.x, self.y, self.width, self.height, 9)  # Retângulo laranja em pé