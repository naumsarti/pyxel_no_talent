import pyxel

class BattleSystem:
    def __init__(self):
        # Opções de ataque
        self.options = ["Corte Bruto", "Corte Duplo", "---", "---"]
        self.selected = 0
        
        # Status
        self.player_hp = 130
        self.player_max_hp = 130
        self.player_mp = 50
        self.player_max_mp = 50
        
        # Inimigo fica recuado no topo direito
        self.boss_x = 105
        self.boss_y = 2
        self.boss_w = 48
        self.boss_h = 56

        # MC fica bem posicionado no canto inferior esquerdo, saindo de trás do menu
        self.player_x = 5
        self.player_y = 37
        self.player_w = 48
        self.player_h = 48

        self.state = "MENU" # Estados: MENU, ATK_DIAGONAL, ATK_DUPLO, BOSS_TEXT, BOSS_ULTIMATE, END
        self.anim_timer = 0
        self.turn = 0
        
        # As falas que ele diz nos turnos 1, 2, 3 e 4
        self.taunts = [
            "Seu nome e Ban, nao e?",
            "So lhe resta forca fisica?",
            "Hahaha! Sem talento e sem habilidade.",
            "Esse mundo e realmente grande."
        ]
        self.visible_chars = 0
        self.text_speed = 2
        self.frame_counter = 0
        # Flag que avisará o main.py que a batalha encerrou
        self.is_finished = False

    def update(self):
        if self.state == "MENU":
            # Navegação no menu de combate
            if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
                if self.selected in [0, 2]:
                    self.selected += 1
                else:
                    self.selected -= 1
                    
            elif pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
                if self.selected in [0, 2]:
                    self.selected += 1
                else:
                    self.selected -= 1

            elif pyxel.btnp(pyxel.KEY_D) or pyxel.btnp(pyxel.KEY_RIGHT):
                if self.selected in [0, 1]:
                    self.selected += 2
                    
            elif pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.KEY_LEFT):
                if self.selected in [2, 3]:
                    self.selected -= 2
                
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.options[self.selected] == "Corte Bruto":
                        self.state = "ATK_DIAGONAL"
                        self.anim_timer = 0
                        self.player_mp = max(0, self.player_mp - 5)
                elif self.options[self.selected] == "Corte Duplo":
                        self.state = "ATK_DUPLO"
                        self.anim_timer = 0
                        self.player_mp = max(0, self.player_mp - 10)
                elif self.options[self.selected] == "---":
                    return
                
        # Animação dos Golpes do MC
        elif self.state in ["ATK_DIAGONAL", "ATK_DUPLO"]:
            self.anim_timer += 1
            if self.anim_timer > 60: # Após 1 segundo (60 frames) de animação...
                # Verifica se é o 5º Turno fatal ou se ele ainda vai conversar
                if self.turn == 4:
                    self.state = "BOSS_ULTIMATE"
                else:
                    self.state = "BOSS_TEXT"
                    self.visible_chars = 0
                    self.frame_counter = 0
                self.anim_timer = 0

        # Turno do Boss (Conversando)
        elif self.state == "BOSS_TEXT":
            full_text = self.taunts[self.turn]
            if self.visible_chars < len(full_text):
                self.frame_counter += 1
                if self.frame_counter >= self.text_speed:
                    self.visible_chars += 1
                    self.frame_counter = 0
            
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.visible_chars < len(full_text):
                    self.visible_chars = len(full_text)
                else:
                    self.turn += 1
                    self.state = "MENU"

        # Turno do Boss
        elif self.state == "BOSS_ULTIMATE":
            self.anim_timer += 1
            if self.anim_timer == 45:
                self.player_hp = 0 # O Hit-Kill real zera o HP
            if self.anim_timer > 150:
                self.state = "END" # Vai para a tela preta

        # Encerramento total
        elif self.state == "END":
            self.is_finished = True
        
    def draw(self):
        if self.state == "END":
            pyxel.cls(0)
            return
        
        # Efeito de Tremor da Câmera no golpe final
        if self.state == "BOSS_ULTIMATE" and 45 <= self.anim_timer < 90:
            pyxel.camera(pyxel.rndi(-4, 4), pyxel.rndi(-4, 4))
        else:
            pyxel.camera(0, 0) # Reseta a câmera

        # Fundo da batalha
        pyxel.cls(11)
        # Desenho do Boss pisca quando atingido
        is_boss_blinking = self.state in ["ATK_DIAGONAL", "ATK_DUPLO"] and 15 < self.anim_timer < 45
        if is_boss_blinking and (self.anim_timer // 4) % 2 == 0:
            pass # Não desenha para criar o efeito de piscar
        else:
            pyxel.blt(self.boss_x, self.boss_y, 0, 48, 96, self.boss_w, self.boss_h, colkey=0)

        is_player_blinking = self.state == "BOSS_ULTIMATE" and 45 <= self.anim_timer < 90
        if is_player_blinking and (self.anim_timer // 4) % 2 == 0:
            pass
        else:
            pyxel.blt(self.player_x, self.player_y, 0, 0, 96, self.player_w, self.player_h, colkey=0)
        
        # CAIXA DE STATUS DO BOSS
        pyxel.rect(6, 8, 55, 28, 1)    # Fundo Azul Escuro
        pyxel.rectb(6, 8, 55, 28, 7)   # Borda Branca
        pyxel.text(10, 12, "ORGULHO", 8)    # Nome Vermelho
        pyxel.text(10, 20, "HP: ??/??", 7) # Texto Branco
        pyxel.text(10, 27, "MP: ??/??", 5) # MP do Boss oculto
        
        # CAIXA DE STATUS DO PROTAGONISTA
        pyxel.rect(98, 48, 56, 28, 1)
        pyxel.rectb(98, 48, 56, 28, 7)
        pyxel.text(102, 52, "BAN", 7) 
        pyxel.text(102, 60, f"HP:{self.player_hp}/{self.player_max_hp}", 7)
        pyxel.text(102, 67, f"MP:{self.player_mp}/{self.player_max_mp}", 12)
        
        # MENU DE AÇÕES
        pyxel.rect(0, 85, 160, 35, 1)
        pyxel.rectb(0, 85, 160, 35, 7)
        pyxel.line(0, 85, 160, 85, 7) # Sombra superior

        # Menu e Diálogo do Boss
        if self.state in ["MENU", "ATK_DIAGONAL", "ATK_DUPLO", "BOSS_ULTIMATE"]:
            pyxel.rect(0, 85, 160, 35, 1)
            pyxel.rectb(0, 85, 160, 35, 7)
            pyxel.line(0, 85, 160, 85, 7) 
            positions = [(15, 92), (15, 104), (90, 92), (90, 104)]
            for i, opt in enumerate(self.options):
                x, y = positions[i]
                if i == self.selected:
                    pyxel.text(x, y, "> " + opt if opt != "---" else "> ---", 10 if opt != "---" else 13)
                else:
                    pyxel.text(x + 8, y, opt, 7 if opt != "---" else 5)
        
        elif self.state == "BOSS_TEXT":
            pyxel.rect(0, 85, 160, 35, 7)
            pyxel.line(0, 85, 160, 85, 0)
            pyxel.text(5, 90, "ORGULHO", 8)
            animated_text = self.taunts[self.turn][:self.visible_chars]
            pyxel.text(5, 102, animated_text, 0)
            if self.visible_chars >= len(self.taunts[self.turn]):
                if (pyxel.frame_count // 15) % 2 == 0:
                    pyxel.text(145, 108, "V", 0)

        # Ataques e Danos
        if self.state == "ATK_DIAGONAL":
            if self.anim_timer < 15:
                # Corte
                pyxel.line(self.boss_x, self.boss_y, self.boss_x + self.boss_w, self.boss_y + self.boss_h, 7)
                pyxel.line(self.boss_x + 1, self.boss_y, self.boss_x + self.boss_w + 1, self.boss_y + self.boss_h, 10)
            elif self.anim_timer < 60:
                # Dano flutuante (sobe suavemente)
                float_y = self.boss_y + 20 - (self.anim_timer - 15) // 2
                pyxel.text(self.boss_x + 15, float_y, "25", 8)
                
        elif self.state == "ATK_DUPLO":
            if self.anim_timer < 10:
                # Primeiro Corte
                pyxel.line(self.boss_x, self.boss_y, self.boss_x + self.boss_w, self.boss_y + self.boss_h, 7)
            elif self.anim_timer < 20:
                # Segundo Corte
                pyxel.line(self.boss_x + self.boss_w, self.boss_y, self.boss_x, self.boss_y + self.boss_h, 7)
            elif self.anim_timer < 60:
                # Dano Duplo flutuante
                float_y = self.boss_y + 20 - (self.anim_timer - 20) // 2
                pyxel.text(self.boss_x + 5, float_y, "15", 8)
                pyxel.text(self.boss_x + 25, float_y + 10, "15", 8)
                
        elif self.state == "BOSS_ULTIMATE":
            if self.anim_timer < 45:
                pyxel.line(self.player_x - 10, self.player_y - 10, self.player_x + 60, self.player_y + 60, 8)
                pyxel.line(self.player_x + 60, self.player_y - 10, self.player_x - 10, self.player_y + 60, 8)
                
            elif self.anim_timer < 90:
                pyxel.line(self.player_x - 10, self.player_y - 10, self.player_x + 60, self.player_y + 60, 8)
                pyxel.line(self.player_x + 60, self.player_y - 10, self.player_x - 10, self.player_y + 60, 8)
                pyxel.text(self.player_x + 18, self.player_y + 15, "130", 8)
