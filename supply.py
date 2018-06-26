#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue March 6 14:31:20 2018

@author: keruiliu
"""
import pygame
import random

class BulletSupply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/ufo1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.bottom = \
                    random.randint(0,self.width-self.rect.width - 5), -100
        self.speed = 4
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        
    
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    
    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
                    random.randint(0,self.width-self.rect.width - 5), -100


class BombSupply(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/ufo2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.bottom = \
                    random.randint(0,self.width-self.rect.width - 5), -100
        self.speed = 4
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        
    
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    
    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
                    random.randint(0,self.width-self.rect.width - 5), -100
        
                    