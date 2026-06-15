import pyxel

class PauseMenu:
    def __init__(self):
        self.options = ["Continuar", "Status", "Inventario", "Mapa", "Reiniciar", "Sair"]
        self.selected = 0
        self.msg_timer = 0  # Timer para mostrar a mensagem de "Em breve"

    def update(self, game):
        # Navegação para Cima/Baixo
        if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
            self.selected = (self.selected - 1) % len(self.options)
        elif pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
            self.selected = (self.selected + 1) % len(self.options)

        # Selecionar opção
        if pyxel.btnp(pyxel.KEY_RETURN):
            choice = self.options[self.selected]
            
            if choice == "Continuar":
                game.change_state("GAMEPLAY")
            
            elif choice == "Reiniciar":
                game.reset_game() # Chama o reset total
                self.selected = 0 # Volta o cursor da pausa para a primeira opção
            
            elif choice == "Sair":
                pyxel.quit()
            
            else:
                # Se for Status, Inventario ou Mapa, ativa a mensagem temporária (60 frames = 2 seg)
                self.msg_timer = 60 

    def draw(self, player):
        # Desenha o fundo do menu de pausa
        pyxel.rect(10, 10, 140, 100, 0) # Fundo preto
        pyxel.rectb(10, 10, 140, 100, 7) # Borda branca

        # Título do Menu
        pyxel.text(65, 15, "PAUSADO", 7)
        pyxel.line(10, 23, 150, 23, 7)

        # Desenha as opções na esquerda
        for i, opt in enumerate(self.options):
            # Cor: Amarelo se selecionado, Cinza se inativo, Branco se normal
            if i == self.selected:
                color = 10  # Amarelo
                pyxel.text(18, 32 + i * 10, ">", color)
            elif opt in ["Status", "Inventario", "Mapa"]:
                color = 13  # Cinza para opções em desenvolvimento
            else:
                color = 7   # Branco
                
            pyxel.text(26, 32 + i * 10, opt, color)

        # Mensagem de "Em desenvolvimento" no rodapé
        if self.msg_timer > 0:
            self.msg_timer -= 1
            pyxel.text(15, 95, "Funcao em desenvolvimento!", 8) # Texto vermelho

        # Personagem ampliado na direita
        scale = 3  # Multiplicador de tamanho
        zoom_x = 90
        zoom_y = 40
        u = player.get_current_u()
        v = 0 # Linha do sprite do player no banco de imagens

        # Lemos os pixels do banco de imagens e desenhamos retângulos para ampliar
        for i in range(16):
            for j in range(16):
                pixel_color = pyxel.image(0).pget(u + i, v + j)
                if pixel_color != 0: # 0 é a cor transparente (colkey)
                    pyxel.rect(zoom_x + i * scale, zoom_y + j * scale, scale, scale, pixel_color)