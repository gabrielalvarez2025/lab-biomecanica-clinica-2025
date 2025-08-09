import pygame
import sys
import math
import requests

# Configuración Phyphox
PP_ADDRESS = "http://192.168.1.119:8080"
CHANNELS = ["accX", "accY", "accZ"]

def obtener_valores():
    url = PP_ADDRESS + "/get?" + "&".join(CHANNELS)
    try:
        r = requests.get(url, timeout=1)
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
    except:
        return [0.0, 0.0, 0.0]

def calcular_pitch_roll(accX, accY, accZ):
    pitch = math.atan2(accX, math.sqrt(accY**2 + accZ**2)) * 180 / math.pi
    roll = math.atan2(accY, accZ) * 180 / math.pi
    return pitch, roll

pygame.init()

ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sinusoide calibrada")

# Colores
AZUL_CIELO = (135, 206, 235)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
VERDE = (0, 180, 0)
AZUL = (50, 120, 200)

# Parámetros sinusoide (frecuencia fija)
frecuencia = 0.01
velocidad = 5

# Pájaro
bird_size = 30
bird_x = ANCHO // 2
bird_y = ALTO // 2
bird_rect = pygame.Rect(bird_x - bird_size//2, bird_y - bird_size//2, bird_size, bird_size)

# Control eje
eje_control = "roll"  # o "pitch"
sensibilidad = 1.0  # ya no se usa directamente para mover pájaro

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Estados: 'calibrar_min', 'calibrar_max', 'jugando'
estado = "calibrar_min"

roll_min = None
roll_max = None

def dibujar_boton(rect, texto, color_fondo, color_texto=NEGRO):
    pygame.draw.rect(pantalla, color_fondo, rect)
    txt = font.render(texto, True, color_texto)
    pantalla.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

boton_min_rect = pygame.Rect(ANCHO//4 - 60, ALTO - 80, 120, 50)
boton_max_rect = pygame.Rect(3*ANCHO//4 - 60, ALTO - 80, 120, 50)

frame_count = 0

roll_suave = 0.5  # inicializamos en mitad

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos
            if estado == "calibrar_min" and boton_min_rect.collidepoint(mx, my):
                accX, accY, accZ = obtener_valores()
                _, roll = calcular_pitch_roll(accX, accY, accZ)
                roll_min = roll
                estado = "calibrar_max"
            elif estado == "calibrar_max" and boton_max_rect.collidepoint(mx, my):
                accX, accY, accZ = obtener_valores()
                _, roll = calcular_pitch_roll(accX, accY, accZ)
                roll_max = roll
                if roll_max != roll_min:
                    estado = "jugando"
                    bird_y = ALTO // 2
                    bird_rect.y = bird_y - bird_size//2
                    frame_count = 0
                    roll_suave = 0.5  # reiniciar suavizado

    pantalla.fill(AZUL_CIELO)

    if estado == "calibrar_min":
        texto = font.render("Mueve al roll MIN y presiona OK MIN", True, NEGRO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 100))
        dibujar_boton(boton_min_rect, "OK MIN", AZUL)

    elif estado == "calibrar_max":
        texto = font.render("Mueve al roll MAX y presiona OK MAX", True, NEGRO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 100))
        dibujar_boton(boton_max_rect, "OK MAX", AZUL)

    elif estado == "jugando":
        frame_count += 1

        accX, accY, accZ = obtener_valores()
        _, roll = calcular_pitch_roll(accX, accY, accZ)

        roll_norm = (roll - roll_min) / (roll_max - roll_min)
        roll_norm = max(0, min(1, roll_norm))

        # Filtro suavizado (EMA)
        alpha = 0.1
        roll_suave = alpha * roll_norm + (1 - alpha) * roll_suave

        desplazamiento_x = frame_count * velocidad

        amplitud_pix = ALTO / 3
        y_centro = ALTO // 2

        y_sinusoide = y_centro + amplitud_pix * math.sin(frecuencia * (frame_count * velocidad + bird_x))

        # Usar roll_suave para mover el pájaro suavemente
        bird_y = y_centro - amplitud_pix + roll_suave * (2 * amplitud_pix)
        bird_rect.y = int(bird_y - bird_size // 2)

        puntos = []
        for x in range(ANCHO):
            y = y_centro + amplitud_pix * math.sin(frecuencia * (x + desplazamiento_x))
            puntos.append((x, int(y)))
        if len(puntos) > 1:
            pygame.draw.lines(pantalla, VERDE, False, puntos, 3)

        pygame.draw.rect(pantalla, AMARILLO, bird_rect)

    pygame.display.flip()
    clock.tick(30)
