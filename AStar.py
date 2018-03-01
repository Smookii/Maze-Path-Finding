import numpy as np
import cv2 as cv
import sys
import os
from lxml import etree

class Node:
    pos = []
    parent = ""
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent


def algoAround(array, start, goal, square=False, colorNuance=False, animation=[1, 1], distanceMax=2000, borderSize=1, delay = 0):
    height, width = array.shape[:2]

    pathFinder = np.zeros(shape=(height,width))

    vectors = [(0, -borderSize), (borderSize, 0), (0, borderSize), (-borderSize, 0)]
    if square == True:
        vectors = [(-borderSize, -borderSize), (0, -borderSize), (borderSize, -borderSize),
                   (borderSize, 0), (borderSize, borderSize), (0, borderSize),
                   (-borderSize, borderSize), (-borderSize, 0)]

    teint = 255
    if colorNuance:
        teint = 0.0
        teintcpt = 255/distanceMax


    tab = [start]
    distanceMin = 0
    reversePos = []
    delaycpt = 0
    icpt = 0
    blExit = False
    while blExit == False:
        newTab = []
        for pos in tab:
            for vect in vectors:
                newPos = [pos[0] + vect[0], pos[1] + vect[1]]
                if newPos[0] >= 0 and newPos[0] < width and newPos[1] >= 0 and newPos[1] < height:
                    diffx = abs(newPos[0] - endPoint[0])
                    diffy = abs(newPos[1] - endPoint[1])

                    if newPos == goal or (diffx <= borderSize and diffy <= borderSize):
                        blExit = True
                        pathFinder[newPos[1], newPos[0]] = icpt
                        distanceMin = icpt
                        reversePos = newPos
                        continue
                    if array[newPos[1], newPos[0]][2] > 200 and newPos not in newTab:
                        newTab.append(newPos)
                        array[newPos[1], newPos[0]] = [0,teint,0]
                        pathFinder[newPos[1], newPos[0]] = icpt

        if colorNuance:
            teint += teintcpt

        if animation[0] == 1 :
            if delaycpt >= delay:
                cv.imshow('Path', array)
                cv.waitKey(1)
                delaycpt = 0
            else:
                delaycpt += 1
        tab = newTab
        icpt += 1
        if icpt >= distanceMax:
            print("La distance max à été atteinte, réessayé en augmentant le DISTANCEMAX dans la partie config")
            blExit = True

    cv.imshow('Path', array)
    cv.waitKey()

    distanceMin -=1
    colorTrace = [0, 0, 255]
    oldPos = reversePos
    finalPath = []
    for i in range(0, distanceMin):
        reversePos = FindPos(vectors, distanceMin-i, reversePos, pathFinder)
        tabPosPix = []
        if borderSize == 1:
            tabPosPix = [reversePos]
        else:
            tabPosPix = TraceLineBeetweenPoints(oldPos, reversePos, borderSize)

        for pos in tabPosPix:
            array[pos[1], pos[0]] = colorTrace

        finalPath += tabPosPix

        oldPos = reversePos
        if animation[1] == 1:
            if delaycpt >= delay:
                cv.imshow('Path', array)
                cv.waitKey(1)
                delaycpt = 0
            else:
                delaycpt += 1
    cv.imshow('Path', array)
    cv.waitKey()
    return finalPath


def TraceLineBeetweenPoints(pos, reversePos, wallsize):
    tabPosPix = []
    vect = [0,0]
    for i in range(0,2):
        if pos[i] < reversePos[i]:
            vect[i] = 1
        elif pos[i] > reversePos[i]:
            vect[i] = -1
        else:
            vect[i] = 0
    for i in range(0, wallsize):
        newPos = [pos[0] + vect[0], pos[1] + vect[1]]
        tabPosPix.append(newPos)
        pos = newPos
    return tabPosPix


def FindPos(vectors, i, pos, pathFinder):
    for vect in vectors:
        newPos = [pos[0] + vect[0], pos[1] + vect[1]]
        if pathFinder[newPos[1], newPos[0]] == i:
            return newPos


def ReadPositionFile(namefile):
    tree = etree.parse(namefile)
    root = tree.getroot()
    posDep = root.find('dep')
    depPoint = [int(posDep.get("x")), int(posDep.get("y"))]
    posEnd = root.find('end')
    endPoint = [int(posEnd.get("x")), int(posEnd.get("y"))]
    return depPoint, endPoint


def FindDepEnd(array, colordep, colorend):
    print("Détection automatique du point de départ et d'arrivé")
    depfind = False
    endfind = False
    depPos = None
    endPos = None
    height, width = array.shape[:2]
    for i in range(0, height):
        for j in range(0, width):
            pixel = array[i, j]
            if not depfind:
                if ComparePixelColor(pixel, colordep):
                    depPos = [j,i]
                    depfind = True
            if not endfind:
                if ComparePixelColor(pixel, colorend):
                    endPos = [j,i]
                    endfind = True
            if depfind and endfind:
                continue
    if not depfind or not endfind:
        return [-1,-1], [-1,-1]
    return depPos, endPos


def ComparePixelColor(l1, l2):
    if len(l1) is not len(l2[1]):
        return False
    for i in range(0, len(l1)):
        if i is l2[0]:
            if l1[i] < l2[1][l2[0]]:
                return False
        else:
            if l1[i] > l2[1][i]:
                return False
    return True


###### CONFIG ######
SQUAREFIND = False
COLORTEINT = True
ANIMATION = [1, 1]
ANIMATIONDELAY = 35
DISTANCEMAX = 20000
BORDERSIZE = 1
COLORDEP = (2, [100,100,250])
COLOREND = (1, [100,250,100])


depPoint = []
endPoint = []
closeProgram = False

if len(sys.argv) > 2:
    depPoint, endPoint = ReadXmlFile(sys.argv[2])
    img = cv.imread(sys.argv[1], cv.IMREAD_ANYCOLOR)
elif len(sys.argv) > 1:
    img = cv.imread(sys.argv[1], cv.IMREAD_ANYCOLOR)
    depPoint, endPoint = FindDepEnd(img, COLORDEP, COLOREND)
    if depPoint[0] < 0 or depPoint[1] < 0 or endPoint[0] < 0 or endPoint[1] < 0:
        closeProgram = True
else:
    depPoint, endPoint = ReadXmlFile('maze.xml')
    img = cv.imread('maze.png', cv.IMREAD_ANYCOLOR)
imgDev = img.copy()

if closeProgram:
    print("Erreur point de départ ou d'arrivé manquant, vérifié qu'au moins un pixel de l'image corresponds à COLORDEP et un autre à  COLOREND, ou précisé les positions dans un fichier xml")
else:
    cv.imshow('Path', imgDev)
    cv.waitKey()
    finalPath = algoAround(imgDev, depPoint, endPoint, SQUAREFIND, COLORTEINT, ANIMATION, DISTANCEMAX,BORDERSIZE,ANIMATIONDELAY)
    imgFinal = img.copy()
    for pos in finalPath:
        imgFinal[pos[1], pos[0]] = [0,0,255]
    cv.imshow('Path', imgFinal)
    cv.waitKey()
