import pyxel

class Camera:
    def __init__(self, screen_w, screen_h, map_w, map_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.map_w = map_w
        self.map_h = map_h
        
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y, target_w, target_h, smooth=1):
        # Calcula a posição ideal para centralizar o alvo
        ideal_x = target_x + (target_w // 2) - (self.screen_w // 2)
        ideal_y = target_y + (target_h // 2) - (self.screen_h // 2)
        
        # Trava a câmera dentro dos limites do mapa (Clamp)
        target_clamp_x = max(0, min(ideal_x, self.map_w - self.screen_w))
        target_clamp_y = max(0, min(ideal_y, self.map_h - self.screen_h))

        # Se for menor (ex: 0.05), ela desliza suavemente até o destino
        self.x += (target_clamp_x - self.x) * smooth
        self.y += (target_clamp_y - self.y) * smooth

    def start(self):
        """Aplica o deslocamento da câmera para o mundo."""
        pyxel.camera(self.x, self.y)

    def stop(self):
        """Reseta a câmera para desenhar elementos fixos na tela (UI)."""
        pyxel.camera()