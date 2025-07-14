# --- Configuración de Pantalla ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 # Frames por segundo

# --- Colores (RGB) ---
COLOR_BACKGROUND = (135, 206, 235)  # Azul cielo
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE_PLAYER = (0, 100, 255) # Color para el jugador si no se usa sprite
COLOR_FLAG_GREEN = (0, 180, 0) # Color para la bandera de fin de nivel
COLOR_COIN = (255, 215, 0) # Dorado para las monedas

# --- Configuración del Jugador ---
PLAYER_VELOCITY = 5
JUMP_STRENGTH = 15
GRAVITY = 0.75
MAX_PLAYER_HEALTH = 3
INVULNERABILITY_FRAMES = FPS * 1.5 # 1.5 segundos de invulnerabilidad

# --- Configuración de Enemigos (tamaños de los cuadrados sólidos) ---
GOOMBA_WIDTH = 32 # Tamaño de Goomba (cuadrado)
GOOMBA_HEIGHT = 32
GOOMBA_SPEED_BASE = 1

MINIBOSS_WIDTH = 64 # Tamaño de Miniboss (cuadrado más grande)
MINIBOSS_HEIGHT = 64
MINIBOSS_SPEED_BASE = 0.8
MINIBOSS_HEALTH = 5

# --- Colores adicionales para UI ---
COLOR_BUTTON_NORMAL = (70, 130, 180)  # Azul acero
COLOR_BUTTON_HOVER = (100, 149, 237)   # Azul aciano
COLOR_TEXT = (255, 255, 255)         # Blanco para el texto

# --- Puntuación ---
POINTS_PER_TIME_UNIT = 10 # Puntos por cada segundo que se ahorra (no implementado en el juego base)
POINTS_PER_COIN = 100
POINTS_PER_ENEMY_DEFEATED = 200

# --- Rutas de Recursos (no usadas en esta versión con colores sólidos, pero se dejan para el futuro) ---
ASSETS_DIR = "assets"

# --- Dimensiones de Sprites Individuales (si se usaran sprites en el futuro) ---
PLAYER_SPRITE_WIDTH = 16 
PLAYER_SPRITE_HEIGHT = 16 
PLAYER_SCALE = 2 # Escala para hacer el jugador más grande en pantalla (16*2 = 32px)

GOOMBA_SPRITE_WIDTH = 16
GOOMBA_SPRITE_HEIGHT = 16
GOOMBA_SCALE = 2 # Escala para el goomba (16*2 = 32px)

COIN_SPRITE_WIDTH = 16 
COIN_SPRITE_HEIGHT = 16 
COIN_SCALE = 1 

FLAG_SPRITE_WIDTH = 16
FLAG_SPRITE_HEIGHT = 32 

TILE_SIZE = 16 # Tamaño base de los tiles en world_tileset.png
PLATFORM_TILE_X = 16 
PLATFORM_TILE_Y = 0 

# --- Animación (no usada en esta versión con colores sólidos) ---
ANIMATION_SPEED = 0.1