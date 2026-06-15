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

    def draw_text_with_shadow(self, x, y, text, col_main=1, col_shadow=7):
        """Função auxiliar para desenhar o texto com uma sombra azul atrás."""
        pyxel.text(x + 1, y + 1, text, col_shadow)
        pyxel.text(x, y, text, col_main)

    def draw_world(self, player):
        # Base de onde os balões de Z vão começar a aparecer ao lado do jogador
        base_x = player.x + 18
        base_y = player.y - 4

        # Controla a velocidade do ciclo de ronco (0 a 79 frames)
        cycle_frame = self.blink_timer % 80

        # Aparece a partir do frame 15 e fica visível até o final do ciclo (frame 75)
        if 15 <= cycle_frame < 75:
            self.draw_text_with_shadow(base_x, base_y, "z")

        # Só aparece a partir do frame 35
        if 35 <= cycle_frame < 75:
            self.draw_text_with_shadow(base_x + 5, base_y - 1, "z")

        # Só aparece a partir do frame 55
        if 55 <= cycle_frame < 75:
            self.draw_text_with_shadow(base_x + 10, base_y - 2, "Z")
        
    def draw_ui(self):
        # O texto de instrução e o Flash são Interface (grudados na tela do monitor)
        text = "Pressione ENTER para Acordar"
        text_x = (160 - len(text) * 4) // 2
        text_y = 90
        # Desenha a sombra do texto de instrução
        self.draw_text_with_shadow(text_x, text_y, text)

        # Desenha o efeito de flash branco na transição
        if self.is_transitioning and (self.transition_timer // 2) % 2 == 0:
            pyxel.cls(7)