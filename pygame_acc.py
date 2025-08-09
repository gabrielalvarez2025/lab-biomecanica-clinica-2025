import pygame
import requests
import time
import math

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
    pitch = math.atan2(-accX, math.sqrt(accY**2 + accZ**2)) * 180 / math.pi
    roll = math.atan2(accY, accZ) * 180 / math.pi
    return pitch, roll

# Función para detectar colisión entre círculo y rectángulo
def colision_circulo_rect(x, y, radio, rect):
    # Encuentra el punto más cercano en el rectángulo al centro del círculo
    closest_x = max(rect.left, min(x, rect.right))
    closest_y = max(rect.top, min(y, rect.bottom))
    # Calcula la distancia entre el centro del círculo y ese punto
    dist_x = x - closest_x
    dist_y = y - closest_y
    distancia = math.hypot(dist_x, dist_y)
    return distancia < radio

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto controlado por acelerómetro")

# Variables del círculo
x, y = 30, ALTO - 30  # posición inicial
radio = 10
color = (255, 100, 100)
velocidad = 2

# Definir paredes del laberinto como rectángulos (x, y, ancho, alto)
paredes = [
    pygame.Rect(0, 0, ANCHO, 10),          # pared superior
    pygame.Rect(0, 0, 10, ALTO),           # pared izquierda
    pygame.Rect(0, ALTO-10, ANCHO, 10),    # pared inferior
    pygame.Rect(ANCHO-10, 0, 10, ALTO),    # pared derecha
    pygame.Rect(50, 0, 10, 300),
    pygame.Rect(150, 100, 10, 300),
    pygame.Rect(250, 0, 10, 300),
    pygame.Rect(350, 100, 10, 300),
    pygame.Rect(450, 0, 10, 300),
    pygame.Rect(550, 100, 10, 300),
]

# Meta (objetivo)
meta = pygame.Rect(ANCHO - 50, 20, 40, 40)
color_meta = (0, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

running = True
ganaste = False

while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    if not ganaste:
        # Obtener aceleración y calcular pitch/roll
        accX, accY, accZ = obtener_valores()
        pitch, roll = calcular_pitch_roll(accX, accY, accZ)

        # Calcular movimiento
        dx = int(roll * velocidad / 10)
        dy = int(pitch * velocidad / 10)

        # Intentar mover X y chequear colisión
        nuevo_x = x + dx
        nuevo_y = y  # y aún no cambia
        circulo_rect = pygame.Rect(nuevo_x - radio, nuevo_y - radio, radio*2, radio*2)
        if not any(colision_circulo_rect(nuevo_x, nuevo_y, radio, pared) for pared in paredes):
            x = nuevo_x

        # Intentar mover Y y chequear colisión
        nuevo_y = y + dy
        circulo_rect = pygame.Rect(x - radio, nuevo_y - radio, radio*2, radio*2)
        if not any(colision_circulo_rect(x, nuevo_y, radio, pared) for pared in paredes):
            y = nuevo_y

        # Verificar si llegó a la meta
        if colision_circulo_rect(x, y, radio, meta):
            ganaste = True

    # Dibujar todo
    pantalla.fill((30, 30, 30))

    # Dibujar meta
    pygame.draw.rect(pantalla, color_meta, meta)

    # Dibujar paredes
    for pared in paredes:
        pygame.draw.rect(pantalla, (200, 200, 200), pared)

    # Dibujar círculo
    pygame.draw.circle(pantalla, color, (x, y), radio)

    if ganaste:
        texto_ganar = font.render("¡Ganaste!", True, (255, 255, 255))
        pantalla.blit(texto_ganar, (ANCHO // 2 - texto_ganar.get_width() // 2, ALTO // 2 - texto_ganar.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
