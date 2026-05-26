import pyxel
from player import Player
from menu import Menu

class Game:
    def __init__(self):
        # Inicializa a tela no tamanho 160x120 solicitado
        pyxel.init(160, 120, title="No Talent")
        
        # Estado inicial do jogo
        self.state = "MENU"  # Estados possíveis: 'MENU', 'GAMEPLAY'
        
        # Instancia as classes do projeto
        self.player = Player(46, 64)  # Posicionado embaixo da árvore
        self.menu = Menu()
        
        pyxel.run(self.update, self.draw)

    def change_state(self, new_state):
        self.state = new_state

    def update(self):
        if self.state == "MENU":
            self.menu.update(self.player, self.change_state)
        elif self.state == "GAMEPLAY":
            self.player.update()

    def draw_scenery(self):
        # Chão verde (Grama)
        pyxel.cls(11)
        
        # Árvore (Cenário simples usando formas geométricas)
        # Tronco
        pyxel.rect(38, 45, 12, 20, 4)
        # Folhas (Copas em círculos)
        pyxel.circ(35, 35, 12, 3)
        pyxel.circ(53, 35, 12, 3)
        pyxel.circ(44, 25, 14, 3)

    def draw(self):
        # Desenha o cenário de fundo compartilhado por ambos os estados
        self.draw_scenery()
        
        # Desenha o jogador (funciona tanto para deitado quanto em pé)
        self.player.draw()

        # Renderiza a camada do menu se estiver nessa tela
        if self.state == "MENU":
            self.menu.draw(self.player)

# Executa o jogo
if __name__ == "__main__":
    Game()