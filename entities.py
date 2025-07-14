import pygame
import os # Se mantiene os por si se necesitan rutas en el futuro, aunque no se use ahora
from constants import (
    COLOR_GREEN, COLOR_BLACK, COLOR_COIN, COLOR_RED, COLOR_FLAG_GREEN,
    GOOMBA_WIDTH, GOOMBA_HEIGHT, GOOMBA_SPEED_BASE,
    MINIBOSS_WIDTH, MINIBOSS_HEIGHT, MINIBOSS_SPEED_BASE, MINIBOSS_HEALTH,
    FLAG_SPRITE_WIDTH, FLAG_SPRITE_HEIGHT,
    FPS # Necesario para la invulnerabilidad de los enemigos
)
# No necesitamos importar las funciones de carga de sprites ahora
# from utils import load_and_cut_sprite_sheet, load_tile_from_tileset

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(COLOR_GREEN) # Color verde para las plataformas
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16)) # Moneda como un pequeño cuadrado
        self.image.fill(COLOR_COIN) # Color dorado para la moneda
        self.rect = self.image.get_rect(center=(x, y)) # Posición usando el centro para la moneda

    def update(self):
        # Las monedas de color sólido no necesitan animación de giro
        pass

class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, movement_range_x, speed_x, health=1, fallback_color=COLOR_BLACK):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(fallback_color) # Color base del enemigo
        self.rect = self.image.get_rect(topleft=(x, y))
        self.min_x, self.max_x = movement_range_x # Rango de movimiento en X
        self.vel_x = speed_x # Velocidad de movimiento en X
        self.health = health # Salud del enemigo
        self.is_defeated = False # Estado de si ha sido derrotado
        self.invulnerable_timer = 0 # Temporizador de invulnerabilidad al ser golpeado

    def update(self):
        if self.is_defeated:
            return

        # Lógica de invulnerabilidad para parpadeo visual del enemigo
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer % 10 < 5: # Parpadeo
                self.image.fill(COLOR_RED) # Color de parpadeo (rojo)
            else:
                self.image.fill(self.image.get_at((0,0))) # Vuelve al color original
        else:
            # Asegurar color normal si no es invulnerable
            pass # No necesitamos rellenar, el color ya está ahí al inicio

        # Movimiento horizontal del enemigo
        self.rect.x += self.vel_x
        if self.rect.left < self.min_x or self.rect.right > self.max_x:
            self.vel_x *= -1 # Cambia de dirección
            # Ajusta la posición para que no se quede atascado fuera del rango
            if self.rect.left < self.min_x:
                self.rect.left = self.min_x
            if self.rect.right > self.max_x:
                self.rect.right = self.max_x

    def take_damage(self, amount):
        if self.invulnerable_timer == 0: # Solo recibe daño si no es invulnerable
            self.health -= amount
            self.invulnerable_timer = FPS / 2 # Activa invulnerabilidad por 0.5 segundos
            if self.health <= 0:
                self.is_defeated = True
                self.kill() # Elimina el sprite del grupo

class Goomba(EnemyBase):
    def __init__(self, x, y, movement_range_x, speed_multiplier=1):
        super().__init__(
            x, y, GOOMBA_WIDTH, GOOMBA_HEIGHT, # Usa las dimensiones de constants
            movement_range_x,
            GOOMBA_SPEED_BASE * speed_multiplier,
            health=1,
            fallback_color=(0, 150, 0) # Verde oscuro para el Goomba
        )
        # Ajuste vertical para que la base del Goomba esté en 'y' (si 'y' es el suelo/plataforma)
        # Esto asume que el 'y' de la plataforma es el topleft.
        # Si el 'y' pasado es el de la base, no necesitamos ajuste: self.rect.bottom = y
        # Para la demo, el topleft es suficiente.
        pass

class Miniboss(EnemyBase):
    def __init__(self, x, y, movement_range_x, speed_multiplier=1):
        super().__init__(
            x, y, MINIBOSS_WIDTH, MINIBOSS_HEIGHT, # Usa las dimensiones de constants
            movement_range_x,
            MINIBOSS_SPEED_BASE * speed_multiplier,
            health=MINIBOSS_HEALTH,
            fallback_color=(150, 0, 150) # Púrpura para el Miniboss
        )
        # Ajuste vertical (similar al Goomba)
        pass

class EndFlag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((FLAG_SPRITE_WIDTH * 2, FLAG_SPRITE_HEIGHT * 2)) # Tamaño de ejemplo para la bandera
        self.image.fill(COLOR_FLAG_GREEN) # Color verde de la bandera
        self.rect = self.image.get_rect(bottomleft=(x, y)) # La base de la bandera estará en (x,y)