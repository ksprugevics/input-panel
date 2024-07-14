import pygame
import math
import pygame.locals

pygame.init()

HEIGHT = 700
WIDTH = 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Input board debug")

DARK_GRAY = (55, 55, 55)
BROWN = (143, 58, 13)
GRAY = (158, 158, 158)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
BLUE = (0, 0, 255)
DARK_BLUE = (3, 5, 130)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 20)

WINDOW.fill(DARK_GRAY)

def draw_screw(screen, center, radius, color_screw, color_cross, cross_width):
    pygame.draw.circle(screen, color_screw, center, radius)
    cross_length = 2 * radius - 5
    pygame.draw.rect(screen, color_cross, (center[0] - cross_length // 2, center[1] - cross_width // 2, cross_length, cross_width))
    pygame.draw.rect(screen, color_cross, (center[0] - cross_width // 2, center[1] - cross_length // 2, cross_width, cross_length))

def draw_pot(screen, center, radius, angle_deg, color_screw, color_line, line_width):
    pygame.draw.circle(screen, color_screw, center, radius)
    offset = -180
    angle_rad = math.radians(offset - angle_deg)
    end_x = center[0] + int(radius * math.cos(angle_rad))
    end_y = center[1] - int(radius * math.sin(angle_rad))
    pygame.draw.line(screen, color_line, center, (end_x, end_y), line_width)

def draw_dip_switch(screen, top_right, bg_color, truth_table, switch_width, switch_height):
    bg_rect = pygame.Rect(top_right[0], top_right[1], 110, 50)
    pygame.draw.rect(screen, bg_color, bg_rect)

    gap = 5
    truth_table.reverse()
    for i, state in enumerate(truth_table):
        switch_rect = pygame.Rect(top_right[0] - (i * (switch_width + gap)) - switch_width + 100,
                                  top_right[1] + gap,
                                  switch_width,
                                  switch_height)
        
        pygame.draw.rect(screen, GREEN if state else RED, switch_rect)

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            exit()
    pygame.draw.rect(WINDOW, BROWN, (125, 175, 450, 350))

    draw_screw(WINDOW, (145, 195), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (555, 195), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (145, 505), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (555, 505), 12, GRAY, BLACK, 3)

    pygame.draw.circle(WINDOW, YELLOW, (225, 350), 25)
    draw_text('B1', font, BLACK, WINDOW, 225, 390)

    pygame.draw.circle(WINDOW, WHITE, (305, 350), 25)
    draw_text('B2', font, BLACK, WINDOW, 305, 390)

    pygame.draw.circle(WINDOW, RED, (385, 350), 25)
    draw_text('B3', font, BLACK, WINDOW, 385, 390)

    pygame.draw.circle(WINDOW, BLUE, (465, 350), 25)
    draw_text('B4', font, BLACK, WINDOW, 465, 390)

    pygame.draw.circle(WINDOW, BLACK, (465, 450), 25)
    draw_text('CTRL', font, BLACK, WINDOW, 465, 490)

    pygame.draw.circle(WINDOW, GREEN, (385, 450), 12)

    draw_pot(WINDOW, (225, 250), 20, 0, WHITE, BLACK, 3)
    draw_text('POT1', font, BLACK, WINDOW, 225, 290)

    draw_pot(WINDOW, (465, 250), 20, 45, WHITE, BLACK, 3)
    draw_text('POT2', font, BLACK, WINDOW, 465, 290)

    draw_dip_switch(WINDOW, (290, 225), DARK_BLUE, [False, False, False, False, True, True, True, True], 7, 40)
    draw_text('CH-1 to CH-8', font, BLACK, WINDOW, 345, 290)

    draw_pot(WINDOW, (225, 450), 20, 270, GRAY, WHITE, 8)
    draw_text('SW1', font, BLACK, WINDOW, 225, 490)

    draw_pot(WINDOW, (305, 450), 20, 90, GRAY, WHITE, 8)
    draw_text('SW2', font, BLACK, WINDOW, 305, 490)

    pygame.display.update()
    