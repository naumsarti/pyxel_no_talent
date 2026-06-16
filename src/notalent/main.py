import pyxel
from player import Player
from menu import Menu
from camera import Camera
from pause import PauseMenu
from boss import Boss
from dialogue import DialogueBox
from battle import BattleSystem

class Game:
    def __init__(self):
        # Inicializa a tela no tamanho 160x120 solicitado
        pyxel.init(160, 120, title="No Talent")
        pyxel.load("../assets/resource.pyxres")
        # Estado inicial do jogo
        self.reset_game()

        self.pause_menu = PauseMenu()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Recria todos os objetos do zero, como se ligasse o videogame agora."""
        self.camera = Camera(screen_w=160, screen_h=120, map_w=832, map_h=128)
        self.player = Player(46, 64)
        self.menu = Menu()
        self.boss = Boss(672, 60)
        # Flag para garantir que o evento só acontece uma vez!
        self.boss_event_triggered = False
        self.dialogue = DialogueBox()
        self.battle = BattleSystem()
        self.transition_timer = 0

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
                # Verifica se o jogador cruzou o X e se o evento ainda não ocorreu
                if self.player.x >= 616 and not self.boss_event_triggered:
                    self.boss_event_triggered = True  # Marca que o evento já começou
                    self.change_state("CINEMATIC")    # Rouba o controle do jogador
                    # Prepara a lista de falas (Nome, Texto)
                    # O limite de largura da tela é de ~35 letras por linha
                    script_inicial = [
                        ("Orgulho", "Hmm?"), ("Orgulho", "O que e isso?"), ("Orgulho", "..."), ("Orgulho", "HAHAHA! VOCE E UM AMALDICOADO!"),
                        ("Ban", "..."), ("Ban", "O que disse?!"),
                        ("Orgulho", "HAHAHA! QUE EXISTENCIA MISERAVEL!"),
                        ("Ban", "Seu... Filho da p*!")
                    ]
                    # Inicia o diálogo. Quando acabar, muda o estado para BATTLE
                    self.dialogue.start(script_inicial, lambda: self.start_battle_transition())

                else:
                    self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)
                
        elif self.state == "PAUSED":
            # Passamos o jogo para o menu de pausa controlar as opções
            self.pause_menu.update(self)
        
        elif self.state == "CINEMATIC":
            # A câmera ignora o Player e passa a focar nas coordenadas do Boss
            self.camera.update(self.boss.x, self.boss.y, self.boss.width, self.boss.height, smooth=0.03)
            self.dialogue.update()

        elif self.state == "BATTLE_TRANSITION":
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.change_state("BATTLE")
                
        elif self.state == "BATTLE":
            self.battle.update()

    def start_battle_transition(self):
        """Ativa um flash na tela por 45 frames antes de entrar na batalha."""
        self.transition_timer = 45
        self.change_state("BATTLE_TRANSITION")

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
        # O cenário de fundo e os personagens só aparecem se NÃO estiver na tela de batalha pura
        if self.state not in ["BATTLE", "BATTLE_TRANSITION"]:
            self.camera.start()
            self.draw_scenery()
            self.boss.draw()

            if self.state == "MENU":
                self.player.draw(self.menu.blink_timer)
                self.menu.draw_world(self.player)
            else:
                self.player.draw()

            self.camera.stop()
            # INTERFACE (PAUSE)
            if self.state == "MENU":
                self.menu.draw_ui()
            elif self.state == "PAUSED":
                # Desenha o menu de pausa por cima de tudo
                self.pause_menu.draw(self.player)
            elif self.state == "CINEMATIC":
                self.dialogue.draw()
                
        elif self.state == "BATTLE_TRANSITION":
            # Pisca a tela rapidamente alternando entre Branco (7) e Preto (0)
            if (self.transition_timer // 3) % 2 == 0:
                pyxel.cls(7)
            else:
                pyxel.cls(0)
                    
        elif self.state == "BATTLE":
            # Desenha olayout de Batalha
            self.battle.draw()
            
if __name__ == "__main__":
    Game()