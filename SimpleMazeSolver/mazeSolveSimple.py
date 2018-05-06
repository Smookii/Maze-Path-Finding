#coding=utf-8

import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],cv2.IMREAD_GRAYSCALE)

start = img.copy()

cv2.imshow('image',img)
cv2.waitKey()

# seuillage
_ , img = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# marquage des zones interconnectées
ret, labels = cv2.connectedComponents(img)

part1 = np.copy(labels)

part1[part1 != 1] = 0

#HSV
label_hue = np.uint8(179*part1/np.max(2))
blank_ch = 255*np.ones_like(label_hue)
part1_img = cv2.merge([label_hue, blank_ch, blank_ch])

# conversion pour affichage
part1_img = cv2.cvtColor(part1_img, cv2.COLOR_HSV2BGR)
part1_img = cv2.cvtColor(part1_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('part1', part1_img)
cv2.waitKey()

#dilatation
kernel = np.ones((7,7),np.uint8)
part1d = cv2.dilate(part1_img,kernel,iterations = 1)
part1e = cv2.erode(part1d,kernel,iterations = 1)
cv2.imshow('dilated', part1d)
cv2.waitKey()

#soustraction pour obtenir le chemin
path = part1d - part1e
cv2.imshow('path', path)
cv2.waitKey()

#convertion pour affichage
path = cv2.cvtColor(path, cv2.COLOR_GRAY2BGR)

# map des marquage avec une valeure de hue
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR pour affichage
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

# bacgkground en noir
labeled_img[label_hue==0] = 0

cv2.imshow('labeled', labeled_img)
cv2.waitKey()

# pour changer le gris le gris du chemin
# car [255, 255, 255] - [255, 255, 0] donne du rouge => start-path
path[np.where((path == [102,102,102]).all(axis = 2))] = [255,255,0]

#convertion pour affichage
start = cv2.cvtColor(start, cv2.COLOR_GRAY2BGR)

cv2.imshow('solution', start-path)
cv2.waitKey()
