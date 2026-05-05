# 1º Trabalho de Computação Gráfica:
# Mebaformers - Simulação Celular

Uma simulação interativa de crescimento celular desenvolvida em **Python** e **Pygame**. O jogador assume o controle de uma ameba em um ambiente hostil, onde deve consumir nutrientes para crescer.

---

## Sobre o Projeto
O objetivo principal deste projeto foi explorar a implementação da lógica de jogo, física e renderização utilizando os recursos fundamentais dentro do Pygame. Diferente de motores prontos, toda a lógica de crescimento, detecção de proximidade e movimentação fluida foi implementada manualmente.

### Estrutura de Pastas
```
mebaformers/
├── lib/                        # Bilblioteca gráfica
│   ├── Motor_grafico.py        # setPixel e Clipping de segurança
│   ├── Preenchimento.py        # Scanline, Gradientes e Texturas
│   ├── Primitivas.py           # Bresenham, Clipping e Scanline
│   ├── Recorte.py              # Algoritmo de Cohen-Sutherland
│   ├── Transformacoes.py       # Matrizes 3x3 e Álgebra Linear
│   └── Viewports.py            # Mapeamento Viewport
├── polygons/                   # Entidades do Jogo
│   ├── ameba.py                # Geração procedural e animação
│   ├── food.py                 # Gerenciamento de comidas
│   └── minimap.py              # Lógica do radar/minimapa
├── utils/                      # Auxiliares
│   └── capture_key.py          # Input e Normalização de velocidade
└── main.py                     # Loop principal e integração
```

### Principais Funcionalidades:
O maior destaque deste projeto é que ele não utiliza as funções de desenho padrão do Pygame. Em vez disso, foi desenvolvida uma **pipeline gráfica própria**, processando a renderização pixel a pixel.
Para começar, a estrutura do código foi dividida em partes para cada funcionalidade.
Pasta **lib**
* `Motor_grafico.py`

<p></p>

A função base `setPixel` foi implementada com um sistema de **Clipping de Segurança**, garantindo que o motor gráfico nunca tente acessar coordenadas fora da superfície da janela, o que otimiza a estabilidade do software.

Para dar vida ao **Mebaformers**, foram implementados algoritmos clássicos que são a base da computação gráfica:
* **Bresenham (Retas):** Implementação otimizada para desenhar as bordas das amebas e elementos do cenário sem usar aritmética de ponto flutuante pesada.
* **Ponto Médio (Círculos e Elipses):** As células são renderizadas através da lógica de ponto médio, garantindo simetria perfeita na simulação.
* **Scanline Fill:** Um sistema de preenchimento por linhas de varredura que permite que as amebas tenham cores sólidas e opacas, processadas dinamicamente.
* **Sistema de Recorte (Clipping):** Para manter a performance, o jogo utiliza o algoritmo de Cohen-Sutherland. Isso permite que o motor identifique instantaneamente quais partes de uma célula ou linha estão fora da visão do jogador, descartando o processamento desnecessário de pixels invisíveis.

* `Preenchimento.py`

* **Interpolação de Cores (Gradientes):** Implementação de um sistema de interpolação linear para criar gradientes dinâmicos nas amebas. Isso permite que a célula mude de cor suavemente dependendo do seu estado de saúde ou evolução.
* **Mapeamento de Textura (UV Mapping):** O projeto conta com um algoritmo de `scanline_texture` que projeta coordenadas de textura (U, V) em polígonos arbitrários. Isso permite "vestir" as células com padrões orgânicos complexos.
* **Algoritmo de Flood Fill (Baseado em Pilha):** Para áreas de preenchimento irregular, foi implementada uma versão otimizada do **Flood Fill** usando uma estrutura de dados de pilha para evitar o estouro da memória (**Stack Overflow**) comum em versões recursivas.
* **Rasterização de Polígonos:** Uso do algoritmo de linha de varredura (**Scanline**) para identificar as interseções dos polígonos em cada linha da tela, garantindo que o preenchimento seja perfeito, sem falhas entre os pixels.

* `Primitivas.py`

<p>As formas geométricas e a renderização das células são processadas através de algoritmos clássicos de computação gráfica:</p>

*   **Bresenham:** Algoritmo otimizado para desenho de retas e contornos.
*   **Ponto Médio (Midpoint):** Utilizado para a renderização matemática de círculos e elipses.
*   **Cohen-Sutherland:** Sistema de Clipping (recorte) para garantir que apenas o que está dentro da janela de visualização seja processado.
*   **Scanline Filling:** Preenchimento de formas geométricas via software, manipulando pixel a pixel na superfície.

* `Recorte.py`

<p>Para garantir a fluidez da simulação, foi implementado o algoritmo de Cohen-Sutherland. Este sistema divide o espaço do mundo em 9 regiões através de códigos binários.</p>

* **Performance:** O motor realiza testes lógicos rápidos para descartar linhas e polígonos que estão totalmente fora da área de visão (viewport).
* **Precisão:** O recorte é feito matematicamente antes de enviar os pixels para a função de desenho, evitando cálculos desnecessários de rasterização.

* `Transformacoes.py`

<p>O Mebaformers processa o movimento e a forma das células através de matrizes de transformação. Em vez de alterar coordenadas manualmente, o motor utiliza:</p>

* **Coordenadas Homogêneas:** Uso de matrizes 3x3 para realizar translações, rotações e escalas de forma unificada.
* **Composição de Matrizes:** O sistema permite multiplicar diferentes matrizes de transformação, aplicando movimentos complexos aos polígonos das células em uma única passagem matemática.
* **Transformações em Tempo Real:**
* **Rotação:** As células podem girar suavemente em torno de seu próprio eixo usando funções trigonométricas.
* **Escala Dinâmica:** O crescimento da ameba ao consumir nutrientes é processado via matrizes de escala.
* **Translação:** Movimentação fluida pelo ambiente microscópico.

* `Viewports.py`

<p>O motor implementa um sistema de visualização que separa o mundo lógico das coordenadas da tela. Através de transformações de normalização, o jogo é capaz de:</p>

* **Zoom Dinâmico:** Ao alterar as dimensões da janela, o motor recalcula automaticamente a escala (sx, sy) para ajustar a visão na viewport.
* **Câmera Livre:** O deslocamento pelo ambiente microscópico é feito via translações matriciais, permitindo que a "câmera" siga a ameba enquanto ela explora o cenário.
* **Independência de Resolução:** A lógica permite que o mundo do jogo seja renderizado em qualquer tamanho de janela sem distorcer as proporções das células.

Pasta **polygons**
* `ameba.py`

<p>Diferente de jogos que utilizam sprites (imagens prontas), a ameba no Mebaformers é gerada matematicamente em cada frame:</p>

* **Deformação Dinâmica:** É utilizado a superposição de múltiplas ondas senoidais e cossenoidais para criar um contorno irregular que pulsa organicamente.
* **Sincronização de Câmera:** A função `draw_ameba_with_camera` demonstra a integração total da pipeline, onde a geometria local do objeto é transformada para as coordenadas do mundo e, finalmente, para o espaço da câmera em tempo real.
* **Alta Resolução Geométrica:** Cada célula é composta por um polígono de 150 vértices calculados dinamicamente, permitindo deformações suaves sem perda de performance.

* `food.py`

<p></p>

A classe Food importa tudo o que foi feito na pasta **lib** para tratar a comida (outros polígonos) como objetos dentro do seu sistema de coordenadas do mundo, aplicando a `matriz_camera` neles antes de renderizar.

* `minimap.py`

<p>O jogo conta com um sistema de navegação auxiliar (minimapa) que utiliza a mesma pipeline de renderização do mundo principal:</p>

* **Fundo Estilizado:** O fundo do minimapa é renderizado com um gradiente vertical, processado via scanline.
* **Reuso de Código:** Demonstra a versatilidade da biblioteca gráfica, utilizando as mesmas funções de polígonos e preenchimento para elementos estáticos da interface.

Pasta **utils**
* `capture_key.py`

<p>Diferente de implementações simples, o **Mebaformers** utiliza um sistema de movimentação normalizada:</p>

* **Correção de Velocidade Diagonal:** Foi implementado uma lógica para evitar o ganho de velocidade excessivo ao pressionar duas teclas simultaneamente (ex: Cima + Direita).
* **Input:** É permitido o uso das teclas de seta e das teclas W A S D, garantindo acessibilidade e conforto para diferentes perfis de jogadores.
* Com o uso da `normalized_diagonal_speed`, é possível que o movimento seja uniforme em todas as direções. 

* `main.py`

<p>Aqui é onde tudo o que foi construído nas outras pastas se conecta para criar a experiência do jogo.</p>

* **Resolução Nativa:** Ao usar o pyautogui, o jogo não tem um tamanho fixo; ele se adapta automaticamente à resolução do monitor do usuário.
* **Repetição de Teclas:** O `pygame.key.set_repeat(1, 5)` garante que, enquanto o usuário segurar uma tecla, o movimento continue sendo disparado rapidamente, permitindo um controle fluido da ameba.
* **Matemática Vetorial:** É definido uma velocidade específica para quando o jogador aperta duas teclas (ex: W e D). Isso evita que a ameba "corra mais" na diagonal do que nos eixos retos, mantendo o equilíbrio do desafio.

<p>Foi criado duas "câmeras" usando a mesma função `janela_viewport`:</p>

* **Câmera Principal:**
* A `janela_principal` é centralizada na posição atual da ameba (`ameba_pos_x`).
* Conforme a ameba se move, a janela se move com ela, criando o efeito de seguimento de câmera.
* **Minimapa:**
* A `janela_minimapa` engloba todo o `MUNDO_W` e `MUNDO_H`.
* Ela não se move; ela reduz todo o mundo de 2000x2000 pixels para caber dentro de um quadradinho de 200x200 na tela.

<p>Dentro do while running, a tela é limpa e desenha tudo duas vezes:</p>

1. Primeiro Passe: Desenha a comida e a ameba usando a `matriz_camera_principal`. Isso mostra o jogo "de perto".
2. Segundo Passe: Desenha o fundo do minimapa e, logo em seguida, desenha a comida e a ameba novamente, mas agora usando a `matriz_camera_minimapa`. Isso cria a visão aérea no canto da tela.
* **Otimização:** É usado a distância ao quadrado para detectar colisão.
* **Evolução:** Se a distância for menor que a soma dos raios, a ameba "come" a comida (`ameba_r += 5`) e o objeto é removido da lista de sobreviventes.

## Linguagem e bibliotecas utilizadas
* Python 3
* Pygame
* PyAutoGUI
* Math

### Pré-requisitos
Você precisará ter o Python instalado em sua máquina. Para instalar a biblioteca Pygame, execute:
<p>pip install pygame</p>
