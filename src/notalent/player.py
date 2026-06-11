import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.is_sleeping = True
        self.direction = "down"  # 'up', 'down', 'left', 'right'
        
        # Dimensões do personagem
        self.width = 16
        self.height = 16

        self.anim_tick = 0  # Só aumenta quando o jogador se move
        self.walk_frame = 0 # Frame final que será desenhado

    def update(self):
        if self.is_sleeping:
            return

        is_moving = False
        # Movimentação restrita a 4 direções
        # Prioriza uma direção por vez para impedir movimento diagonal
        if pyxel.btn(pyxel.KEY_W):
            self.y -= self.speed
            self.direction = "up"
            is_moving = True
        elif pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
            self.direction = "down"
            is_moving = True
        elif pyxel.btn(pyxel.KEY_A):
            self.x -= self.speed
            self.direction = "left"
            is_moving = True
        elif pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
            self.direction = "right"
            is_moving = True

        # Lógica de animação baseada nos frames
        if is_moving:
            self.anim_tick += 1 # O tempo da animação só corre se houver movimento!
            
            # O número 6 dita a velocidade (maior = mais lento).
            frame_index = (self.anim_tick // 6)

            if self.direction in ["down", "up"]:
                # Alterna estritamente entre Passo 1 (0) e Passo 2 (2)
                # O % 2 gera 0 ou 1. Multiplicando por 2, temos apenas 0 ou 2 (pula o 1!)
                self.walk_frame = (frame_index % 2) * 2
            else:
                # Para os lados (left, right) 2 frames (0, 1)
                self.walk_frame = frame_index % 2
        else:
            # Quando PARADO, define o frame correto para cada direção:
            if self.direction in ["down", "up"]:
                self.walk_frame = 1  # O frame do meio (16 para frente, 64 para trás) é o parado
            else:
                self.walk_frame = 0  # O primeiro frame (96 para esquerda, 128 para direita) é o parado

        # Limites do MAPA inteiro (704x128)
        self.x = max(0, min(self.x, 704 - self.width))
        self.y = max(0, min(self.y, 128 - self.height))

    def draw(self):
         # Onde começa o primeiro frame de cada grupo de animação
        direction_base_u = {
            "down":  0,    # Começa no pixel 0
            "up":    48,   # Começa no pixel 48
            "left":  96,   # Começa no pixel 96
            "right": 128   # Começa no pixel 128
        }

        # Calcula a posição X (u) somando 16 pixels para cada frame que avança
        u = direction_base_u[self.direction] + (self.walk_frame * 16)
        
        if self.is_sleeping:
            # Se estiver dormindo, desenha o frame parado de frente (u=16)
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, colkey=0)
        else:
            # Desenha o sprite correto de forma direta, sempre com largura positiva (16)
            pyxel.blt(self.x, self.y, 0, u, 0, 16, 16, colkey=0)