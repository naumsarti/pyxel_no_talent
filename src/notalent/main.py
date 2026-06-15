import pyxel
from player import Player
from menu import Menu
from camera import Camera
from pause import PauseMenu

class Game:
    def __init__(self):
        # Inicializa a tela no tamanho 160x120 solicitado
        pyxel.init(160, 120, title="No Talent")
        pyxel.load("../../assets/resource.pyxres")
        # Estado inicial do jogo
        self.state = "MENU"  # Estados possíveis: 'MENU', 'GAMEPLAY'
        
        # Instancia a câmera passando as dimensões
        self.camera = Camera(screen_w=160, screen_h=120, map_w=832, map_h=128)

        # Instancia as classes do projeto
        self.state = "MENU"
        self.player = Player(46, 64)  # Posicionado embaixo da árvore
        self.menu = Menu()
        self.pause_menu = PauseMenu()
        
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Recria todos os objetos do zero, como se ligasse o videogame agora."""
        self.camera = Camera(screen_w=160, screen_h=120, map_w=832, map_h=128)
        self.player = Player(46, 64)
        self.menu = Menu()
        self.state = "MENU"

    def change_state(self, new_state):
        self.state = new_state

    def is_solid(self, x, y):
        """Recebe uma coordenada em pixels e diz se tem colisão ali."""
        # 1. Converte pixels para a célula correspondente no Tilemap (divisão inteira por 8)
        tile_x = int(x // 8)
        tile_y = int(y // 8)
        
        # 2. Pega o índice do tile nessa posição do mapa (tm=0)
        # O Pyxel retorna uma tupla (u, v) correspondente ao local do sprite no Image Bank
        tile_data = pyxel.tilemap(0).pget(tile_x, tile_y)
        
        # tile_data[0] é a coluna (u)
        # tile_data[1] é a linha (v) no banco de imagens
        sprite_v = tile_data[1]
        
        # 3. Regra de colisão baseada nas linhas de blocos (de 8 a 11 inclusive)
        if 8 <= sprite_v <= 11:
            return True # É colisão! Ele bloqueia o jogador.

        return False

    def update(self):
        if self.state == "MENU":
            self.menu.update(self.player, self.change_state)
            self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)
        elif self.state == "GAMEPLAY":
            # Ao apertar ENTER durante o jogo, vai para a pausa!
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.change_state("PAUSED")
            else:
                self.player.update(self)
                self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)
                
        elif self.state == "PAUSED":
            # Passamos o jogo para o menu de pausa controlar as opções
            self.pause_menu.update(self)

    def draw_scenery(self):
        pyxel.cls(11)
        
        # --- DESENHA O TILEMAP ---
        # tm: índice do tilemap (geralmente 0 no Pyxel Editor)
        # x, y: posição na tela onde o mapa começa a ser desenhado (0, 0)
        # u, v: coordenada inicial dentro do tilemap (em células/tiles, ex: de onde começa a câmera)
        # w, h: largura e altura do mapa que será renderizado (em células/tiles)
        # 160x120 pixels equivalem a 20x15 tiles de tamanho 8x8
        pyxel.bltm(x=0, y=0, tm=0, u=0, v=0, w=832, h=128)

    def draw(self):
        self.camera.start()
        self.draw_scenery()
        self.player.draw()

        if self.state == "MENU":
            self.menu.draw_world(self.player)

        # --- INTERFACE (UI) ---
        self.camera.stop()
        if self.state == "MENU":
            self.menu.draw_ui()
        elif self.state == "PAUSED":
            # Desenha o menu de pausa por cima de tudo
            self.pause_menu.draw(self.player)
            
if __name__ == "__main__":
    Game()