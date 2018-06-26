#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon March 5 22:52:07 2018

@author: keruiliu
"""

import pygame
from random import randint

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/enemy1.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('image/enemy1_down1.png').convert_alpha(), \
            pygame.image.load('image/enemy1_down2.png').convert_alpha(), \
            pygame.image.load('image/enemy1_down3.png').convert_alpha(), \
            pygame.image.load('image/enemy1_down4.png').convert_alpha() \
            ])
        self.alive = True
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)    
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.alive = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-3 * self.height, 0)
        
class MidEnemy(pygame.sprite.Sprite):
    hp = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/enemy2.png').convert_alpha()
        self.image_hit = pygame.image.load('image/enemy2_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('image/enemy2_down1.png').convert_alpha(), \
            pygame.image.load('image/enemy2_down2.png').convert_alpha(), \
            pygame.image.load('image/enemy2_down3.png').convert_alpha(), \
            pygame.image.load('image/enemy2_down4.png').convert_alpha() \
            ])
        self.alive = True
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image) 
        self.hp = MidEnemy.hp
        self.hit = False
             
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.alive = True
        self.hp = MidEnemy.hp
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-5 * self.height, -self.height)

class BigEnemy(pygame.sprite.Sprite):
    hp = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/enemy3_n1.png').convert_alpha()
        self.image1 = pygame.image.load('image/enemy3_n2.png').convert_alpha()
        self.image_hit = pygame.image.load('image/enemy3_hit.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('image/enemy3_down1.png').convert_alpha(), \
            pygame.image.load('image/enemy3_down2.png').convert_alpha(), \
            pygame.image.load('image/enemy3_down3.png').convert_alpha(), \
            pygame.image.load('image/enemy3_down4.png').convert_alpha(), \
            pygame.image.load('image/enemy3_down5.png').convert_alpha(), \
            pygame.image.load('image/enemy3_down6.png').convert_alpha() \
            ])
        self.alive = True
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = BigEnemy.hp
        self.hit = False
                        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.alive = True
        self.hp = BigEnemy.hp
        self.rect.left, self.rect.top = \
                        randint(0, self.width - self.rect.width), \
                        randint(-15 * self.height, -5 * self.height)