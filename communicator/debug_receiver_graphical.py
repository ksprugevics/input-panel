import pygame
import math
import pygame.locals
from ibcp_com import IbcpCom
from board import Board
import signal
import time
import threading

pygame.init()

HEIGHT = 700
WIDTH = 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Input board debug")

DARK_GRAY = (55, 55, 55)
BROWN = (143, 58, 13)
GRAY = (158, 158, 158)
YELLOW = (255, 255, 0)
DARK_YELLOW = (176, 171, 42)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
DARK_RED = (143, 13, 13)
BLUE = (0, 0, 255)
DARK_BLUE = (3, 5, 130)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

clicked_buttons = []
color_change_time = 0

font = pygame.font.Font(None, 20)

WINDOW.fill(DARK_GRAY)

def draw_screw(screen, center, radius, color_screw, color_cross, cross_width):
    pygame.draw.circle(screen, color_screw, center, radius)
    cross_length = 2 * radius - 5
    pygame.draw.rect(screen, color_cross, (center[0] - cross_length // 2, center[1] - cross_width // 2, cross_length, cross_width))
    pygame.draw.rect(screen, color_cross, (center[0] - cross_width // 2, center[1] - cross_length // 2, cross_width, cross_length))

def draw_pot(screen, center, radius, color_screw, color_line, line_width, value):
    pygame.draw.circle(screen, color_screw, center, radius)
    offset = -180
    angle_rad = math.radians(offset - value * 1.8)
    end_x = center[0] + int(radius * math.cos(angle_rad))
    end_y = center[1] - int(radius * math.sin(angle_rad))
    pygame.draw.line(screen, color_line, center, (end_x, end_y), line_width)

def draw_switch(screen, center, radius, color_screw, color_line, line_width, on):
    pygame.draw.circle(screen, color_screw, center, radius)
    offset = -180
    if on:
        angle_deg = 90
    else:
        angle_deg = -90
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

def draw(board):
    pygame.draw.rect(WINDOW, BROWN, (125, 175, 450, 350))

    draw_screw(WINDOW, (145, 195), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (555, 195), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (145, 505), 12, GRAY, BLACK, 3)
    draw_screw(WINDOW, (555, 505), 12, GRAY, BLACK, 3)

    pygame.draw.circle(WINDOW, YELLOW, (225, 350), 25)
    pygame.draw.circle(WINDOW, WHITE, (305, 350), 25)
    pygame.draw.circle(WINDOW, RED, (385, 350), 25)
    pygame.draw.circle(WINDOW, BLUE, (465, 350), 25)
    pygame.draw.circle(WINDOW, BLACK, (465, 450), 25)

    for b in clicked_buttons:
        if "B1" in b:
            pygame.draw.circle(WINDOW, DARK_YELLOW, (225, 350), 25)
        elif "B2" in b:
            pygame.draw.circle(WINDOW, GRAY, (305, 350), 25)
        elif "B3" in b:
            pygame.draw.circle(WINDOW, DARK_RED, (385, 350), 25)
        elif "B4" in b:
            pygame.draw.circle(WINDOW, DARK_BLUE, (465, 350), 25)
        if b.endswith("B"):
            pygame.draw.circle(WINDOW, GRAY, (465, 450), 25)

    draw_text('B1', font, BLACK, WINDOW, 225, 390)
    draw_text('B2', font, BLACK, WINDOW, 305, 390)
    draw_text('B3', font, BLACK, WINDOW, 385, 390)
    draw_text('B4', font, BLACK, WINDOW, 465, 390)
    draw_text('CTRL', font, BLACK, WINDOW, 465, 490)

    pygame.draw.circle(WINDOW, GREEN, (385, 450), 12)

    draw_pot(WINDOW, (225, 250), 20, WHITE, BLACK, 3, board.pot_1)
    draw_text('POT1', font, BLACK, WINDOW, 225, 290)

    draw_pot(WINDOW, (465, 250), 20, WHITE, BLACK, 3, board.pot_2)
    draw_text('POT2', font, BLACK, WINDOW, 465, 290)

    draw_dip_switch(WINDOW, (290, 225), DARK_BLUE, [board.channel_1, board.channel_2, board.channel_3, board.channel_4, False, False, False, False], 7, 40)
    draw_text('CH-1 to CH-8', font, BLACK, WINDOW, 345, 290)

    draw_switch(WINDOW, (225, 450), 20, GRAY, WHITE, 8, board.switch_1)
    draw_text('SW1', font, BLACK, WINDOW, 225, 490)

    draw_switch(WINDOW, (305, 450), 20, GRAY, WHITE, 8, board.switch_2)
    draw_text('SW2', font, BLACK, WINDOW, 305, 490)

    pygame.display.update()

def update_button_press(nr):
    clicked_buttons.append(nr)

def background_update_task(comms, board):
    while True:
        time.sleep(0.025)
        message = comms.listen()
        if message is None or not message:
            continue

        board.parse_message(message)

def graceful_exit(signal, frame, comms):
    print("Stopping Communicator and closing serial connection...")
    del comms
    exit(0)

if __name__ == "__main__":

    with IbcpCom() as comms:
        print("Waiting a bit for connection to establish...")
        time.sleep(3)
        signal.signal(signal.SIGINT, lambda sig, frame: graceful_exit(sig, frame, comms))

        initial_status = comms.send_command_and_await_response("STATUS")
        print(f"Initial state:\n{initial_status}")

        board = Board(initial_status)
        board.set_button_handler(Board.BUTTON_1_PRIMARY, update_button_press)
        board.set_button_handler(Board.BUTTON_2_PRIMARY, update_button_press)
        board.set_button_handler(Board.BUTTON_3_PRIMARY, update_button_press)
        board.set_button_handler(Board.BUTTON_4_PRIMARY, update_button_press)
        board.set_button_handler(Board.BUTTON_1_SECONDARY, update_button_press)
        board.set_button_handler(Board.BUTTON_2_SECONDARY, update_button_press)
        board.set_button_handler(Board.BUTTON_3_SECONDARY, update_button_press)
        board.set_button_handler(Board.BUTTON_4_SECONDARY, update_button_press)
        print("READY...")
        
        background_thread = threading.Thread(target=background_update_task, args=(comms, board))
        background_thread.daemon = True
        background_thread.start()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    exit()

            if len(clicked_buttons) != 0 and not color_change_time:
                color_change_time = time.time()

            if color_change_time and time.time() - color_change_time > 1:
                clicked_buttons = []
                color_change_time = None
            draw(board)
    