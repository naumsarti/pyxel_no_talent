# No Talent - Demonstração Pyxel

Este projeto foi desenvolvido como objeto de estudo e apresentação para demonstrar as capacidades da biblioteca **Pyxel** (um motor de jogos retrô para Python). O objetivo principal é servir como um exemplo prático do que a ferramenta consegue fazer, unindo mecânicas clássicas de RPG em um escopo reduzido e direto.

---
## Sobre o Projeto

"No Talent" é uma demonstração em estilo *Vertical Slice* de um RPG 8-bits. O jogo acompanha o protagonista Ban em um encontro roteirizado contra o demônio "Orgulho". A demonstração foca em mostrar a transição fluida entre exploração de mapa, eventos cinemáticos e um sistema de batalha por turnos.

---
## Recursos do Pyxel Demonstrados

* **Renderização Clássica:** Uso de limite de cores e resolução fixa de 160x120 pixels.
* **Tilemaps e Colisão:** Leitura de mapas e detecção de blocos sólidos para movimentação do jogador.
* **Máquina de Estados:** Controle de fluxo dinâmico entre exploração, menus de pausa, cenas de corte (cutscenes) e batalhas.
* **Sistemas de UI:** Caixas de texto dinâmicas com efeito de "máquina de escrever" e menus interativos.
* **Animação por Código:** Tremores de câmera, manipulação de frames de sprites e transições temporizadas.

---

## Como Jogar

### Pré-requisitos:
* **Python 3.x**
---
### 1. **Clone este repositório para o seu computador:**
```bash
git clone https://github.com/naumsarti/pyxel_no_talent.git
cd pyxel_no_talent
```
---
### 2. **Crie um Ambiente Virtual:**
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
---
### 3. **Instale a biblioteca Pyxel executando o comando:**
   ```bash
   pip install -r requirements.txt
   ```
---
### 4. **Rodar o Jogo:**
```bash
python src/notalent/main.py
```
---
## **Controles:**
* **W, A, S, D**: Movimentar o personagem e navegar nos menus.

* **ENTER**: Interagir, abrir menu de pause, avançar diálogos e confirmar opções.

* **SHIFT**: Correr (durante a exploração do mapa).