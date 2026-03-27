# 🚀 Deep Space Pilot - 3D Starship Combat

![Status](https://img.shields.io/badge/Status-Finalizado-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Lib](https://img.shields.io/badge/Library-Tkinter-orange)

Um jogo de combate espacial "surreal" desenvolvido inteiramente em **Python** utilizando apenas a biblioteca padrão **Tkinter**. O projeto simula um ambiente 3D através de cálculos de projeção de perspectiva, sem a necessidade de engines externas como PyGame ou OpenGL.

---

## 🌌 Sobre o Projeto
Este projeto foi criado como uma demonstração de habilidades em **Matemática Aplicada à Computação** e **Interface Gráfica**. O desafio era criar uma experiência imersiva de "Warp Speed" (velocidade da luz) onde o jogador controla uma nave para destruir inimigos em um campo de estrelas infinito.

### 🎨 Diferenciais
*   **Engine 3D "Vanilla":** Projeção de coordenadas $(X, Y, Z)$ para $(X, Y)$ de tela em tempo real.
*   **Efeito de Profundidade:** Objetos aumentam de tamanho e brilho conforme se aproximam do observador.
*   **Performance:** Renderização otimizada no `tk.Canvas` para manter 60 FPS.
*   **Zero Instalações:** Utiliza apenas bibliotecas nativas do Python (Tkinter + PIL).

---

## 🕹️ Como Jogar

### Pré-requisitos
1. Certifique-se de ter o **Python 3** instalado.
2. Certifique-se de ter a imagem `avião.png` na mesma pasta do script.
3. (Opcional) Instale o Pillow se o seu Python não tiver suporte nativo a PNG:
   ```bash
   pip install Pillow
