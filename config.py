import pygame as pg
import time
import random

pg.init()

# colours
blue = (43, 192, 255)
green = (31, 156, 64)
red = (255, 0, 0)
translucent = (13, 68, 28)

# window dimensions
win_width = 1080
win_height = 850

# coordinates of players
x = 500
y = 820
dx = 0
dy = 0

# player wise score
score = [0, 0]

# time elapsed
time = 0
player_no = 1
level = 0
speed = 10

# [y, score]
y_score_1 = [[720, 10], [670,20], [560, 30], [550, 40], [430, 50], [400, 60], [310, 70], [240, 80], [190, 100], [80, 110]]
y_score_2 = [[80, 10], [190, 20], [240, 40], [310, 50], [400, 60], [430, 70], [550, 80], [560, 90], [670, 100], [720, 110]]


# the array containing the info about the moving obstacles
xArr = [100, 400, 248, 906, 641, 739]
yArr = [190, 190, 310, 430, 550, 670]


# all the images are a copyright of Mario Bros