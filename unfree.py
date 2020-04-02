import random
import os
import time
import keyboard
from tkinter import *
from PIL import *
from PIL import Image, ImageTk

class BlockType:
    def __init__(self,pilimage,pilimagetkphotoimage,typename):
        self.i=pilimage
        self.r=pilimagetkphotoimage
        self.n=typename
        (self.w, self.h)=pilimage.size
class Womap:
    def __init__(self,blocktypelist,numberofrows,numberofcolumns,mapstring=""):
        if mapstring=="":
            mapstring=blocktypelist[0].n*numberofrows*numberofcolumns
            r1=random.randint(0,numberofrows*numberofcolumns-1)
            mapstring=mapstring[:r1]+blocktypelist[1].n+mapstring[r1+1:]
            r2=random.randint(0,numberofrows*numberofcolumns-1)
            while r2==r1:
                r2=random.randint(0,numberofrows*numberofcolumns-1)
            mapstring=mapstring[:r2]+blocktypelist[2].n+mapstring[r2+1:]
            self.s=mapstring
        else:
            self.s=mapstring
        #
        self.b=blocktypelist
        self.m=numberofrows
        self.n=numberofcolumns
class Block:
    def __init__(self,canvas,x,y,blocktype):
        self.c=canvas
        self.x=x
        self.y=y
        self.b=blocktype
        self.s=canvas.create_image(x,y,image=blocktype.r)
    def setBlockType(self,blocktype):
        self.c.itemconfig(self.s,image=blocktype.r)
        self.b=blocktype
class Field:
    def __init__(self,tkroot,womap):
        tkroot.geometry(str(womap.m*womap.b[0].w)+"x"+str(womap.n*womap.b[0].h))
        tkcanvas=Canvas(tkroot,width=womap.m*womap.b[0].w,height=womap.n*womap.b[0].h)
        blocklist=[]
        i=0
        x=0
        y=0
        while i<womap.m*womap.n:
            j=0
            while womap.s[i]!=womap.b[j].n:
                j+=1
            #
            if i==0:
                x+=womap.b[j].w/2
                y+=womap.b[j].h/2
            elif i%womap.n==0:
                x-=(womap.n-1)*womap.b[j].w
                y+=womap.b[j].h
            else:
                x+=womap.b[j].w
            #
            blocklist.append(Block(tkcanvas,x,y,womap.b[j]))
            i+=1
        #
        self.b=blocklist
        self.r=tkroot
        self.c=tkcanvas
        self.m=womap
        tkcanvas.pack()
    def getBlockIDByType(self,blocktype):
        blockids=[]
        i=0
        while i<len(self.b):
            if self.b[i].b.n==blocktype.n:
                blockids.append(i)
            i+=1
        return blockids
    def getBlockIDAtRight(self,blockid):
        b=blockid
        m=self.m.m
        n=self.m.n
        b=b+1-n if (b+1)%n==0 else b+1
        return b
    def getBlockIDAtLeft(self,blockid):
        b=blockid
        m=self.m.m
        n=self.m.n
        b=b-1+n if b%n==0 else b-1
        return b
    def getBlockIDAtUp(self,blockid):
        b=blockid
        m=self.m.m
        n=self.m.n
        b=b+((m-1)*n) if b-n<0 else b-n
        return b
    def getBlockIDAtDown(self,blockid):
        b=blockid
        m=self.m.m
        n=self.m.n
        b=b-((m-1)*n) if b+n>=m*n else b+n
        return b
    def makeStep(self,srcid,dstid):
        self.b[srcid].setBlockType(blts[0])
        if self.b[dstid].b.n==blts[2].n:
            r=random.randint(0,self.m.m*self.m.n-1)
            while r==dstid:
                r=random.randint(0,self.m.m*self.m.n-1)
            self.b[r].setBlockType(blts[2])
        self.b[dstid].setBlockType(blts[1])
#
root = Tk()
pils=[]
imas=[]
blts=[]
dirpat="."
dirlis=os.listdir(path=dirpat)
dirlis.sort()
i=0
j=0
while i<len(dirlis):
    if dirlis[i][-4:]==".png":
        pils.append(Image.open(dirlis[i]))
        imas.append(ImageTk.PhotoImage(pils[j]))
        blts.append(BlockType(pils[j],imas[j],dirlis[i][:-4]))
        j+=1
    i+=1
#
womap=Womap(blts,7,7)
field=Field(root,womap)
#
def stepright():
    srcid=field.getBlockIDByType(blts[1])[0]
    dstid=field.getBlockIDAtRight(srcid)
    field.makeStep(srcid,dstid)
def stepleft():
    srcid=field.getBlockIDByType(blts[1])[0]
    dstid=field.getBlockIDAtLeft(srcid)
    field.makeStep(srcid,dstid)
def stepup():
    srcid=field.getBlockIDByType(blts[1])[0]
    dstid=field.getBlockIDAtUp(srcid)
    field.makeStep(srcid,dstid)
def stepdown():
    srcid=field.getBlockIDByType(blts[1])[0]
    dstid=field.getBlockIDAtDown(srcid)
    field.makeStep(srcid,dstid)
keyboard.add_hotkey("right arrow",stepright)
keyboard.add_hotkey("left arrow",stepleft)
keyboard.add_hotkey("up arrow",stepup)
keyboard.add_hotkey("down arrow",stepdown)
#
root.mainloop()
#
'''
while True:
    time.sleep(1)
    if keyboard.is_pressed("h"):
        field.getBlocksByType(blts[1])[0].setBlockType(blts[2])
'''
'''
while True:
    time.sleep(1)
    #down = j
    #left = s
    #right = l
    #up = f
    if keyboard.is_pressed("s+l+f"):
        print("down")
    elif keyboard.is_pressed("j+l+f"):
        print("left")
    elif keyboard.is_pressed("j+s+f"):
        print("right")
    elif keyboard.is_pressed("j+s+l"):
        print("up")
    if keyboard.is_pressed("enter"):
        print("\n",end="")
    if keyboard.is_pressed("q"):
        break;
'''
