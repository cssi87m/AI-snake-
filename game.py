import pygame 
import time 
import random
import numpy as np
from Model import *
from USR_buffer import USR
from para_initializer import *

model = Model()
model.compile(loss = 'mse', optimizer = 'adam', metrics = ['mae'])
target_network = Model()
target_network.compile(loss = 'mse', optimizer = 'adam', metrics = ['mae'])
usr = USR()

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

# fruit position 
fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y //10)) * 10]
fruit_spawn = True # check whether fruit is eaten or not 
# default snake direction is right 
direction = 'RIGHT'
change_to = direction 
state = np.ones(11).reshape(-1, 1)
reward = 0
def restart():
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    # snake_body=[[100, 50], [90, 50], [80, 50]]
    fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y //10)) * 10]
    fruit_spawn = True
    return snake_position, snake_body, fruit_position, fruit_spawn
''' Calculate state. The state is [danger straight, danger right, danger left, direction left, direction right, direction up, 
direction down, food left, food right, food up, food down]. If any factor is right, set value to 0, otherwise 1'''
def snake_direction(direction):
    if direction == 'RIGHT':
        STRAIGHT = 'RIGHT'
        RIGHT = 'DOWN'
        LEFT = 'UP'
    if direction == 'LEFT':
        STRAIGHT = 'LEFT'
        RIGHT = 'UP'
        LEFT = 'DOWN'
    if direction == 'UP':
        STRAIGHT = 'UP'
        RIGHT = 'RIGHT'
        LEFT = 'LEFT'
    if direction == 'DOWN':
        STRAIGHT = 'DOWN'
        RIGHT = 'LEFT'
        LEFT = 'RIGHT'
    return STRAIGHT, RIGHT, LEFT
def cal_state(direction, snake_position, fruit_position, snake_body):
    # state.numpy()
    state = np.ones((1, 11))
    STRAIGHT, RIGHT, LEFT = snake_direction(direction)

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            state[0][0] = 0  # Collision with body
    
    if (STRAIGHT, RIGHT, LEFT) == ('RIGHT', 'DOWN', 'UP'):
        # check whether nearly collide with the wall
        if window_x - snake_position[0] == 10: state[0][0] = 0
        if window_y - snake_position[1] == 10: state[0][1] = 0 
        if snake_position[1] == 10: state[0][2] = 0
        # check danger whether nearly collide with the body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] - block[1] == 10: 
                if state[0][1] == 1: state[0][1] = 0  
            if snake_position[0] == block[0] and block[1] - snake_position[1] == 10:
                if state[0][2] == 1: state[0][2] = 0
        state[0][3] = 1 # direction left 
        state[0][4] = 0 # direction right 
        state[0][5] = 1 # direction up
        state[0][6] = 1 # direction down 
        if fruit_position[1] < snake_position[1]: state[0][7] = 0 # food left 
        if fruit_position[1] > snake_position[1]: state[0][8] = 0 # food right 
        if fruit_position[0] > snake_position[0]: state[0][9] = 0 # food up 
        if fruit_position[0] < snake_position[0]: state[0][10] = 0 # food down 
    
    if (STRAIGHT, RIGHT, LEFT) == ('LEFT', 'UP', 'DOWN'):
        # check whether nearly collide with the wall
        if snake_position[0] == 10: state[0][0] = 0
        if snake_position[1] == 10: state[0][1] = 0 
        if window_y - snake_position[1] == 10: state[0][2] = 0
        # check danger whether nearly collide with the body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] - block[1] == -10: 
                if state[0][1] == 1: state[0][1] = 0  
            if snake_position[0] == block[0] and block[1] - snake_position[1] == -10:
                if state[0][2] ==1: state[0][2] = 0
        state[0][3] = 0 # direction left 
        state[0][4] = 1 # direction right 
        state[0][5] = 1 # direction up
        state[0][6] = 1 # direction down 
        if fruit_position[1] > snake_position[1]: state[0][7] = 0 # food left 
        if fruit_position[1] < snake_position[1]: state[0][8] = 0 # food right 
        if fruit_position[0] < snake_position[0]: state[0][9] = 0 # food up 
        if fruit_position[0] > snake_position[0]: state[0][10] = 0 # food down 
    
    if (STRAIGHT, RIGHT, LEFT) == ('UP', 'RIGHT', 'LEFT'):
        # check whether nearly collide with the wall
        if snake_position[1] == 10: state[0][0] = 0
        if window_x - snake_position[0] == 10: state[0][1] = 0 
        if snake_position[0] == 10: state[0][2] = 0
        # check danger whether nearly collide with the body
        for block in snake_body[1:]:
            if snake_position[1] == block[1] and snake_position[0] - block[0] == -10: 
                if state[0][1] == 1: state[0][1] = 0  
            if snake_position[1] == block[1] and block[0] - snake_position[0] == -10:
                if state[0][2] == 1: state[0][2] = 0
        state[0][3] = 1 # direction left 
        state[0][4] = 1 # direction right 
        state[0][5] = 0 # direction up
        state[0][6] = 1 # direction down 
        if fruit_position[0] < snake_position[0]: state[0][7] = 0 # food left 
        if fruit_position[0] > snake_position[0]: state[0][8] = 0 # food right 
        if fruit_position[1] < snake_position[1]: state[0][9] = 0 # food up 
        if fruit_position[1] > snake_position[1]: state[0][10] = 0 # food down 

    if (STRAIGHT, RIGHT, LEFT) == ('DOWN', 'LEFT', 'RIGHT'):
        # check whether nearly collide with the wall
        if window_y - snake_position[1] == 10: state[0][0] = 0
        if snake_position[0] == 10: state[0][1] = 0 
        if window_x - snake_position[0] == 10: state[0][2] = 0
        # check danger whether nearly collide with the body
        for block in snake_body[1:]:
            if snake_position[1] == block[1] and snake_position[0] - block[0] == 10: 
                if state[0][1] == 1: state[0][1] = 0  
            if snake_position[1] == block[1] and block[0] - snake_position[0] == 10:
                if state[0][2] ==1: state[0][2] = 0
        state[0][3] = 1 # direction left 
        state[0][4] = 0 # direction right 
        state[0][5] = 1 # direction up
        state[0][6] = 1 # direction down 
        if fruit_position[1] < snake_position[1]: state[0][7] = 0 # food left 
        if fruit_position[1] > snake_position[1]: state[0][8] = 0 # food right 
        if fruit_position[0] > snake_position[0]: state[0][9] = 0 # food up 
        if fruit_position[0] < snake_position[0]: state[0][10] = 0 # food down 
    return state

def dis_fruit_snake(snake_position, fruit_position, direction):
    def normalizer(arr):
        sum = arr[0][0] + arr[0][1] + arr[0][2]
        return [[(arr[0][0] + 1) / (sum + 3), (arr[0][1] + 1)/ (sum + 3), (arr[0][2] + 1)/ (sum + 3)]]
    straight, right, left = snake_direction(direction)
    if (straight, right, left) == ('RIGHT', 'DOWN', 'UP'):
        res = [[max(fruit_position[0] - snake_position[0], 0), max(fruit_position[1] - snake_position[1], 0), max(snake_position[1] - fruit_position[1], 0)]]
    if (straight, right, left) == ('LEFT', 'UP', 'DOWN'):
        res = [[max(snake_position[0] - fruit_position[0], 0), max(snake_position[1] - fruit_position[1], 0), max(fruit_position[1] - snake_position[1], 0)]]
    if (straight, right, left) == ('UP', 'RIGHT', 'LEFT'):
        res = [[max(snake_position[1] - fruit_position[1], 0), max(fruit_position[0] - snake_position[0], 0), max(snake_position[0] - fruit_position[0], 0)]]
    if (straight, right, left) == ('DOWN', 'LEFT', 'RIGHT'):
        res = [[max(fruit_position[1] - snake_position[1], 0), max(snake_position[0] - fruit_position[0], 0), max(fruit_position[0] - snake_position[0], 0)]]
    return normalizer(res) 

# score of player 
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
    # pygame.quit()
    # quit()

while True:
    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_UP:
    #             change_to = 'UP'
    #         if event.key == pygame.K_DOWN:
    #             change_to = 'DOWN'
    #         if event.key == pygame.K_RIGHT:
    #             change_to = 'RIGHT'
    #         if event.key == pygame.K_LEFT:
    #             change_to = 'LEFT'
    # Use epsilon-greedy policy to select action
    if random.random() < eps:
        straight, left, right = snake_direction(direction)
        change_to = random.choice([straight, left, right])
        if change_to == straight: action_index = 0
        elif change_to == left: action_index = 1 
        else: action_index = 2
    
    else:
        straight, left, right = snake_direction(direction)
        action_index = np.argmax(model.predict(state.reshape(1, 11)) - dis_fruit_snake(fruit_position, snake_position, direction))
        if action_index == 0 : change_to = straight
        elif action_index == 1 : change_to = left 
        else : change_to = right 
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    new_state = cal_state(direction, snake_position, fruit_position, snake_body)
    # Moving the snake 
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10 
    if direction == 'RIGHT':
        snake_position[0] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    # if snake and fruit collide then scores will be incremented by 10
    snake_body.insert(0, list(snake_position))

    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        reward = 10
        fruit_spawn = False 
    else: 
        snake_body.pop()
    if not game_over() and fruit_spawn:
        reward += 1
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10, random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True 
    game_window.fill(black)

    pygame.draw.rect(game_window, blue, pygame.Rect(snake_position[0], snake_position[1], 10, 10))
    for pos in snake_body[1:]:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    
    # Game Over condition 
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        reward = -10
        print(snake_position, snake_body)
        snake_position, snake_body, fruit_position, fruit_spawn = restart()
        game_over()
        score = 0
        print (reward, target, eps)
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        reward = -10 
        print(snake_position, snake_body)
        snake_position, snake_body, fruit_position, fruit_spawn = restart()
        game_over()
        score = 0
        print (reward, target, eps)
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            reward = -10
            print(snake_position, snake_body)
            snake_position, snake_body, fruit_position, fruit_spawn = restart()
            game_over()
            score = 0
            print (reward, target, eps)   
            break 
    
    # # long-term return 
    # l_return = 0
    # if not game_over():
    #     l_return += learn_factor * reward
    #     learn_factor *= LEARN_FACTOR 
    # else:
    #     l_return = 0
    #     learn_factor = LEARN_FACTOR
    # experience replay buffer
    if reward > -10:
        experience = (state, action_index, new_state, reward) 
        usr.append(experience)
        
    if len(usr) >= BATCH_SIZE:
        mini_batch = usr.sample(2)
        for experience in mini_batch:
            rep_state, rep_action_index, rep_new_state, rep_reward = experience
            target = reward + discount_factor * np.max(target_network.predict(rep_new_state.reshape(-1, 11))) # calculate target by target_network 
            q_values = model.predict(rep_state.reshape(-1, 11))
            q_values[0, action_index] = target 
            model.fit(rep_state.reshape(1, 11), q_values.reshape(1, 3), verbose = 0) # training model using reply state 
            total_steps += 1
        if total_steps % TARGET_UPDATE_FREQUENCY == 0:
            target_network.set_weights(model.get_weights())
    
    # calculate the target function
    target = reward + discount_factor * np.max(model.predict(new_state.reshape(-1, 11)))
    # target += LEARNING_RATE * (l_return - target)
    target_vector = model.predict(state.reshape(1, 11))
    target_vector[0, action_index] = target
    model.fit(state.reshape(1, 11), target_vector.reshape(-1, 3), epochs = 1, verbose = 0)
    state = new_state
    eps *= eps_decay_factor
    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(snake_speed)