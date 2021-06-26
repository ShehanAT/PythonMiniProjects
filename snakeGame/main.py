import random

import pygame
import random
import sys 

pygame.init()
 
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
 
block_color = (53,115,255)
 
car_width = 73
 
win = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game by Shehan Atukorala')
clock = pygame.time.Clock()



def setup_snake_food(food_position):
    new_food_position = [random.randrange(1, (display_width//10))* 10, random.randrange(1, (display_height//10)) * 10]
    return new_food_position

def end_game():
    pygame.quit();
    sys.exit()

def game_loop():
    difficulty = 25;
    x = display_width/2
    y = display_height/2
    snake_position = [display_width/2, display_height/2]
    snake_body = [[display_width/2, display_height/2], [(display_width/2)-10, display_height/2], [(display_width/2)-(2*10), display_width/2]]
    snake_width = 20
    snake_height = 20
    snake_speed = 5
    snake_direction = "UP"
    new_direction = snake_direction 
    gameExit = False
    game_score = 0;

    food_position = setup_snake_food([0, 0])
    show_food = True 

    while not gameExit:
        pygame.time.delay(10)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            break
        if keys[pygame.K_LEFT]:
            new_direction = "LEFT";
        if keys[pygame.K_RIGHT]:
            new_direction = "RIGHT";
        if keys[pygame.K_UP]:
            new_direction = "UP";
            
 
        if keys[pygame.K_DOWN]:
            new_direction = "DOWN";
        if snake_direction != "UP" and new_direction == "DOWN":
            snake_direction = new_direction
        if snake_direction != "DOWN" and new_direction == "UP":
            snake_direction = new_direction
        if snake_direction != "LEFT" and new_direction == "RIGHT":
            snake_direction = new_direction
        if snake_direction != "RIGHT" and new_direction == "LEFT":
            snake_direction = new_direction

        if snake_direction == "UP":
            snake_position[1] -= snake_speed
        if snake_direction == "DOWN":
            snake_position[1] += snake_speed;
        if snake_direction == "LEFT":
            snake_position[0] -= snake_speed;
        if snake_direction == "RIGHT":
            snake_position[0] += snake_speed;

        snake_body.insert(0, list(snake_position));
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            print("snake ate food!");
            game_score += 10;
            show_food = False;
        else:
            snake_body.pop();

        if not show_food:
            new_food_position = setup_snake_food(food_position);
            food_position = new_food_position;
            show_food = True ;


        win.fill(black);
        for pos in snake_body:
            # Draw all parts of the snake
            pygame.draw.rect(win, (255, 255, 255), pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food 
        pygame.draw.rect(win, (255, 0, 255), (food_position[0], food_position[1], snake_width/2, snake_height/2));
    
        # if snake head hits the edge of the screen then end game
        if snake_position[0] < 0 or snake_position[0] > (display_width - snake_width/2):
            end_game();
        if snake_position[1] < 0 or snake_position[1] > (display_height - snake_height/2):
            end_game();            

        pygame.display.update();

        clock.tick(difficulty);

game_loop();
pygame.quit();
quit();
