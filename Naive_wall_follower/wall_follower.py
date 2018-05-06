import cv2
import numpy as np
import sys

PATH = 255
WALL = 0
GREY = 128
DIRECTION = {
    'right' : (1, 0),
    'left' : (-1, 0),
    'up' : (0, -1),
    'down' : (0, 1)
    }
RELATIVERIGHT = {
    'right' : (1, 1),
    'left' : (-1, -1),
    'up' : (1, -1),
    'down' : (-1, 1)
}

def follow_wall(img):
    path = list()
    steps = 0
    x = 0
    y = 0
    d = ''
    x, y, d = find_start(img, d)
    print(find_start(img, d))
    while not out(img, x, y):
        steps = steps + 1
        newPos = step(img, x, y, d)
        if newPos is not None:
            x = newPos[0]
            y = newPos[1]
            d = newPos[2]
            path.append((x, y))
        else:
            print("exit found ! ", newPos)
            return path
        if out(img, x, y):
            print("exit found !")
            return path

def playback(path, img, speed, color):
    steps = 0
    backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    for i in range(len(path)):
        backtorgb[path[i][1]][path[i][0]] = color
        if steps % speed == 0:
            cv2.imshow('maze', backtorgb)
            cv2.waitKey(delay = 1)
        steps = steps + 1


def out(img, x, y):
    return x < 0 or x >= len(img[0]) or y < 0 or y >= len(img[1])

def step(img, x, y, direction):
    index_r = RELATIVERIGHT[direction]
    index = DIRECTION[direction]
    if not out(img, x + index_r[0], y + index_r[1]) and not out(img, x + index[0], y + index[1]):
        right_space = img[y + index_r[1]][x + index_r[0]]
        front_space = img[y + index[1]][x + index[0]]

        if right_space == WALL:
            if front_space != PATH:
                if direction == 'up':
                    direction = 'left'
                elif direction == 'left':
                    direction = 'down'
                elif direction == 'down':
                    direction = 'right'
                else:
                    direction = 'up'
        else:
            if direction == 'up':
                direction = 'right'
            elif direction == 'left':
                direction = 'up'
            elif direction == 'right':
                direction = 'down'
            else:
                direction = 'left'

        dx = DIRECTION[direction][0]
        dy = DIRECTION[direction][1]
        x = x + dx
        y = y + dy
        return x, y, direction

def printinfo(x, y, direction):
    print("x : {} | y : {} | direction : {}".format(x,y,direction))

def find_start(img, direction):
    ep = find_entry_point(img)
    return stick_to_the_goddamn_wall(img, ep)

def stick_to_the_goddamn_wall(img, ep):
    x = ep[0]
    while img[ep[1]][x+1] == 255:
        x += 1
    return (x, ep[1], ep[2])

def find_entry_point(img):
    #print(img[34] )
    width = len(img[0]) - 1
    height = len(img[1])  - 1
    for x in range(0, width):
        if (img[0][x] == PATH):
            direction = 'down'
            #print("found, 1")
            return (x, 0, direction)
        elif (img[width][x] == PATH):
            #print(x)
            #print(width)
            direction = 'up'
            print("found, 2")
            return (x, width, direction)

    for y in range(0, height):
        if (img[y][0] == PATH):
            direction = 'left'
            #print("found, 3")
            return (0, y, direction)
        elif (img[y][height] == PATH):
            direction = 'right'
            #print("found, 4")
            return (height, y, direction)
def main():
    if len(sys.argv) < 3 :
        print("Usage : \npython wall-follower.py <filename> <playback speed>\n python wall-follower.py auto")
    else:
	path = sys.argv[1]
	playback_speed = int(sys.argv[2])
	old_img = cv2.imread(path)
        img =  cv2.imread(path, 0)
	ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	cv2.imshow('original', old_img)
        cv2.waitKey()
        cv2.imshow('test', thresh)
	cv2.waitKey()
	path = follow_wall(thresh)
	print(len(path))
	playback(path, img, playback_speed, (255, 125, 0))

main()
