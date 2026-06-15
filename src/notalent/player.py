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

    def update(self, game):
        if self.is_sleeping:
            return

        is_moving = False
        next_x = self.x
        next_y = self.y
        # Hitbox (caixa de colisão) menor que o corpo inteiro.
        hit_left = 2     # Dá 2 pixels de folga no ombro esquerdo
        hit_right = 13    # Dá 2 pixels de folga no ombro direito
        hit_top = 12       # Ignora a cabeça inteira! (Colisão começa da cintura pra baixo)
        hit_bottom = 15   # Bate exatamente na sola do pé

        # Movimentação restrita a 4 direções
        if pyxel.btn(pyxel.KEY_W):
            next_y -= self.speed
            self.direction = "up"
            is_moving = True
            if game.is_solid(self.x + hit_left, next_y + hit_top) or game.is_solid(self.x + hit_right, next_y + hit_top):
                is_moving = False
            else:
                self.y = next_y
        elif pyxel.btn(pyxel.KEY_S):
            next_y += self.speed
            self.direction = "down"
            is_moving = True
            if game.is_solid(self.x + hit_left, next_y + hit_bottom) or game.is_solid(self.x + hit_right, next_y + hit_bottom):
                is_moving = False
            else:
                self.y = next_y
        elif pyxel.btn(pyxel.KEY_A):
            next_x -= self.speed
            self.direction = "left"
            is_moving = True
            if game.is_solid(next_x + hit_left, self.y + hit_top) or game.is_solid(next_x + hit_left, self.y + hit_bottom):
                is_moving = False
            else:
                self.x = next_x
        elif pyxel.btn(pyxel.KEY_D):
            next_x += self.speed
            self.direction = "right"
            is_moving = True
            if game.is_solid(next_x + hit_right, self.y + hit_top) or game.is_solid(next_x + hit_right, self.y + hit_bottom):
                is_moving = False
            else:
                self.x = next_x

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
        self.x = max(0, min(self.x, 832 - self.width))
        self.y = max(0, min(self.y, 128 - self.height))

    def get_current_u(self):
        """Retorna a coordenada X (u) do sprite atual para o sistema de zoom ler."""
        # Onde começa o primeiro frame de cada grupo de animação
        direction_base_u = {
            "down":  0,    
            "up":    48,   
            "left":  96,   
            "right": 128   
        }
        return direction_base_u[self.direction] + (self.walk_frame * 16)
    
    def draw(self):
        # Calcula a posição X (u) somando 16 pixels para cada frame que avança
        u = self.get_current_u()
        
        if self.is_sleeping:
            # Se estiver dormindo, desenha o frame parado de frente (u=16)
            pyxel.blt(self.x, self.y, 0, 160, 0, 160, 16, colkey=0)
        else:
            # Desenha o sprite correto de forma direta, sempre com largura positiva (16)
            pyxel.blt(self.x, self.y, 0, u, 0, 16, 16, colkey=0)