import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana
ANCHO = 600
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Evita la bola")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# Jugador (cuadrado)
jugador_tam = 50
jugador_x = ANCHO // 2 - jugador_tam // 2
jugador_y = ALTO - jugador_tam - 10
jugador_vel = 5

# Bola
bola_radio = 20
bola_x = random.randint(bola_radio, ANCHO - bola_radio)
bola_y = 0
bola_vel = 4

# Fuente para texto
fuente = pygame.font.SysFont(None, 48)

def texto_final(texto):
    texto_render = fuente.render(texto, True, ROJO)
    rect = texto_render.get_rect(center=(ANCHO//2, ALTO//2))
    pantalla.blit(texto_render, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Loop principal
reloj = pygame.time.Clock()
jugando = True

while jugando:
    reloj.tick(60)  # 60 FPS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Movimiento jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador_x > 0:
        jugador_x -= jugador_vel
    if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_tam:
        jugador_x += jugador_vel

    # Movimiento bola
    bola_y += bola_vel
    if bola_y > ALTO:
        bola_y = 0
        bola_x = random.randint(bola_radio, ANCHO - bola_radio)

    # Colisiones
    jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_tam, jugador_tam)
    bola_rect = pygame.Rect(bola_x - bola_radio, bola_y - bola_radio, bola_radio*2, bola_radio*2)
    if jugador_rect.colliderect(bola_rect):
        texto_final("¡Perdiste!")
        jugando = False

    # Dibujar todo
    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, BLANCO, jugador_rect)
    pygame.draw.circle(pantalla, ROJO, (bola_x, bola_y), bola_radio)
    pygame.display.flip()

pygame.quit()
sys.exit()
