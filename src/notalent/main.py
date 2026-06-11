import pyxel
from player import Player
from menu import Menu
from camera import Camera

class Game:
    def __init__(self):
        # Inicializa a tela no tamanho 160x120 solicitado
        pyxel.init(160, 120, title="No Talent")
        
        pyxel.load("../../assets/resource.pyxres")
        # Estado inicial do jogo
        self.state = "MENU"  # Estados possíveis: 'MENU', 'GAMEPLAY'
        
        # Instancia a câmera passando as dimensões
        self.camera = Camera(screen_w=160, screen_h=120, map_w=792, map_h=128)

        # Instancia as classes do projeto
        self.state = "MENU"
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

        # Atualiza a câmera passando a posição e tamanho do jogador
        self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)

    def draw_scenery(self):
        pyxel.cls(11)
        
        # --- DESENHA O TILEMAP ---
        # tm: índice do tilemap (geralmente 0 no Pyxel Editor)
        # x, y: posição na tela onde o mapa começa a ser desenhado (0, 0)
        # u, v: coordenada inicial dentro do tilemap (em células/tiles, ex: de onde começa a câmera)
        # w, h: largura e altura do mapa que será renderizado (em células/tiles)
        # 160x120 pixels equivalem a 20x15 tiles de tamanho 8x8
        pyxel.bltm(x=0, y=0, tm=0, u=0, v=0, w=792, h=128)

    def draw(self):
        self.camera.start()

        # Desenha o cenário de fundo compartilhado por ambos os estados
        self.draw_scenery()
        # Desenha o jogador (funciona tanto para deitado quanto em pé)
        self.player.draw()

        if self.state == "MENU":
            self.menu.draw_world(self.player)

        # --- INTERFACE (UI) ---
        self.camera.stop()
        if self.state == "MENU":
            self.menu.draw_ui()

if __name__ == "__main__":
    Game()