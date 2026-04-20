import pygame
import time
import math

pygame.init()

WIDTH, HEIGHT = 900, 835    # size of window(pygame)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock") #name of window


WHITE = (255, 255, 255) # what is white

left = pygame.image.load('/Users/zansezim/Practice/Lab9/mickeys_clock/left-hand.png')
right = pygame.image.load('/Users/zansezim/Practice/Lab9/mickeys_clock/right-hand.png')
background = pygame.image.load('/Users/zansezim/Practice/Lab9/mickeys_clock/main-clock.png')       #uploading

bg_rect = background.get_rect(center=(WIDTH // 2, HEIGHT // 2))

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2 + 50       # defining the center

OFFSET_Y = -40  # for sync

left_rect = left.get_rect()
right_rect = right.get_rect()       # to control

left_rect = left.get_rect(center=(CENTER_X, CENTER_Y + OFFSET_Y))
right_rect = right.get_rect(center=(CENTER_X, CENTER_Y + OFFSET_Y)) 

def rotate_and_blit(image, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=pivot)     
    screen.blit(rotated_image, rotated_rect.topleft)        #Rotates image around its center and draws it at the pivot point

    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False

    current_time = time.localtime() #setting up the time
    seconds = current_time.tm_sec
    minutes = current_time.tm_min

    second_angle = (-seconds * 6) + 90 
    minute_angle = (-minutes * 6) + 90

   
    screen.fill(WHITE)

    screen.blit(background, bg_rect)

    rotate_and_blit(left, second_angle, (CENTER_X, CENTER_Y))  
    rotate_and_blit(right, minute_angle, (CENTER_X, CENTER_Y)) 

    pygame.display.flip()
    pygame.time.delay(100)  

pygame.quit()
