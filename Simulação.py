import tkinter as tk
import random
import math

class SurrealStarfield3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Hyperdrive - 3D Surreal Engine")
        
        # Configurações da Tela (Preto Profundo)
        self.width = 1000
        self.height = 700
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Configurações da Simulação
        self.num_stars = 350
        self.speed = 15          # Velocidade de aproximação
        self.stars = []          # Lista para guardar os dados das estrelas
        
        # Perspectiva e Centro da Tela
        self.fov = 400           # Field of View (Distância focal simulada)
        self.cx = self.width // 2
        self.cy = self.height // 2

        self.initialize_stars()
        self.animate()

    def initialize_stars(self):
        """Cria as estrelas iniciais em posições 3D aleatórias."""
        for _ in range(self.num_stars):
            # X, Y variam de negativo a positivo ao redor do centro
            # Z é a profundidade (0 até a distância focal máxima)
            x = random.uniform(-self.width * 2, self.width * 2)
            y = random.uniform(-self.height * 2, self.height * 2)
            z = random.uniform(1, self.fov)
            
            # Cria a forma gráfica no Canvas
            id = self.canvas.create_oval(0, 0, 0, 0, fill="white", outline="")
            self.stars.append([x, y, z, id])

    def animate(self):
        """Loop de animação principal: move e renderiza as estrelas."""
        
        # Limpa as estrelas que 'morreram' na iteração anterior de forma segura
        # (Neste algoritmo, reutilizamos as estrelas, então não precisamos limpar o canvas todo)

        for star in self.stars:
            # 1. Move a estrela em Z (aproximação)
            star[2] -= self.speed

            # 2. Se a estrela passou da tela (Z <= 1), reseta ela lá no fundo
            if star[2] <= 1:
                star[0] = random.uniform(-self.width * 2, self.width * 2)
                star[1] = random.uniform(-self.height * 2, self.height * 2)
                star[2] = self.fov

            # 3. Projeção 3D para 2D (A MÁGICA ACONTECE AQUI)
            # Fórmula padrão de perspectiva: X_tela = (X_3d * FOV) / Z_3d + Centro
            k = self.fov / star[2]
            px = star[0] * k + self.cx
            py = star[1] * k + self.cy

            # 4. Efeitos Visuais Baseados na Profundidade (Z)
            # Tamanho: Estrelas mais perto (Z menor) são maiores
            # Brilho/Cor: Mais perto são brancas, mais longe ficam cinzas (efeito névoa)
            
            # Calcula tamanho (r) entre 1 e 5 pixels
            r = max(1, (1 - star[2] / self.fov) * 5)
            
            # Calcula Brilho (0 a 255) baseado em Z
            brightness = int((1 - star[2] / self.fov) * 255)
            # Garante que não fica negativo e formata para Hexadecimal
            brightness = max(10, min(255, brightness))
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'

            # 5. Atualiza a posição e aparência do objeto no Canvas
            # create_oval precisa das coordenadas (x1, y1, x2, y2)
            self.canvas.coords(star[3], px - r, py - r, px + r, py + r)
            self.canvas.itemconfig(star[3], fill=color)

        # Próximo frame (aproximadamente 30-60 FPS dependendo da máquina)
        self.root.after(15, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    # Tenta maximizar a janela para maior imersão
    try:
        root.state('zoomed') # Windows
    except:
        try:
            root.attributes('-zoomed', True) # Linux
        except:
            pass # Mac ou erro, mantém geometry padrão
            
    app = SurrealStarfield3D(root)
    
    # Adiciona uma instrução simples na tela
    label = tk.Label(root, text="Tkinter 3D Engine - Efeito Warp Speed", 
                     fg="#333333", bg="black", font=("Arial", 10))
    label.place(x=10, y=10)
    
    root.mainloop()