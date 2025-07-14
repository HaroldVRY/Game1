import pygame
from constants import (
    PLAYER_VELOCITY, JUMP_STRENGTH, GRAVITY,
    MAX_PLAYER_HEALTH, INVULNERABILITY_FRAMES,
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BLUE_PLAYER, COLOR_RED, FPS # FPS para invulnerabilidad
)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Usar una superficie de color sólido para el jugador
        self.image = pygame.Surface((32, 32)) # Tamaño de ejemplo para el jugador
        self.image.fill(COLOR_BLUE_PLAYER) # Color del jugador
        
        # Posición inicial del jugador
        self.rect = self.image.get_rect(topleft=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100 - self.image.get_height()))

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.health = MAX_PLAYER_HEALTH
        self.invulnerable_timer = 0 # Contador para invulnerabilidad
        self.defeated_enemies_count = 0
        self.facing_right = True # Para futura implementación de dirección de sprite

    def update(self, platforms):
        # Reiniciar velocidad X si no se está moviendo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_VELOCITY
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_VELOCITY
            self.facing_right = True
        else:
            self.vel_x = 0

        # Aplicar gravedad
        self.vel_y += GRAVITY
        
        # Mover en X
        self.rect.x += self.vel_x

        # Mover en Y
        self.rect.y += self.vel_y

        # Colisión con plataformas en Y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0: # Cayendo
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: # Saltando hacia arriba
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Limitar al jugador dentro de los límites de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: # Para que no pueda saltar fuera de la pantalla por arriba
            self.rect.top = 0

        # Lógica de invulnerabilidad para parpadeo visual
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer % 10 < 5: # Parpadeo: cambiar de color cada 5 frames
                self.image.fill(COLOR_RED) # Color de parpadeo (rojo)
            else:
                self.image.fill(COLOR_BLUE_PLAYER) # Color normal del jugador
        else:
            self.image.fill(COLOR_BLUE_PLAYER) # Asegurar color normal si no es invulnerable

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_STRENGTH
            self.on_ground = False

    def take_damage(self, amount):
        if self.invulnerable_timer == 0: # Solo recibe daño si no es invulnerable
            self.health -= amount
            self.invulnerable_timer = INVULNERABILITY_FRAMES # Activa el temporizador de invulnerabilidad
            if self.health <= 0:
                print("Game Over!")
                # Aquí podrías añadir una pantalla de Game Over o reiniciar el juego
                return True # Indica que el jugador ha sido derrotado
        return False # Indica que el jugador no ha sido derrotado o no recibió daño

    def add_defeated_enemy(self):
        self.defeated_enemies_count += 1