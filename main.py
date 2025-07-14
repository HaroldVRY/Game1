import pygame
import sys
import os # Aunque no se usen assets, `os` a veces es útil para la ruta del proyecto.

# Importar todas las constantes necesarias
from constants import (
    COLOR_GREEN, JUMP_STRENGTH, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BACKGROUND,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_BUTTON_NORMAL, COLOR_BUTTON_HOVER, COLOR_TEXT,
    PLAYER_VELOCITY, MAX_PLAYER_HEALTH,
    POINTS_PER_TIME_UNIT, POINTS_PER_COIN, POINTS_PER_ENEMY_DEFEATED,
    GOOMBA_WIDTH, GOOMBA_HEIGHT, MINIBOSS_WIDTH, MINIBOSS_HEIGHT
)

# Importar las clases del juego
from player import Jugador
from entities import Platform, Coin, Goomba, Miniboss, EndFlag
from levels import LEVELS, PLAYER_RENDER_HEIGHT, GOOMBA_RENDER_HEIGHT, MINIBOSS_RENDER_HEIGHT

# --- Inicialización de Pygame ---
pygame.init()

# --- Configuración de la pantalla ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aventura del Caballero Color") # Nuevo nombre del juego

# --- Reloj para controlar el framerate ---
clock = pygame.time.Clock()

# --- Fuentes ---
font_small = pygame.font.Font(None, 36) # Para texto normal y botones
font_medium = pygame.font.Font(None, 50) # Para títulos o mensajes importantes
font_large = pygame.font.Font(None, 72) # Para el título del juego

# --- Estados del juego ---
MENU = 0
GAME_PLAYING = 1
GUIDE = 2
GAME_OVER = 3 # Incluye tanto Game Over por muerte como Juego Completado

current_game_state = MENU

# --- Variables del juego (se reinician al iniciar un nuevo juego) ---
player = None
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
end_flag = None
current_level_num = 0
player_score = 0
game_won_status = False # True si se completaron todos los niveles, False si es Game Over por vida

# --- Funciones de Juego ---
def reset_game():
    """Reinicia todas las variables y el estado del juego para un nuevo inicio."""
    global player, platforms, enemies, coins, end_flag, current_level_num, player_score, game_won_status, game_over
    
    player = Jugador()
    platforms.empty()
    enemies.empty()
    coins.empty()
    end_flag = None
    current_level_num = 0
    player_score = 0
    game_won_status = False
    load_level(current_level_num, player) # Cargar el primer nivel al reiniciar

def load_level(level_num, player_instance, enemy_speed_difficulty_multiplier=1.0):
    """Carga los elementos para un nivel específico."""
    global platforms, enemies, coins, end_flag

    platforms.empty() # Limpiar grupos de sprites
    enemies.empty()
    coins.empty()

    if level_num >= len(LEVELS):
        print("¡Has completado todos los niveles!")
        return # No hay más niveles para cargar

    level_data = LEVELS[level_num]

    # Crear plataformas
    for p_data in level_data["platforms"]:
        platforms.add(Platform(*p_data))

    # Crear enemigos
    for e_type, x, y, movement_range in level_data["enemies"]:
        if e_type == "goomba":
            enemies.add(Goomba(x, y, movement_range, speed_multiplier=enemy_speed_difficulty_multiplier))
        elif e_type == "miniboss":
            enemies.add(Miniboss(x, y, movement_range, speed_multiplier=enemy_speed_difficulty_multiplier))

    # Crear monedas
    for c_x, c_y in level_data["coins"]:
        coins.add(Coin(c_x, c_y))

    # Crear bandera de fin de nivel
    flag_x, flag_y = level_data["flag_pos"]
    end_flag = EndFlag(flag_x, flag_y)

    # Reposicionar al jugador al inicio del nivel
    player_instance.rect.midbottom = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50)

# --- Clases Auxiliares para UI (Botones) ---
class Button:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.color = COLOR_BUTTON_NORMAL

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = COLOR_BUTTON_HOVER
        else:
            self.color = COLOR_BUTTON_NORMAL
        
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, COLOR_BLACK, self.rect, 2) # Borde del botón

        text_surface = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True # Retorna True si el botón fue presionado
        return False

# --- Funciones de Pantallas ---

def draw_menu_screen():
    screen.fill(COLOR_BACKGROUND)
    
    title_text = font_large.render("Aventura del Caballero Color", True, COLOR_BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    start_button.draw(screen)
    guide_button.draw(screen)
    exit_button.draw(screen)

def draw_guide_screen():
    screen.fill(COLOR_BACKGROUND)
    
    guide_title = font_medium.render("Guía del Juego", True, COLOR_BLACK)
    guide_title_rect = guide_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
    screen.blit(guide_title, guide_title_rect)

    guide_text_lines = [
        "Objetivo: Llegar a la bandera de fin de nivel.",
        "Controles:",
        "  - Flecha Izquierda/Derecha: Mover al caballero.",
        "  - Barra Espaciadora: Saltar.",
        "  - Pisotear enemigos para derrotarlos (saltando sobre ellos).",
        "  - Recolecta monedas para ganar puntos.",
        "  - Cuidado con los enemigos, te quitarán vida.",
        "  - ¡No te caigas del mapa!"
    ]
    
    y_offset = guide_title_rect.bottom + 30
    for line in guide_text_lines:
        line_surface = font_small.render(line, True, COLOR_BLACK)
        line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(line_surface, line_rect)
        y_offset += 40 # Espacio entre líneas

    back_button.draw(screen)

def draw_game_over_screen():
    screen.fill(COLOR_BACKGROUND)
    
    if game_won_status:
        message_text = font_large.render("¡JUEGO COMPLETADO!", True, COLOR_GREEN)
    else:
        message_text = font_large.render("GAME OVER", True, COLOR_RED)
    
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(message_text, message_rect)

    score_display = font_medium.render(f"Puntuación Final: {player_score}", True, COLOR_BLACK)
    score_rect = score_display.get_rect(center=(SCREEN_WIDTH // 2, message_rect.bottom + 50))
    screen.blit(score_display, score_rect)

    restart_button_game_over.draw(screen)
    exit_button_game_over.draw(screen)

# --- Acciones de Botones ---
def start_game_action():
    global current_game_state
    reset_game()
    current_game_state = GAME_PLAYING

def show_guide_action():
    global current_game_state
    current_game_state = GUIDE

def exit_game_action():
    pygame.quit()
    sys.exit()

def back_to_menu_action():
    global current_game_state
    current_game_state = MENU

# --- Creación de Botones ---
# Menú Principal
start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "Iniciar Juego", font_small, start_game_action)
guide_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, "Guía", font_small, show_guide_action)
exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50, "Salir", font_small, exit_game_action)

# Pantalla de Guía
back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Volver al Menú", font_small, back_to_menu_action)

# Pantalla de Game Over/Juego Completado
restart_button_game_over = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Reiniciar", font_small, start_game_action)
exit_button_game_over = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 170, 200, 50, "Salir", font_small, exit_game_action)

# --- Bucle principal del juego ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_game_state == MENU:
            start_button.handle_event(event)
            guide_button.handle_event(event)
            exit_button.handle_event(event)
        elif current_game_state == GUIDE:
            back_button.handle_event(event)
        elif current_game_state == GAME_OVER:
            restart_button_game_over.handle_event(event)
            exit_button_game_over.handle_event(event)
        elif current_game_state == GAME_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                # La tecla 'R' ya no es para reiniciar, los botones lo hacen
                # if event.key == pygame.K_r: 
                #    reset_game()
                #    current_game_state = MENU # Podría ser un reinicio directo al juego si se prefiere

    # --- Lógica de actualización de estados ---
    if current_game_state == GAME_PLAYING:
        # Actualizar jugador
        player.update(platforms)

        # Actualizar enemigos
        enemies.update()

        # Actualizar monedas
        coins.update()

        # Colisiones del jugador con enemigos
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False) 
        for enemy in collided_enemies:
            # Lógica de pisotón
            # Se añade un pequeño margen `+5` para asegurar que el centro del enemigo esté justo por debajo del pie del jugador.
            if player.vel_y > 0 and player.rect.bottom <= enemy.rect.centery + 5: 
                enemy.take_damage(1)
                player.vel_y = -JUMP_STRENGTH / 2 # Pequeño rebote para el jugador
                if enemy.is_defeated:
                    player_score += POINTS_PER_ENEMY_DEFEATED
            else: # Colisión normal (el jugador es golpeado)
                if player.take_damage(1): # Si el jugador muere
                    current_game_state = GAME_OVER
                    game_won_status = False # Perdió el juego

        # Colisiones del jugador con monedas
        collected_coins = pygame.sprite.spritecollide(player, coins, True) 
        for coin in collected_coins:
            player_score += POINTS_PER_COIN

        # Colisión con la bandera de fin de nivel
        if end_flag and player.rect.colliderect(end_flag.rect):
            current_level_num += 1
            if current_level_num < len(LEVELS):
                print(f"Nivel {current_level_num} completado. ¡Cargando siguiente nivel!")
                # Aumentar dificultad de enemigos para el siguiente nivel
                load_level(current_level_num, player, 1.0 + current_level_num * 0.1) 
            else:
                current_game_state = GAME_OVER
                game_won_status = True # Completó todos los niveles

        # Si el jugador cae fuera de la pantalla (muere)
        if player.rect.top > SCREEN_HEIGHT:
            player.health = 0 # Asegurarse de que la vida sea 0 al caer
            current_game_state = GAME_OVER
            game_won_status = False # Perdió el juego

    # --- Lógica de Dibujo ---
    screen.fill(COLOR_BACKGROUND)

    if current_game_state == MENU:
        draw_menu_screen()
    elif current_game_state == GAME_PLAYING:
        platforms.draw(screen)
        enemies.draw(screen)
        coins.draw(screen)
        if end_flag: # Asegurarse de que la bandera exista
            screen.blit(end_flag.image, end_flag.rect)
        screen.blit(player.image, player.rect)

        # Mostrar puntuación y vida
        score_text = font_small.render(f"Puntuación: {player_score}", True, COLOR_BLACK)
        health_text = font_small.render(f"Vida: {player.health}", True, COLOR_BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (SCREEN_WIDTH - health_text.get_width() - 10, 10))
    elif current_game_state == GUIDE:
        draw_guide_screen()
    elif current_game_state == GAME_OVER:
        draw_game_over_screen()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()