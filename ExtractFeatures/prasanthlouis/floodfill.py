from PIL import Image
from operator import itemgetter
import os
import shutil
import sys

sys.setrecursionlimit(10000)
finalx=0
finaly=0
highy=999
lowy=0

def floodfill(x, y, oldColor, newColor):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.

	pix=im2.getpixel((y,x))
	if (pix!= oldColor):
		global finalx
		global highy
		global lowy
		finalx=y
		if(x>lowy):
			lowy=x
		if(x<highy):
			highy=x
		global finaly
		finaly=x
		return
	im2.putpixel((y,x),newColor)

	try:
		floodfill(x + 1, y, oldColor, newColor) # right
		floodfill(x - 1, y, oldColor, newColor) # left
		floodfill(x, y + 1, oldColor, newColor) # down
		floodfill(x, y - 1, oldColor, newColor)
	except:
		return
	
flag=0	
xcord=0
ycord=0
xcount=0
# im2=Image.open("output1.gif")
# for y in range(im2.size[0]):
	# if flag==1:
		# floodfill(xcord,ycord,0,10)
		# flag=0
		# im2.putpixel((y,finalx),80)
		# im2.save("exp"+str(xcount)+".gif")
		# xcount=xcount+1
		# bbox = (y, 0,fycord+finaly, im2.size[1])
		
		# working_slice = im2.crop(bbox)
		# working_slice.save("lala"+str(xcount)+".gif")
		# break
	# for x in range(im2.size[1]):
		# pix = im2.getpixel((y,x))
		# if pix!=255:
			# xcord=x
			# ycord=y
			# fxcord=y
			# fycord=x
			# flag=1
			# break
		# else:
			# im2.putpixel((y,x),80)
	
		
			
			
fxcord=0
fycord=0
checky=0			
im2=Image.open("output1.gif")
for y in range(finaly,im2.size[0]):
	if flag==1:
		floodfill(xcord,ycord,0,10)
		flag=0
		im2.save("exp"+str(xcount)+".gif")
		
		#print finalx
		#print finaly
		xcount=xcount+1
		flag=0
	for x in range(0,im2.size[1]):
		pix = im2.getpixel((y,x))
		if pix!=255 and pix!=10:
			fxcord=x
			fycord=y
			if checky==1:
				ffxcord=fxcord-xcord
				ffycord=fycord-ycord
				bbox = (ycord, highy,ycord+ffycord, lowy)
				print highy
				working_slice = im2.crop(bbox)
				working_slice.thumbnail((9,11),Image.ANTIALIAS)
				working_slice.save("lala"+str(xcount)+".gif",quality=95)
				highy=999
				lowy=0
			xcord=x
			ycord=y
			checky=1
			flag=1
			break
			
bbox = (ycord, highy,ycord+ffycord, lowy)
			
working_slice = im2.crop(bbox)
working_slice.thumbnail((9,11),Image.ANTIALIAS)
working_slice.save("lala"+str(xcount)+".gif",quality=95)
		
		
			
			
	
			



