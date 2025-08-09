import pygame
import requests
import time

# Configuración Phyphox
PP_ADDRESS = "http://192.168.1.119:8080"
CHANNELS = ["accX", "accY"]

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
        return [0.0, 0.0]

# Inicializar Pygame
pygame.init()
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Controlado por acelerómetro")

# Variables del círculo
x, y = ANCHO // 2, ALTO // 2
radio = 20
color = (255, 100, 100)
velocidad = 5  # multiplicador para ajustar sensibilidad

clock = pygame.time.Clock()

running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    # Obtener valores del acelerómetro
    acc_x, acc_y = obtener_valores()

    # Actualizar posición (invertir eje Y si quieres que suba al inclinar)
    x += int(acc_x * velocidad)
    y += int(-acc_y * velocidad)

    # Limitar que el círculo no salga de la pantalla
    x = max(radio, min(ANCHO - radio, x))
    y = max(radio, min(ALTO - radio, y))

    # Dibujar
    pantalla.fill((30, 30, 30))
    pygame.draw.circle(pantalla, color, (x, y), radio)

    pygame.display.flip()
    clock.tick(30)  # FPS

pygame.quit()