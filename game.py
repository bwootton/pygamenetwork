import select
import socket
import struct
import sys

import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT,K_RIGHT,K_ESCAPE,KEYDOWN,QUIT


class MessageChannel(object):
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind(("{}".format("0.0.0.0"), port))

    def get_message_list(self):
        input_ready, output_ready, except_ready = select.select([self.sock],[],[],0)
        data = [s.recv(1500).decode('ascii') for s in input_ready]
        return data

    def send_message(self, address, port, message):
        message_bytes = message.encode('ascii')
        self.sock.sendto(message_bytes, (address, port))



def play_game(my_port, other_port):
    pygame.init()


    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True

    state = {'a':1}

    message_channel = MessageChannel(my_port)

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    circle = Circle(screen)
    circle.redraw()

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # controls
                if event.key == pygame.K_DOWN:
                    circle.move_y(10)
                elif event.key == pygame.K_UP:
                    circle.move_y(-10)
                elif event.key == pygame.K_RIGHT:
                    circle.move_x(10)
                elif event.key == pygame.K_LEFT:
                    circle.move_x(-10)


        # handle any new messages
        for message in message_channel.get_message_list():
           print(message)


        # Flip the display
        pygame.display.flip()
    # Done! Time to quit.
    pygame.quit()

def print_add(a, b):
    c = a + b
    print(c)

class Circle(object):
    def __init__(self, screen):
        self.x = 250
        self.old_x = 250
        self.y = 250
        self.old_y = 250
        self.screen = screen

    def move_x(self, distance):
        self.x = self.x + distance
        self.redraw()

    def move_y(self, distance):
        self.y = self.y + distance
        self.redraw()

    def redraw(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.old_x, self.old_y), 10)
        self.old_x = self.x
        self.old_y = self.y
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x, self.y), 10)

def erase_circle(x, y , screen):
    pygame.draw.circle(screen, (255, 255,255), (x, y), 10)

def draw_circle(x, y , screen):
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 10)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python screen1.py <my_port>, <peer_port>")
    else:
        play_game(int(sys.argv[1]), int(sys.argv[2]))
        