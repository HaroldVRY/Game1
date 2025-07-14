from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_VELOCITY, GOOMBA_WIDTH, GOOMBA_HEIGHT, MINIBOSS_WIDTH, MINIBOSS_HEIGHT
)

# Las dimensiones de los personajes y enemigos (escalados) en su forma de cuadrado sólido.
# Si cambias los tamaños en entities.py, actualiza aquí para un cálculo preciso.
PLAYER_RENDER_HEIGHT = 32 
GOOMBA_RENDER_HEIGHT = GOOMBA_HEIGHT # Se usan directamente de constants ahora
MINIBOSS_RENDER_HEIGHT = MINIBOSS_HEIGHT # Se usan directamente de constants ahora

# Define los niveles del juego
LEVELS = [
    {
        "platforms": [
            (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), # Suelo
            (100, SCREEN_HEIGHT - 150, 150, 20),
            (300, SCREEN_HEIGHT - 250, 100, 20),
            (550, SCREEN_HEIGHT - 200, 200, 20),
            (0, SCREEN_HEIGHT - 350, 150, 20)
        ],
        "enemies": [
            # La Y es el topleft del enemigo. Si la plataforma es Y, entonces Y_plataforma - Altura_enemigo.
            ("goomba", 320, SCREEN_HEIGHT - 250 - GOOMBA_RENDER_HEIGHT, (300, 400)), 
            ("goomba", 600, SCREEN_HEIGHT - 200 - GOOMBA_RENDER_HEIGHT, (550, 750))
        ],
        "coins": [
            (170, SCREEN_HEIGHT - 150 - 15), # Centro de la moneda
            (350, SCREEN_HEIGHT - 250 - 15),
            (650, SCREEN_HEIGHT - 200 - 15)
        ],
        "flag_pos": (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50) # Base de la bandera en el suelo
    },
    {
        "platforms": [
            (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), # Suelo
            (200, SCREEN_HEIGHT - 150, 250, 20),
            (0, SCREEN_HEIGHT - 250, 100, 20),
            (500, SCREEN_HEIGHT - 300, 200, 20),
            (150, SCREEN_HEIGHT - 400, 150, 20),
            (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 450, 100, 20)
        ],
        "enemies": [
            ("goomba", 250, SCREEN_HEIGHT - 150 - GOOMBA_RENDER_HEIGHT, (200, 450)),
            ("goomba", 550, SCREEN_HEIGHT - 300 - GOOMBA_RENDER_HEIGHT, (500, 700)),
            ("goomba", 50, SCREEN_HEIGHT - 250 - GOOMBA_RENDER_HEIGHT, (0, 100))
        ],
        "coins": [
            (300, SCREEN_HEIGHT - 150 - 15),
            (50, SCREEN_HEIGHT - 250 - 15),
            (600, SCREEN_HEIGHT - 300 - 15),
            (200, SCREEN_HEIGHT - 400 - 15)
        ],
        "flag_pos": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 450) # Base de la bandera en la plataforma
    },
    # --- Fase de Miniboss ---
    {
        "platforms": [
            (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50), # Suelo
            (100, SCREEN_HEIGHT - 200, 200, 20),
            (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 200, 200, 20),
            (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 350, 100, 20) # Plataforma central
        ],
        "enemies": [
            ("miniboss", SCREEN_WIDTH / 2 - MINIBOSS_WIDTH / 2, SCREEN_HEIGHT - 350 - MINIBOSS_RENDER_HEIGHT, (SCREEN_WIDTH / 2 - 100, SCREEN_WIDTH / 2 + 100))
        ],
        "coins": [],
        "flag_pos": (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50) # Base de la bandera en el suelo
    }
]