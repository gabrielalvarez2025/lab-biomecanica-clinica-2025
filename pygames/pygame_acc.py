import pygame
import requests
import time
import math
import random

# Configuración Phyphox
PP_ADDRESS = "http://192.168.1.119:8080"
CHANNELS = ["accX", "accY", "accZ"]

def obtener_valores():
    url = PP_ADDRESS + "/get?" + "&".join(CHANNELS)
    try:
        r = requests.get(url, timeout=2)
        r.raise_for_status()
        data = r.json()
        valores = []
        for ch in CHANNELS:
            buffer = data["buffer"].get(ch, {}).get("buffer", [])
            if buffer:
                valores.append(buffer[0])
            else:
                valores.append(0.0)
        return valores
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return [0.0, 0.0, 0.0]

def calcular_pitch_roll(accX, accY, accZ):
    pitch = math.atan2(accX, math.sqrt(accY**2 + accZ**2)) * 180 / math.pi
    roll = math.atan2(accY, accZ) * 180 / math.pi
    return pitch, roll

def colision_circulo_rect(x, y, radio, rect):
    closest_x = max(rect.left, min(x, rect.right))
    closest_y = max(rect.top, min(y, rect.bottom))
    dist_x = x - closest_x
    dist_y = y - closest_y
    distancia = math.hypot(dist_x, dist_y)
    return distancia < radio

def generar_laberinto(ancho, alto, margen=10, min_largo=50, max_largo=150, num_paredes=15):
    """Genera paredes verticales y horizontales al azar para laberinto"""
    paredes = []
    # Paredes fijas borde del laberinto
    paredes.append(pygame.Rect(0, 0, ancho, margen))             # superior
    paredes.append(pygame.Rect(0, 0, margen, alto))              # izquierda
    paredes.append(pygame.Rect(0, alto - margen, ancho, margen)) # inferior
    paredes.append(pygame.Rect(ancho - margen, 0, margen, alto)) # derecha

    for _ in range(num_paredes):
        # Elegir si pared vertical u horizontal
        vertical = random.choice([True, False])

        if vertical:
            # Pared vertical
            x = random.randint(margen*2, ancho - margen*3)
            y = random.randint(margen, alto - max_largo - margen)
            largo = random.randint(min_largo, max_largo)
            pared = pygame.Rect(x, y, margen, largo)
        else:
            # Pared horizontal
            x = random.randint(margen, ancho - max_largo - margen)
            y = random.randint(margen*2, alto - margen*3)
            largo = random.randint(min_largo, max_largo)
            pared = pygame.Rect(x, y, largo, margen)

        # Opcional: podrías agregar lógica para evitar paredes que se solapen mucho

        paredes.append(pared)
    return paredes

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto controlado por acelerómetro")

pos_inicial = (30, ALTO - 30)
x, y = pos_inicial
radio = 10
color = (255, 100, 100)
velocidad = 2

# Meta
meta = pygame.Rect(ANCHO - 50, 20, 40, 40)
color_meta = (0, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

boton_color = (70, 130, 180)
boton_hover_color = (100, 160, 210)
boton_rect = pygame.Rect(ANCHO//2 - 60, ALTO//2 + 40, 120, 40)

# Generar paredes la primera vez
paredes = generar_laberinto(ANCHO, ALTO)

running = True
ganaste = False

while running:
    mx, my = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        if ganaste and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_rect.collidepoint(mx, my):
                # Reiniciar
                x, y = pos_inicial
                ganaste = False
                paredes = generar_laberinto(ANCHO, ALTO)

    if not ganaste:
        accX, accY, accZ = obtener_valores()
        pitch, roll = calcular_pitch_roll(accX, accY, accZ)

        sensibilidad = 3  # Ajusta este número a tu gusto, >1 para más sensible
        dx = int(roll * velocidad * sensibilidad / 10)
        dy = int(pitch * velocidad * sensibilidad / 10)

        nuevo_x = x + dx
        if not any(colision_circulo_rect(nuevo_x, y, radio, pared) for pared in paredes):
            x = nuevo_x

        nuevo_y = y + dy
        if not any(colision_circulo_rect(x, nuevo_y, radio, pared) for pared in paredes):
            y = nuevo_y

        if colision_circulo_rect(x, y, radio, meta):
            ganaste = True

    pantalla.fill((30, 30, 30))

    pygame.draw.rect(pantalla, color_meta, meta)
    for pared in paredes:
        pygame.draw.rect(pantalla, (200, 200, 200), pared)

    pygame.draw.circle(pantalla, color, (x, y), radio)

    if ganaste:
        texto_ganar = font.render("¡Ganaste!", True, (255, 255, 255))
        pantalla.blit(texto_ganar, (ANCHO // 2 - texto_ganar.get_width() // 2, ALTO // 2 - texto_ganar.get_height()))
        color_actual = boton_hover_color if boton_rect.collidepoint(mx, my) else boton_color
        pygame.draw.rect(pantalla, color_actual, boton_rect)
        texto_boton = font.render("Reiniciar", True, (255, 255, 255))
        pantalla.blit(texto_boton, (boton_rect.centerx - texto_boton.get_width() // 2,
                                    boton_rect.centery - texto_boton.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
