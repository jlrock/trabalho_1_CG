# Mebaformers - Cellular Simulation

An interactive cellular growth simulation developed in **Pygame**. The player takes control of an amoeba in a hostile environment, where it must consume nutrients to grow.

---

## About the Project

The main objective of this project was to explore the implementation of game logic, physics, and rendering using the fundamental resources within Pygame. Unlike off-the-shelf game engines, all the logic for growth, proximity detection, and fluid movement was implemented manually from scratch.

## Gameplay/Demo Video
*You can [download the video](assets/mebaformers-demo.mp4) directly or [watch it on Google Drive](https://drive.google.com/file/d/15w1MV8mhaxPwcMBZmuFhEtLMk8KhfV0s/view?usp=drive_link)*

### Folder Structure

```text
mebaformers/
├── lib/                        # Graphics library
│   ├── Motor_grafico.py        # setPixel and Safety Clipping
│   ├── Preenchimento.py        # Scanline, Gradients, and Textures
│   ├── Primitivas.py           # Bresenham, Clipping, and Scanline
│   ├── Recorte.py              # Cohen-Sutherland Algorithm
│   ├── Transformacoes.py       # 3x3 Matrices and Linear Algebra
│   └── Viewports.py            # Viewport Mapping
├── polygons/                   # Game Entities
│   ├── ameba.py                # Procedural generation and animation
│   ├── button.py               # Buttons creation
│   ├── food.py                 # Food management
│   ├── menu_ameba.py           # Displaying different ameba in menu
│   └── minimap.py              # Radar/minimap logic
├── utils/                      # Helpers
│   ├── display_hud.py          # Display ameba stats during game
│   └── capture_key.py          # Input and Speed Normalization
└── main.py                     # Main loop and integration
```

### Main Features

The main highlight of this project is that it does not use standard Pygame drawing functions. Instead, a **custom graphics pipeline** was developed, processing rendering pixel by pixel.
To begin, the code structure was divided into parts for each functionality.

**lib** Folder

* `Motor_grafico.py`

The base function `setPixel` was implemented with a **Safety Clipping** system, ensuring that the graphics engine never tries to access coordinates outside the window surface, which optimizes software stability.

To bring **Mebaformers** to life, classic algorithms that are the foundation of computer graphics were implemented:

* **Bresenham (Lines):** Optimized implementation to draw the edges of the amoebas and scenario elements without using heavy floating-point arithmetic.
* **Midpoint (Circles and Ellipses):** Cells are rendered through midpoint logic, ensuring perfect symmetry in the simulation.
* **Scanline Fill:** A scanline filling system that allows amoebas to have solid, opaque colors, processed dynamically.
* **Clipping System:** To maintain performance, the game uses the Cohen-Sutherland algorithm. This allows the engine to instantly identify which parts of a cell or line are outside the player's view, discarding the unnecessary processing of invisible pixels.

* `Preenchimento.py`

* **Color Interpolation (Gradients):** Implementation of a linear interpolation system to create dynamic gradients on the amoebas. This allows the cell to change color smoothly depending on its health or evolution state.
* **Texture Mapping (UV Mapping):** The project features a `scanline_texture` algorithm that projects texture coordinates (U, V) onto arbitrary polygons. This allows "dressing" the cells with complex organic patterns.
* **Flood Fill Algorithm (Stack-based):** For irregular filling areas, an optimized version of **Flood Fill** was implemented using a stack data structure to avoid the memory overflow (**Stack Overflow**) common in recursive versions.
* **Polygon Rasterization:** Use of the **Scanline** algorithm to identify polygon intersections on each screen line, ensuring perfect filling with no gaps between pixels.

* `Primitivas.py`

Geometric shapes and cell rendering are processed through classic computer graphics algorithms:

* **Bresenham:** Optimized algorithm for drawing lines and outlines.
* **Midpoint:** Used for the mathematical rendering of circles and ellipses.
* **Cohen-Sutherland:** Clipping system to ensure that only what is inside the viewport is processed.
* **Scanline Filling:** Filling geometric shapes via software, manipulating pixel by pixel on the surface.

* `Recorte.py`

To ensure fluid simulation, the Cohen-Sutherland algorithm was implemented. This system divides the world space into 9 regions using binary codes.

* **Performance:** The engine performs quick logical tests to discard lines and polygons that are completely outside the viewing area (viewport).
* **Precision:** Clipping is done mathematically before sending the pixels to the drawing function, avoiding unnecessary rasterization calculations.

* `Transformacoes.py`

Mebaformers processes the movement and shape of the cells through transformation matrices. Instead of manually altering coordinates, the engine uses:

* **Homogeneous Coordinates:** Use of 3x3 matrices to perform translations, rotations, and scaling in a unified way.
* **Matrix Composition:** The system allows multiplying different transformation matrices, applying complex movements to the cell polygons in a single mathematical pass.
* **Real-time Transformations:**
* **Rotation:** Cells can rotate smoothly around their own axis using trigonometric functions.
* **Dynamic Scale:** The amoeba's growth upon consuming nutrients is processed via scale matrices.
* **Translation:** Fluid movement through the microscopic environment.

* `Viewports.py`

The engine implements a viewing system that separates the logical world from the screen coordinates. Through normalization transformations, the game is able to perform:

* **Dynamic Zoom:** When altering the window dimensions, the engine automatically recalculates the scale (sx, sy) to adjust the view in the viewport.
* **Free Camera:** Panning through the microscopic environment is done via matrix translations, allowing the "camera" to follow the amoeba as it explores the scenario.
* **Resolution Independence:** The logic allows the game world to be rendered in any window size without distorting the cells' proportions.

**polygons** Folder

* `ameba.py`

Unlike games that use sprites (ready-made images), the amoeba in Mebaformers is generated mathematically in every frame:

* **Dynamic Deformation:** The superposition of multiple sine and cosine waves is used to create an irregular outline that pulses organically.
* **Camera Synchronization:** The `draw_ameba_with_camera` function demonstrates the full integration of the pipeline, where the object's local geometry is transformed into world coordinates and, finally, into camera space in real time.

* `food.py`

The Food class imports everything built in the **lib** folder to treat the food (other polygons) as objects within its world coordinate system, applying the `matriz_camera` to them before rendering.

* `minimap.py`

The game features an auxiliary navigation system (minimap) that uses the same rendering pipeline as the main world:

* **Stylized Background:** The minimap background is rendered with a vertical gradient, processed via scanline.
* **Code Reuse:** Demonstrates the versatility of the graphics library, using the same polygon and filling functions for static interface elements.

**utils** Folder

* `capture_key.py`

Unlike simple implementations, **Mebaformers** uses a normalized movement system:

* **Diagonal Speed Correction:** Logic was implemented to prevent excessive speed gain when pressing two keys simultaneously (e.g., Up + Right).
* **Input:** The use of arrow keys and W A S D keys is permitted, ensuring accessibility and comfort for different player profiles.
* With the use of `normalized_diagonal_speed`, it is possible for movement to be uniform in all directions.

* `main.py`

This is where everything built in the other folders connects to create the game experience.

* **Native Resolution:** By using pyautogui, the game doesn't have a fixed size; it automatically adapts to the user's monitor resolution.
* **Key Repetition:** `pygame.key.set_repeat(1, 5)` ensures that as long as the user holds down a key, the movement continues to be triggered quickly, allowing fluid control of the amoeba.
* **Vector Math:** A specific speed is defined for when the player presses two keys (e.g., W and D). This prevents the amoeba from "running faster" diagonally than on straight axes, maintaining the game's balance.

Two "cameras" were created using the same `janela_viewport` function:

* **Main Camera:**
* `janela_principal` is centered on the amoeba's current position (`ameba_pos_x`).
* As the amoeba moves, the window moves with it, creating a camera-following effect.
* **Minimap:**
* `janela_minimapa` encompasses the entire `MUNDO_W` and `MUNDO_H`.
* It does not move; it scales down the entire 2000x2000 pixel world to fit inside a small 200x200 square on the screen.

Inside the while running loop, the screen is cleared and everything is drawn twice:

1. First Pass: Draws the food and the amoeba using the `matriz_camera_principal`. This shows the game "up close".

2. Second Pass: Draws the minimap background and, right after, draws the food and amoeba again, but now using the `matriz_camera_minimapa`. This creates the aerial view in the corner of the screen.

* **Optimization:** Squared distance is used to detect collisions.
* **Evolution:** If the distance is less than the sum of the radius, the amoeba "eats" the food and the object is removed from the list of survivors.

## Language and Libraries

* Python 3
* Pygame
* PyAutoGUI
* Math

### Prerequisites

You will need to have Python installed on your machine. To install used libraries, run:

```bash
    pip install pygame
    pip install pyautogui
    pip install math
```
