import pygame 
import time 
import random
import numpy as np
# Initiate parameters for game 
snake_speed = 100
window_x = 720 
window_y = 480
#  Define color 
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
# Initilaizing pygame 
pygame.init()

# Initialize game window 
pygame.display.set_caption("Snake game")
game_window = pygame.display.set_mode((window_x, window_y))

# FPS
fps = pygame.time.Clock()

# Default snake position 
snake_position = [100, 50]
# Define first 4 blocks of snake (at first length of the snake is 4)
snake_body=[[100, 50], [90, 50], [80, 50], [70, 50]]
# snake_body=[[100, 50], [90, 50], [80, 50]]

direction = 'RIGHT'
change_to = direction

# fruit position 
fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y //10)) * 10]
fruit_spawn = True

def restart():
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    # snake_body=[[100, 50], [90, 50], [80, 50]]
    fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y //10)) * 10]
    fruit_spawn = True
    return snake_position, snake_body, fruit_position, fruit_spawn


score = 0
def show_score (choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: '+ str(score), True, color)
    score_rec=score_surface.get_rect()
    game_window.blit(score_surface, score_rec)
# game over function 
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
     
    game_over_surface = my_font.render('Score is: ' + str(score), True, red)
    game_over_rec = game_over_surface.get_rect()
    game_over_rec.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface, game_over_rec)
    pygame.display.flip()

    # after 2 seconds, quit the program 
    time.sleep(1.5)

class Player:
    def __init__(self, snake_position, fruit_position, snake_body, direction):
        self.snake_position = snake_position
        self.fruit_position = fruit_position
        self.snake_body = snake_body
        self.direction = direction
        self.path = [snake_position]
        
    
    def snake_direction(self):
        if self.direction == 'RIGHT':
            STRAIGHT = 'RIGHT'
            RIGHT = 'DOWN'
            LEFT = 'UP'
        if self.direction == 'LEFT':
            STRAIGHT = 'LEFT'
            RIGHT = 'UP'
            LEFT = 'DOWN'
        if self.direction == 'UP':
            STRAIGHT = 'UP'
            RIGHT = 'RIGHT'
            LEFT = 'LEFT'
        if self.direction == 'DOWN':
            STRAIGHT = 'DOWN'
            RIGHT = 'LEFT'
            LEFT = 'RIGHT'
        return STRAIGHT, RIGHT, LEFT
    
    def dis(self, old_pos, new_pos):
        return abs(old_pos[0] - new_pos[0]) + abs(old_pos[1] - new_pos[1])
    
    def valid(self, pos):
        x, y = pos
        if x < 0 or x > 720: return False
        if y < 0 or y > 480: return False
        if pos in self.snake_body: return False 
        return True 
    
    def a_star(self, current, goal):
        if current == goal:
            self.path = [current]
        else:
            straight, right, left = self.snake_direction()
            new_current = None 
            if (straight, right, left) == ('RIGHT', 'DOWN', 'UP'):
                cand_move = {straight: (current[0] + 10, current[1]), right: (current[0], current[1] + 10), left: (current[0], current[1] - 10)}
                sorted_cand_move = sorted(cand_move.items(), key = lambda x:self.dis(x[1], goal))
                for move, pos in sorted_cand_move:
                    if self.valid(pos):
                        new_current = pos
                        new_move = move 
                        self.path.append(new_current)
                        break
            if (straight, right, left) == ('LEFT', 'UP', 'DOWN'):
                cand_move = {straight: (current[0] - 10, current[1]), right: (current[0], current[1] - 10), left: (current[0], current[1] + 10)}
                sorted_cand_move = sorted(cand_move.items(), key = lambda x:self.dis(x[1], goal))
                for move, pos in sorted_cand_move:
                    if self.valid(pos):
                        new_current =  pos
                        new_move = move 
                        self.path.append(new_current)
                        break
            if (straight, right, left) == ('UP', 'RIGHT', 'LEFT'):
                cand_move = {straight: (current[0], current[1] - 10), right: (current[0] + 10, current[1]), left: (current[0] - 10, current[1])}
                sorted_cand_move = sorted(cand_move.items(), key = lambda x:self.dis(x[1], goal))
                for move, pos in sorted_cand_move:
                    if self.valid(pos):
                        new_current =  pos
                        new_move = move
                        self.path.append(new_current)
                        break
            if (straight, right, left) == ('DOWN', 'LEFT', 'RIGHT'):
                cand_move = {straight: (current[0], current[1] + 10), right: (current[0] - 10, current[1]), left: (current[0] + 10, current[1])}
                sorted_cand_move = sorted(cand_move.items(), key = lambda x:self.dis(x[1], goal))
                for move, pos in sorted_cand_move:
                    if self.valid(pos):
                        new_current =  pos
                        new_move = move 
                        self.path.append(new_current)
                        break
            if new_current == None: game_over()
            else: 
                # self.a_star(new_current, goal)
                # return new_current, new_move 
                return new_move

player = Player(snake_position, fruit_position, snake_body, direction)
                
while True:
    change_to = player.a_star(snake_position, fruit_position)
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    

    # Moving the snake 
    player.direction = direction
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10 
    if direction == 'RIGHT':
        snake_position[0] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    
    snake_body.insert(0, list(snake_position))
    player.snake_position = snake_position
    player.snake_body = snake_body
    # if snake and fruit collide then scores will be incremented by 10
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False 
        print(player.path)
    else: 
        snake_body.pop()
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
        player.fruit_position = fruit_position # change the attribute fruit_position of the snake 
    fruit_spawn = True 
    game_window.fill(black)

    pygame.draw.rect(game_window, blue, pygame.Rect(snake_position[0], snake_position[1], 10, 10))
    for pos in snake_body[1:]:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # Game Over condition 
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        snake_position, snake_body, fruit_position, fruit_spawn = restart()
        player.snake_position = snake_position
        player.snake_body = snake_body
        player.fruit_position = fruit_position
        player.path = [snake_position]
        game_over()
        print(player.path)
        print('____________________________')
        score = 0
        
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        snake_position, snake_body, fruit_position, fruit_spawn = restart()
        player.snake_position = snake_position
        player.snake_body = snake_body
        player.fruit_position = fruit_position
        player.path = [snake_position]
        game_over()
        print(player.path)
        print('____________________________')
        score = 0
        
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            snake_position, snake_body, fruit_position, fruit_spawn = restart()
            player.snake_position = snake_position
            player.snake_body = snake_body
            player.fruit_position = fruit_position
            player.path = [snake_position]
            game_over()
            print(player.path)
            print('____________________________')
            score = 0
            break 

    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)