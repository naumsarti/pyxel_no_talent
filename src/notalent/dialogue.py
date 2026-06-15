import pyxel

class DialogueBox:
    def __init__(self):
        self.messages = []
        self.current_index = 0
        self.is_active = False
        self.on_finish_callback = None
        self.visible_chars = 0       # Quantas letras estão aparecendo na tela agora
        self.text_speed = 2          # Velocidade: a cada X frames, revela 1 letra (menor = mais rápido)
        self.frame_counter = 0       # Conta os frames para saber quando soltar a próxima letra

    def start(self, messages, on_finish):
        """Inicia uma sequência de diálogos."""
        self.messages = messages
        self.current_index = 0
        self.is_active = False # Começa desativado para limpar e ligar com segurança
        self.visible_chars = 0
        self.frame_counter = 0
        self.is_active = True
        self.on_finish_callback = on_finish

    def update(self):
        if not self.is_active:
            return
        
        # Pega a frase inteira atual para saber o tamanho dela
        _, full_text = self.messages[self.current_index]
        # Se o texto ainda não terminou de aparecer, vamos revelando letra por letra
        if self.visible_chars < len(full_text):
            self.frame_counter += 1
            if self.frame_counter >= self.text_speed:
                self.visible_chars += 1
                self.frame_counter = 0

        # Avança o diálogo ao apertar ENTER
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Se apertar ENTER antes do texto acabar completa a frase instantaneamente
            if self.visible_chars < len(full_text):
                self.visible_chars = len(full_text)
            else:
                # Se o texto já estava completo, avança para a próxima frase
                self.current_index += 1
                self.visible_chars = 0  # Reseta para a próxima frase começar do zero
                self.frame_counter = 0
            # Se acabaram as frases, fecha o diálogo e chama a próxima ação
            if self.current_index >= len(self.messages):
                self.is_active = False
                if self.on_finish_callback:
                    self.on_finish_callback()

    def draw(self):
        if not self.is_active:
            return

        # Desenha a faixa branca no fundo (Y 85 até 120)
        pyxel.rect(0, 85, 160, 35, 7) # 7 é Branco
        pyxel.line(0, 85, 160, 85, 0) # Linha preta (0) na borda superior para destacar

        # Pega o nome do falante e o texto da frase atual
        speaker, full_text = self.messages[self.current_index]

        # Desenha o nome de quem está falando (Preto)
        pyxel.text(5, 90, f"{speaker}", 0)

        animated_text = full_text[:self.visible_chars]
        
        # Desenha a frase da pessoa logo abaixo (Preto)
        pyxel.text(5, 102, animated_text, 0)
        
        # Pisca uma setinha no canto direito para indicar que deve apertar ENTER
        if self.visible_chars == len(full_text):
            if (pyxel.frame_count // 15) % 2 == 0:
                pyxel.text(145, 108, "V", 0)