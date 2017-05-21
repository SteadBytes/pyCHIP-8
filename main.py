#!/usr/bin/env python3

import chip8
import sys
import pygame
from pygame import gfxdraw, Rect

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
    screenSize = (width * 10, height * 10)

    screen = pygame.display.set_mode(screenSize)

    initGraphics(screen)

    chip_8.initialize(pixels)
    chip_8.loadProgram(program)

    while True:
        chip_8.emulateCycle()
        if chip_8.draw_flag:
            draw_graphics(screens, colours, chip_8, width, height)

        allEvents = pygame.event.get()
        key_events(events, keys, chip_8)


def initGraphics(screen):
    # Blank black screen
    screen.fill((0, 0, 0))


def drawGraphics(screen, colors, chip_8, width, height):
    for x in range(0, width):
        for y in range(0, height):
            # Actual window size upscaled 10x
            rect = Rect(x * 10, y * 10, 10, 10)
            colorIndex = chip8.graphics[x + (y * width)]
            screen.fill(colors[colorIndex], rect)

    pygame.display.flip()  # Update screen
    chip_8.draw_flag = False


def key_events(events, keys, chip_8):
    for event in events:
        key_event = -1
        if event.type == pygame.KEYDOWN:
            key_event = 1
        elif event.type == pygame.KEYUP:
            key_event = 0

        if key_event >= 0:
            if key.event in keys:
                # Get location of key in keys array
                keyIndex = keys.index(event.key)
                chip_8.keys[keyIndex] = key_event


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error : script and game required")
        sys.exit
    else:
        program = sys.argv[1]
        main(program)
