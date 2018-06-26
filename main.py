#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon March 5 16:52:52 2017

@author: keruiliu
"""

import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
import random
import os

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 852
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('Aircraft Battle')
background = pygame.image.load('image/background.png').convert()

# Load music
pygame.mixer.music.load('sound/game_music.wav')
pygame.mixer.music.set_volume(0.3)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/big_spaceship_flying.wav')
enemy3_fly_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_double_laser.wav')
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound('sound/game_over.wav')
me_down_sound.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

black = (0,0,0)
green = (0,255,0)
red = (255,0,0)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e = enemy.SmallEnemy(bg_size)
        group1.add(e)
        group2.add(e)
        
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e = enemy.MidEnemy(bg_size)
        group1.add(e)
        group2.add(e)
        
def add_big_enemies(group1, group2, num):
    for i in range(num):
        e = enemy.BigEnemy(bg_size)
        group1.add(e)
        group2.add(e)

def increase_speed(target, num):
    for i in target:
        i.speed += 1
    
    
def main():
    
    pygame.mixer.music.play(-1)
   
    me = myplane.MyPlane(bg_size)
    
    enemies = pygame.sprite.Group()
        
    # Initialize small enemies
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 50)
    
    # Initialize mid enemies
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 15)
    
    # Initialize big enemies
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 6)
    
    clock = pygame.time.Clock()
    
    # Control the aircraft destroy effect
    small_destroy_index = 0
    mid_destroy_index = 0
    big_destroy_index = 0
    me_destroy_index = 0
    
    # Control the dynamic effect of images
    switch_image = True
    delay = 100
    
    # You have three life points
    life = 3
    life_image = pygame.image.load('image/lifejet.png').convert_alpha()
    life_rect = life_image.get_rect()
    
    # Initialize score
    score = 0
    score_font = pygame.font.Font('SentyCreamPuff.ttf',36)
    final_score_font = pygame.font.Font('SentyCreamPuff.ttf',48)
    
    # Pause button stuff
    paused = False
    pause_regular_image = pygame.image.load('image/game_pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('image/game_pause_pressed.png').convert_alpha()
    resume_regular_image = pygame.image.load('image/game_resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('image/game_resume_pressed.png').convert_alpha()
    pause_rect = pause_regular_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 5, 5
    pause_image = pause_regular_image
    
    pause_animation1 = pygame.image.load('image/game_loading1.png').convert_alpha()
    pause_animation2 = pygame.image.load('image/game_loading2.png').convert_alpha()
    pause_animation3 = pygame.image.load('image/game_loading3.png').convert_alpha()
    
    # Game difficulty level
    level = 1
    
    # Full Screen bomb!
    bomb_image = pygame.image.load('image/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('SentyCreamPuff.ttf',48)
    bomb_num = 0 # Without any bomb at the very beginning
    
    # Bomb supply + bullet supply
    bomb_supply = supply.BombSupply(bg_size)
    bullet_supply = supply.BulletSupply(bg_size)
    supply_timer = USEREVENT
    pygame.time.set_timer(supply_timer, 30*1000)
    
    
    # Double bullet timer
    double_bullet_timer = USEREVENT + 1
    is_double_bullets = False
    
    # Invincible period timer
    invincible_timer = USEREVENT + 2
    
    # Create regular bullets
    bullets1 = []
    bullet1_index = 0
    bullet_num = 6
    for i in range(bullet_num):
        bullet_position = (me.rect.midtop[0]-3,me.rect.midtop[1])
        bullets1.append(bullet.Bullet(bullet_position))
    
    # Create double bulltes
    bullets2 = []
    bullet2_index = 0
    double_num = 8
    for i in range(double_num):
        bullets2.append(bullet.DoubleBullet((me.rect.centerx-35,me.rect.centery)))
        bullets2.append(bullet.DoubleBullet((me.rect.centerx+28,me.rect.centery)))
    
    # Set bullets to be regular bullets initially
    bullets = bullets1
    
    # Play again button
    again_image = pygame.image.load('image/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    again_rect.left += 150
    again_rect.top += 450
    
    terminated = False
    
    running = True
    
    while running:
        
        # Draw background
        screen.blit(background, (0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Click to pause the game 
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and life == 0 and again_rect.collidepoint(event.pos):
                    # Restart the game
                    main()  
                elif event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(supply_timer,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_timer,30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            
            # When cursor is moving and interact with the pause button
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image
                else:
                    if paused:
                        pause_image = resume_regular_image
                    else:
                        pause_image = pause_regular_image
            
            # Hit space bar and use the full-screen bomb
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        for e in enemies:
                            if e.rect.bottom > 0:
                                e.alive = False
            
            # Provide a supply every 30s
            elif event.type == supply_timer:
                if random.random()>0.5:
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
                    
            # Double firing period
            elif event.type == double_bullet_timer:
                is_double_bullets = False
                pygame.time.set_timer(double_bullet_timer,0)
                
            elif event.type == invincible_timer:
                me.invincible = False
                pygame.time.set_timer(invincible_timer,0)
         
        # Delay effect, avoid image switching too fast
        delay -= 1
        if delay == 0:
            delay = 100
        if not(delay%10):
            switch_image = not switch_image   
            
        # Draw score
        score_text = score_font.render('Score: %s' % str(score), True, black)
        screen.blit(score_text, (5,5))
        
        # Draw pause or resume buttion
        screen.blit(pause_image,pause_rect)
        if paused and delay%33>22:
            screen.blit(pause_animation1,(90,380))
        elif paused and delay%33>11:
            screen.blit(pause_animation2,(140,380))
        elif paused:
            screen.blit(pause_animation3,(190,380))
        
        # Draw bombs
        bomb_text = bomb_font.render('x %d' % bomb_num, True, black)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
        screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
        
        # Draw life points
        for i in range(life):
            life_rect.left = width - 50*(i+1)
            life_rect.top = height - 70
            screen.blit(life_image,life_rect)
        
        
        # Control the game difficulty level
        if level == 1 and score > 2000:
            level = 2
            add_small_enemies(small_enemies,enemies,10)
            add_mid_enemies(mid_enemies,enemies,5)
            add_big_enemies(big_enemies,enemies,2)
            increase_speed(small_enemies,1)
        
        if level == 2 and score > 5000:
            level = 3
            #add_small_enemies(small_enemies,enemies,10)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            increase_speed(small_enemies,1)
            increase_speed(mid_enemies,1)
        
        if level == 3 and score > 10000:
            level = 4
            #add_small_enemies(small_enemies,enemies,10)
            add_mid_enemies(mid_enemies,enemies,2)
            add_big_enemies(big_enemies,enemies,1)
            increase_speed(small_enemies,1)
            increase_speed(mid_enemies,1)
            increase_speed(big_enemies,1)
        
        # Only play when the game is unpaused
        if (not paused) and life:
            # Player's control
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            
                
            # Draw bomb supply and test whether player gets it
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            
            # Draw bullet supply and test whether player gets it
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    # Double bullets fire!
                    is_double_bullets = True
                    pygame.time.set_timer(double_bullet_timer,20*1000)
                    bullet_supply.active = False
            
            
            # Bullets, both regular and double
            if is_double_bullets and not(delay%5):
                bullet_sound.play()
                bullets = bullets2
                bullets[bullet2_index].reset((me.rect.centerx-35,me.rect.centery))
                bullets[bullet2_index+1].reset((me.rect.centerx+28,me.rect.centery))
                bullet2_index = (bullet2_index+2)%(double_num*2)
            
            elif not is_double_bullets and not(delay%10):
                bullets = bullets1
                bullet_position = (me.rect.midtop[0]-3,me.rect.midtop[1])
                bullets[bullet1_index].reset(bullet_position)
                bullet1_index = (bullet1_index+1)%bullet_num
            
            
            # Draw bullet and Collision test (bullet and enemy)
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.hp -= 1
                                if e.hp == 0:
                                    e.alive = False
                            else:
                                # If hit a small enemy
                                e.alive = False
            
            
            # Collision test (jet and enemy)
            crashed = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if crashed and not me.invincible:
                me.alive = False
                for e in crashed:
                    e.alive = False
                    
            # Draw big enemies
            for e in big_enemies:
                if e.alive:
                    e.move()
                    if e.hit:
                        # Show some damage effects
                        screen.blit(e.image_hit, e.rect)
                        e.hit = False
                    else:
                        if switch_image:
                            screen.blit(e.image, e.rect)
                        else:
                            screen.blit(e.image1, e.rect)
                    if e.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                
                    # Draw hp bar
                    pygame.draw.line(screen, black, \
                                     (e.rect.left, e.rect.bottom + 5), \
                                     (e.rect.right, e.rect.bottom +5), 2)
                    hp_percentage = float(e.hp)/enemy.BigEnemy.hp
                    if hp_percentage > 0.3:
                        hp_color = green
                    else:
                        hp_color = red
                    pygame.draw.line(screen, hp_color, \
                                     (e.rect.left, e.rect.bottom + 5), \
                                     (e.rect.left+e.rect.width*hp_percentage, \
                                      e.rect.bottom + 5), 2)
                
                else: 
                    # Enemy blows up!
                    # Use the delay effect to entend the time interval among
                    # blow up images, make the blow animation better 
                    screen.blit(e.destroy_images[big_destroy_index],e.rect)
                    if not(delay%3):
                        # Only play the sound once per explosion
                        if big_destroy_index == 0:
                            enemy3_down_sound.play()
                        # Keep the index value between 0 and 5
                        big_destroy_index = (big_destroy_index+1)%6
                        if big_destroy_index == 0:
                            score += 1000
                            enemy3_fly_sound.stop()
                            e.reset()
                    
            
            # Draw mid enemies
            for e in mid_enemies:
                if e.alive:
                    e.move()
                    if e.hit:
                        # Show some damage effects
                        screen.blit(e.image_hit, e.rect)
                        e.hit = False
                    else:
                        screen.blit(e.image, e.rect)
                
                    # Draw hp bar
                    pygame.draw.line(screen, black, \
                                     (e.rect.left, e.rect.bottom + 5), \
                                     (e.rect.right, e.rect.bottom +5), 2)
                    hp_percentage = float(e.hp)/enemy.MidEnemy.hp
                    if hp_percentage > 0.3:
                        hp_color = green
                    else:
                        hp_color = red
                    pygame.draw.line(screen, hp_color, \
                                     (e.rect.left, e.rect.bottom + 5), \
                                     (e.rect.left+e.rect.width*hp_percentage, \
                                      e.rect.bottom + 5), 2)
                else:
                    # Enemy blows up!
                    # Use the delay effect to entend the time interval among
                    # blow up images, make the blow animation better 
                    screen.blit(e.destroy_images[mid_destroy_index],e.rect)
                    if not(delay%3):
                        # Only play the sound once per explosion
                        if mid_destroy_index == 0:
                            enemy2_down_sound.play()
                        # Keep the index value between 0 and 3
                        mid_destroy_index = (mid_destroy_index+1)%4
                        if mid_destroy_index == 0:
                            score += 100
                            e.reset()
            
            # Draw small enemies
            for e in small_enemies:
                if e.alive:
                    e.move()
                    screen.blit(e.image, e.rect)
                else:
                    # Enemy blows up!
                    # Use the delay effect to entend the time interval among
                    # blow up images, make the blow animation better 
                    screen.blit(e.destroy_images[small_destroy_index],e.rect)
                    if not(delay%3):
                        # Only play the sound once per explosion
                        if small_destroy_index == 0:
                            enemy1_down_sound.play()
                        # Keep the index value between 0 and 3
                        small_destroy_index = (small_destroy_index+1)%4
                        if small_destroy_index == 0:
                            score += 10
                            e.reset()
                
            # Draw hero jet
            if me.alive and not me.invincible:
                if switch_image:
                    screen.blit(me.image, me.rect)
                else:
                    screen.blit(me.image1, me.rect)
            elif me.alive and me.invincible:
                if delay%10>4:
                    screen.blit(me.image,me.rect)
            else:
                # Hero jet blows up!
                # Use the delay effect to entend the time interval among
                # blow up images, make the blow animation better 
                screen.blit(me.destroy_images[me_destroy_index],me.rect)
                if not(delay%3):
                    # Only play the sound once per explosion
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    # Keep the index value between 0 and 3
                    me_destroy_index = (me_destroy_index+1)%4
                    if me_destroy_index == 0:
                        life -= 1
                        # If has life points, continue playing
                        if life:
                            me.resurrect()
                            pygame.time.set_timer(invincible_timer, 2*1000)
                        # No life points left
                        else: 
                            print('Game Over!')
            
        elif not life:
            # Only conduct the following procedure once
            if not terminated:
                terminated = True
                # Terminate some stuff
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.time.set_timer(supply_timer,0)
                    
                # Historical highest score
                if not os.path.exists('record.txt'):
                    best_score = 0
                else:
                    with open('record.txt','r') as f:
                        best_score = int(f.read())
                        f.close()
                
                if score > best_score:
                    best_score = score
                    print(best_score)
                    with open('record.txt','w') as f:
                        f.write(str(score))
                        f.close()
            
            #gameover_image = pygame.image.load('image/background.png').convert_alpha()
            final_score_text = final_score_font.render('Final Score: %s' % str(score), True, black)
            best_score_text = score_font.render('Highest Score: {}'.format(best_score), True, black)
            again_image = pygame.image.load('image/again.png').convert_alpha()
            again_rect = again_image.get_rect()
            again_rect.left += 150
            again_rect.top += 400
            screen.blit(background,(0,0))
            screen.blit(best_score_text,(20,20))
            screen.blit(final_score_text,(70,270))
            screen.blit(again_image,again_rect)
            
            
            
            
            
        pygame.display.flip()
        
        clock.tick(60)
    
    '''
    if gameover:
        gameover_image = pygame.image.load('image/background.png').convert_alpha()
        final_score_text = final_score_font.render('Score: %s' % str(score), True, black)
        
        while(1):
            screen.blit(background,(0,0))
            screen.blit(final_score_text, (100,100))
            
        
        pygame.display.flip()
        
        clock.tick(60)'''
  
      
if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
