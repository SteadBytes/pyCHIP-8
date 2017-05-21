#!/usr/bin/env python3

import chip8
import sys
import pygame
import time
pygame.init()


def main(program):
    chip_8 = chip8.Chip8()
    keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
            pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
    width = 64
    height = 32
    colours = [(0, 0, 0), (255, 255, 255)]  # 0 for black, 1 for white
    pixels = width * height
    # Actual window size=10xlarger than 64x32
    # pygame display takes tuple of width,height
    scale_factor = 10
    screenSize = (width * scale_factor, height * scale_factor)

    # Setup display
    icon = pygame.image.load("res/icon.gif")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("pyCHIP-8")

    initGraphics(screen)

    chip_8.initialize(pixels)
    chip_8.loadProgram(program)

    cycle_start_time = time.time()
    opcode_frequency = 10
    op_count = 0
    while True:
        if time.time() - cycle_start_time > 1 / 60:
            cycle_start_time = time.time()
            op_count = 0
            if chip_8.delay_timer > 0:
                chip_8.delay_timer -= 1
            if chip_8.sound_timer > 0:
                sys.stdout.write("\a")  # ASCII Bell
                chip_8.sound_timer -= 1
        if op_count <= opcode_frequency:
            chip_8.emulateCycle()
            op_count += 1

            if chip_8.draw_flag:
                drawGraphics(screen, colours, chip_8,
                             width, height, scale_factor)

            all_events = pygame.event.get()
            key_events(all_events, keys, chip_8)


def initGraphics(screen):
    # Blank black screen
    screen.fill((0, 0, 0))


def drawGraphics(screen, colors, chip_8, width, height, scale_factor):
    for x in range(0, width):
        for y in range(0, height):
            # Actual window size upscaled 10x
            rect = pygame.Rect(x * scale_factor, y *
                               scale_factor, scale_factor, scale_factor)
            color_index = chip_8.graphics[x + (y * width)]
            screen.fill(colors[color_index], rect)

    pygame.display.flip()  # Update screen
    chip_8.draw_flag = False


def key_events(events, keys, chip_8):
    for event in events:
        key_event = -1
        if event.type == pygame.KEYDOWN:
            key_event = 1
        elif event.type == pygame.KEYUP:
            key_event = 0
        elif event.type == pygame.QUIT:
            sys.exit(0)

        if key_event == 0 or key_event == 1:
            if event.key in keys:
                # Get location of key in keys array
                key_index = keys.index(event.key)
                chip_8.keys[key_index] = key_event


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error : script and game required")
        sys.exit
    else:
        program = sys.argv[1]
        main(program)
