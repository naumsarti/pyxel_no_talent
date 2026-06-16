import pyxel

class BattleSystem:
    def __init__(self):
        # Opções de ataque
        self.options = ["Corte Diagonal", "Corte Duplo", "---", "---"]
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

    def update(self):
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
            if self.options[self.selected] == "---":
                return
            # Por enquanto, apenas avisa que clicou
            pass

    def draw(self):
        # Fundo da batalha
        pyxel.cls(11)

        pyxel.blt(self.boss_x, self.boss_y, 0, 48, 96, self.boss_w, self.boss_h, colkey=0)

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

        # Desenha as opções dispostas em duas colunas
        positions = [
            (15, 92),  # Slot 1 (Corte Diagonal)
            (15, 104), # Slot 2 (Corte Duplo)
            (90, 92),  # Slot 3 (Vazio)
            (90, 104)  # Slot 4 (Vazio)
        ]
        
        # Desenha as opções
        for i, opt in enumerate(self.options):
            x, y = positions[i]
            # Se for o slot selecionado atual
            if i == self.selected:
                if opt == "---":
                    pyxel.text(x, y, "> ---", 13) # Cursor cinza claro se for slot vazio
                else:
                    pyxel.text(x, y, "> " + opt, 10) # Cursor Amarelo para golpes reais
            else:
                if opt == "---":
                    pyxel.text(x + 8, y, opt, 5) # Texto cinza escuro para slots vazios apagados
                else:
                    pyxel.text(x + 8, y, opt, 7) # Texto branco para golpes normais