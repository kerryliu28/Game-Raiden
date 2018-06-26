#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon March 5 20:24:52 2018

@author: keruiliu
"""

import pygame

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/hero1.png').convert_alpha()
        self.image1 = pygame.image.load('image/hero2.png').convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load('image/hero_blowup_n1.png').convert_alpha(), \
            pygame.image.load('image/hero_blowup_n2.png').convert_alpha(), \
            pygame.image.load('image/hero_blowup_n3.png').convert_alpha(), \
            pygame.image.load('image/hero_blowup_n4.png').convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0],bg_size[1]
        # Initially, the jet should be in the bottom center of the screen
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width)//2, \
                        self.height- self.rect.height - 60
        self.speed = 10
        self.alive = True
        self.mask = pygame.mask.from_surface(self.image)
        # After colliding with an enemy, give 2 seconds invincible period
        self.invincible = False

    def resurrect(self):
        self.alive = True
        self.invincible = True

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
    
    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60
    
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width
            
         
            
            
            
            