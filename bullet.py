#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon March 5 22:00:09 2018

@author: keruiliu
"""

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 13
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.rect.top -= self.speed
        # Bullet can't move beyond the screen
        if self.rect.top < 0:
            self.active = False
        
    def reset(self,position):
        self.rect.left, self.rect.top = position
        self.active = True


class DoubleBullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 20
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self):
        self.rect.top -= self.speed
        # Bullet can't move beyond the screen
        if self.rect.top < 0:
            self.active = False
        
    def reset(self,position):
        self.rect.left, self.rect.top = position
        self.active = True