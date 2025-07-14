import pygame
import os
from constants import ASSETS_DIR # Se mantiene ASSETS_DIR por si se usan en el futuro

def load_scaled_image(filename, width, height, fallback_color=(255, 0, 255)):
    """
    Carga y escala una imagen. Si la imagen no se encuentra, devuelve una superficie de color.
    """
    path = os.path.join(ASSETS_DIR, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar la imagen '{filename}': {e}. Usando color de fallback.")
        fallback_surface = pygame.Surface((width, height))
        fallback_surface.fill(fallback_color)
        return fallback_surface

def load_and_cut_sprite_sheet(filename, sprite_width, sprite_height, scale=1, num_frames=None, x_offset=0, y_offset=0):
    """
    Carga un spritesheet y lo divide en frames individuales.
    filename: Nombre del archivo de la spritesheet.
    sprite_width, sprite_height: Dimensiones de cada sprite individual en la hoja.
    scale: Factor de escala para los sprites.
    num_frames: Número específico de frames a extraer. Si es None, se calcula automáticamente.
    x_offset, y_offset: Desplazamiento inicial en el spritesheet para empezar a cortar.
    """
    path = os.path.join(ASSETS_DIR, filename)
    frames = []
    try:
        sheet = pygame.image.load(path).convert_alpha()
        
        # Calcular el número de frames si no se especifica
        if num_frames is None:
            # Si la hoja es horizontal, asume todos los frames en la primera fila.
            num_frames = (sheet.get_width() - x_offset) // sprite_width
            if num_frames < 0: num_frames = 0 # Evitar negativos
            
        scaled_width = sprite_width * scale
        scaled_height = sprite_height * scale

        for i in range(num_frames):
            frame_rect = pygame.Rect(x_offset + i * sprite_width, y_offset, sprite_width, sprite_height)
            frame_surface = pygame.Surface(frame_rect.size, pygame.SRCALPHA)
            frame_surface.blit(sheet, (0, 0), frame_rect)
            frame_surface = pygame.transform.scale(frame_surface, (scaled_width, scaled_height))
            frames.append(frame_surface)
    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar o cortar la spritesheet '{filename}': {e}. Usando color de fallback.")
        # Fallback a una superficie de color si hay un error
        fallback_surface = pygame.Surface((sprite_width * scale, sprite_height * scale), pygame.SRCALPHA)
        fallback_surface.fill((255, 0, 255)) # Color magenta para destacar el error
        frames.append(fallback_surface) # Al menos un frame de fallback

    return frames


def load_tile_from_tileset(filename, tile_x_index, tile_y_index, tile_size, scale=1, fallback_color=(255, 0, 255)):
    """
    Carga un tile específico de un tileset.
    filename: Nombre del archivo del tileset.
    tile_x_index, tile_y_index: Índices (columna, fila) del tile en el tileset (0-based).
    tile_size: Tamaño de cada tile (ej. 16 para un tileset de 16x16).
    scale: Factor de escala para el tile.
    """
    path = os.path.join(ASSETS_DIR, filename)
    try:
        tileset = pygame.image.load(path).convert_alpha()
        
        # Calcular la posición en píxeles del tile
        x_pixel = tile_x_index * tile_size
        y_pixel = tile_y_index * tile_size
        
        # Asegurarse de que el tile esté dentro de los límites del tileset
        if x_pixel + tile_size > tileset.get_width() or y_pixel + tile_size > tileset.get_height():
            raise ValueError(f"Tile ({tile_x_index}, {tile_y_index}) está fuera de los límites de '{filename}'")

        tile_rect = pygame.Rect(x_pixel, y_pixel, tile_size, tile_size)
        tile_surface = pygame.Surface(tile_rect.size, pygame.SRCALPHA)
        tile_surface.blit(tileset, (0, 0), tile_rect)
        
        # Escalar el tile si es necesario
        if scale != 1:
            tile_surface = pygame.transform.scale(tile_surface, (tile_size * scale, tile_size * scale))
            
        return tile_surface

    except pygame.error as e:
        print(f"Advertencia: No se pudo cargar el tileset '{filename}' o extraer tile ({tile_x_index}, {tile_y_index}): {e}. Usando color de fallback.")
        # Fallback a una superficie de color si hay un error
        fallback_surface = pygame.Surface((tile_size * scale, tile_size * scale), pygame.SRCALPHA)
        fallback_surface.fill(fallback_color)
        return fallback_surface
    except ValueError as e:
        print(f"Error de valor al extraer tile: {e}. Usando color de fallback.")
        fallback_surface = pygame.Surface((tile_size * scale, tile_size * scale), pygame.SRCALPHA)
        fallback_surface.fill(fallback_color)
        return fallback_surface