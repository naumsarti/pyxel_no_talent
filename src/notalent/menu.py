import pyxel

class Menu:
    def __init__(self):
        self.blink_timer = 0
        self.transition_timer = 0
        self.is_transitioning = False

    def update(self, player, change_state_callback):
        self.blink_timer += 1

        # Inicia a transição ao pressionar ENTER
        if pyxel.btnp(pyxel.KEY_RETURN) and not self.is_transitioning:
            self.is_transitioning = True
            self.transition_timer = 15  # Duração do piscar (frames)

        # Gerencia o efeito de piscar antes de mudar o estado
        if self.is_transitioning:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                player.is_sleeping = False
                player.y -= 4  # Ajusta a posição para o personagem "ficar em pé"
                change_state_callback("GAMEPLAY")

    def draw_world(self, player):
        # O 'Zzz' faz parte do mundo (fica fisicamente ao lado do jogador)
        if (self.blink_timer // 15) % 2 == 0:
            text_x = player.x + 18
            text_y = player.y - 4
            # Desenha a sombra primeiro deslocada em 1 pixel
            pyxel.text(x=text_x + 1, y=text_y + 1, s="Zzz...", col=1)
            # Desenha o texto principal por cima (Branco = 7)
            pyxel.text(x=text_x, y=text_y, s="Zzz...", col=7)

    def draw_ui(self):
        # O texto de instrução e o Flash são Interface (grudados na tela do monitor)
        text = "Pressione ENTER para Acordar"
        text_x = (160 - len(text) * 4) // 2
        text_y = 80
        # Desenha a sombra do texto de instrução
        pyxel.text(x=text_x + 1, y=text_y + 1, s=text, col=1)
        # Desenha o texto principal por cima (Branco = 7)
        pyxel.text(x=text_x, y=text_y, s=text, col=7)

        # Desenha o efeito de flash branco na transição
        if self.is_transitioning and (self.transition_timer // 2) % 2 == 0:
            pyxel.cls(7)