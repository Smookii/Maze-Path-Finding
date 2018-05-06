import cv2
import numpy as np
import sys
from skimage import io
from skimage import morphology
from lxml import etree


def ReadPositionFile(namefile):
    tree = etree.parse(namefile)
    root = tree.getroot()
    posDep = root.find('dep')
    depPoint = [int(posDep.get("x")), int(posDep.get("y"))]
    posEnd = root.find('end')
    endPoint = [int(posEnd.get("x")), int(posEnd.get("y"))]
    return depPoint, endPoint

#marquer départ et fin et noter que deadEnd du skel le plus proch est départ ou fin

img = cv2.imread(sys.argv[1],0)
_ , img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow("maze",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# size = np.size(img)
# skel = np.zeros(img.shape,np.uint8)
# ret,img = cv2.threshold(img,127,255,0)
# element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
# done = False


# cv2.imshow("test",image)
# cv2.waitKey(0)
oute = morphology.skeletonize(img > 0)
oute = oute.astype(np.uint8)
skel = oute
skel[skel>0] = 255


# while not done:
#     eroded = cv2.erode(img,element)
#     temp = cv2.dilate(eroded,element)
#     temp = cv2.subtract(img,temp)
#     skel = cv2.bitwise_or(skel,temp)
#     img = eroded.copy()
#
#     zeros = size - cv2.countNonZero(img)
#     if zeros==size:
#         done = True

cv2.imshow("skel",skel)
cv2.imwrite('skel.png',skel)
cv2.waitKey(0)
cv2.destroyAllWindows()

# met les contours en blanc pour garder la l'entrée du labyrinthe
# height, width = skel.shape[:2]
# skel[0:1,:]=255
# skel[:,0:1]=255
# skel[height-2:height-1][:]=255
# skel[:,width-2:width-1]=255

maze = np.copy(skel)
maze = cv2.cvtColor(maze, cv2.COLOR_GRAY2BGR)
around =  [0,0,1,1,1,-1,-1,-1]
around2 = [-1,1,1,0,-1,1,-1,0]
deadEnd = []
for x in range(0,skel.shape[0]):
    for y in range(0,skel.shape[1]):
        if skel[x][y] == 255:
            val = 0
            for i in range(0,len(around)):
                try:
                    if skel[x+around[i]][y+around2[i]] == 255:
                        val+=1
                except:
                    val = 4
            if val < 2:
                deadEnd.append((x,y))


depPoint, endPoint = ReadPositionFile('param.xml')
diffDep = 8000000
diffEnd = 8000000
dp = None
ep = None
for tp in deadEnd:
    if abs(tp[0]-depPoint[0])+abs(tp[1]-depPoint[1])<diffDep:
        diffDep = abs(tp[0]-depPoint[0])+abs(tp[1]-depPoint[1])
        dp = tp
        #print(f"start : { abs(tp[0]-depPoint[0])+abs(tp[1]-depPoint[1])}")
        #print(f"tp[0]:{tp[0]} tp[1]:{tp[1]}||depPoint[0]:{depPoint[0]} depPoint[1]:{depPoint[1]}")
        #print("dp",dp)
    if abs(tp[0]-endPoint[0])+abs(tp[1]-endPoint[1])<diffEnd:
        diffEnd = abs(tp[0]-endPoint[0])+abs(tp[1]-endPoint[1])
        ep = tp
        #print(f"start : { abs(tp[0]-endPoint[0])+abs(tp[1]-endPoint[1])}")
        #print(f"tp[0]:{tp[0]} tp[1]:{tp[1]}||endPoint[0]:{endPoint[0]} endPoint[1]:{endPoint[1]}")
        #print("ep",ep)
maze[dp[0]][dp[1]] = [0,0,255]
maze[ep[0]][ep[1]] = [255,0,0]
deadEnd.remove(dp)
deadEnd.remove(ep)

cv2.imshow("start End",maze)
cv2.waitKey(0)
cv2.destroyAllWindows()

for tp in deadEnd:
    # partir des dead end et supprimer iterativement les pixels avec un seul pixel connetcé
    x=tp[0]
    y=tp[1]
    maze[x][y] = [0,0,0]
    val = 0

    while val != -1 :
        val = 0
        xoffset = 0
        yoffset = 0
        for j in range(0,len(around)):
            try:
                if maze[x+around[j]][y+around2[j]][0] == 255:
                    xoffset = around[j]
                    yoffset = around2[j]
                    val += 1
            except:
                    val = 4
        if val == 1 :
            maze[x][y] = [0,0,0]
            x = x+xoffset
            y = y+yoffset
        else:
            maze[x][y] = [0,0,0]
            val = -1

cv2.imshow("rmDead",maze)
cv2.waitKey(0)
cv2.destroyAllWindows()
