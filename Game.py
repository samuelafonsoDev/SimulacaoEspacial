import tkinter as tk
from PIL import Image, ImageTk
import random
import math
import os

class SpaceWar3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Starship Combat - Projeto IA")
        self.width = 1000
        self.height = 700
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Configurações de Jogo
        self.game_over = False
        self.score = 0
        self.fov = 500
        self.speed = 15
        
        # Listas de Objetos
        self.stars = []
        self.enemies = []
        self.lasers = []
        
        # Carregar Jogador (Avião.png)
        self.setup_player()
        
        # Interface
        self.score_display = self.canvas.create_text(20, 20, text="SCORE: 0", fill="white", 
                                                    font=("Arial", 18, "bold"), anchor="w")

        self.setup_controls()
        self.initialize_environment()
        self.update_game()

    def setup_player(self):
        """Carrega a imagem avião.png do diretório local"""
        self.player_x = self.width // 2
        self.player_y = self.height - 120
        
        # Tenta localizar a imagem no mesmo diretório do script
        script_dir = os.path.dirname(__file__)
        img_path = os.path.join(script_dir, "avião.png")
        
        try:
            # Abre e redimensiona a imagem para caber bem no jogo
            pil_img = Image.open(img_path).convert("RGBA")
            pil_img = pil_img.resize((70, 70), Image.Resampling.LANCZOS)
            self.player_img = ImageTk.PhotoImage(pil_img)
            
            self.player = self.canvas.create_image(self.player_x, self.player_y, image=self.player_img)
            print("Imagem 'avião.png' carregada com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            # Se falhar, cria um triângulo verde como reserva (fallback)
            self.player = self.canvas.create_polygon(0, -20, 20, 20, -20, 20, fill="#00ff00")
            self.canvas.move(self.player, self.player_x, self.player_y)

    def setup_controls(self):
        self.keys = set()
        self.root.bind("<KeyPress>", lambda e: self.keys.add(e.keysym.lower()))
        self.root.bind("<KeyRelease>", lambda e: self.keys.discard(e.keysym.lower()))
        self.root.bind("<space>", lambda e: self.shoot())

    def initialize_environment(self):
        for _ in range(80):
            x = random.uniform(-self.width, self.width)
            y = random.uniform(-self.height, self.height)
            z = random.uniform(1, self.fov)
            id = self.canvas.create_oval(0,0,0,0, fill="white", outline="")
            self.stars.append([x, y, z, id])

    def spawn_enemy(self):
        if len(self.enemies) < 8 and not self.game_over:
            x = random.uniform(-self.width, self.width)
            y = random.uniform(-self.height, self.height)
            z = self.fov
            id = self.canvas.create_oval(0,0,0,0, fill="#ff4444", outline="white", width=2)
            self.enemies.append([x, y, z, id])

    def shoot(self):
        if not self.game_over:
            # O laser sai da ponta do avião
            lx = (self.player_x - self.width//2) 
            ly = (self.player_y - self.height//2) - 30
            lz = 10 
            id = self.canvas.create_line(0,0,0,0, fill="#00ffff", width=3)
            self.lasers.append([lx, ly, lz, id])

    def update_game(self):
        if self.game_over: return

        cx, cy = self.width // 2, self.height // 2

        # Movimentação suave
        m = 12
        if 'left' in self.keys or 'a' in self.keys: self.player_x = max(50, self.player_x - m)
        if 'right' in self.keys or 'd' in self.keys: self.player_x = min(self.width-50, self.player_x + m)
        if 'up' in self.keys or 'w' in self.keys: self.player_y = max(50, self.player_y - m)
        if 'down' in self.keys or 's' in self.keys: self.player_y = min(self.height-50, self.player_y + m)
        
        self.canvas.coords(self.player, self.player_x, self.player_y)

        # Estrelas
        for s in self.stars:
            s[2] -= self.speed
            if s[2] <= 1: s[2] = self.fov
            k = self.fov / s[2]
            px, py = s[0]*k + cx, s[1]*k + cy
            self.canvas.coords(s[3], px, py, px+2, py+2)

        # Lasers
        for l in self.lasers[:]:
            l[2] += 40
            if l[2] > self.fov:
                self.canvas.delete(l[3])
                self.lasers.remove(l)
                continue
            k = self.fov / l[2]
            px, py = l[0]*k + cx, l[1]*k + cy
            self.canvas.coords(l[3], px, py, px, py - 20)

        # Inimigos e Colisões
        if random.random() < 0.06: self.spawn_enemy()
        
        for e in self.enemies[:]:
            e[2] -= self.speed * 0.7
            if e[2] <= 1:
                self.canvas.delete(e[3])
                self.enemies.remove(e)
                continue

            k = self.fov / e[2]
            ex, ey = e[0]*k + cx, e[1]*k + cy
            r = max(5, (1 - e[2]/self.fov) * 50)
            self.canvas.coords(e[3], ex-r, ey-r, ex+r, ey+r)

            # Colisão com o Avião
            if e[2] < 60:
                dist = math.sqrt((ex - self.player_x)**2 + (ey - self.player_y)**2)
                if dist < r + 30:
                    self.die()

            # Colisão Laser vs Inimigo
            for l in self.lasers[:]:
                lk = self.fov / l[2]
                lpx, lpy = l[0]*lk + cx, l[1]*lk + cy
                if abs(l[2] - e[2]) < 50:
                    if abs(lpx - ex) < r and abs(lpy - ey) < r:
                        self.score += 100
                        self.canvas.itemconfig(self.score_display, text=f"SCORE: {self.score}")
                        if e[3] in self.canvas.find_all(): self.canvas.delete(e[3])
                        if e in self.enemies: self.enemies.remove(e)
                        self.canvas.delete(l[3])
                        if l in self.lasers: self.lasers.remove(l)

        self.root.after(20, self.update_game)

    def die(self):
        self.game_over = True
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black", alpha=0.5)
        self.canvas.create_text(self.width//2, self.height//2, text="AVIÃO ABATIDO", 
                               fill="red", font=("Arial", 40, "bold"))
        self.canvas.create_text(self.width//2, self.height//2 + 70, 
                               text=f"Pontuação: {self.score}\n\nFeche e abra para reiniciar", 
                               fill="white", font=("Arial", 16), justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    # Garante que o jogo não trave se a imagem for pesada
    root.resizable(False, False)
    app = SpaceWar3D(root)
    root.mainloop()