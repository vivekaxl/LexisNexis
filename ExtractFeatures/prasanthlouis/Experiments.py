from PIL import Image
from operator import itemgetter
import os
import shutil
xcount=0;
for r in range(1,18):
	xcount=xcount+1;
		
	im = Image.open("captcha"+str(xcount)+".gif")
	im = im.convert("L")
	im2 = Image.new("L",im.size,255)
	imx = Image.new("L",im2.size,255)
	



	count = 0
	intens = {}

	im = im.convert("L")
	hm = im.histogram();
	values= {}
	for i in range(256):
	  values[i] = hm[i]


	temp = {}

	for x in range(im.size[1]):
	  for y in range(im.size[0]):
		pix = im.getpixel((y,x))
		temp[pix] = pix
		if pix in range(0,150) : # these are the numbers to get
		  im2.putpixel((y,x),0)

	im2.save("output"+str(xcount)+".gif")
	hm = im2.histogram();
	print xcount
	for i in range(256):
	  values[i] = hm[i]

	for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
		intens[count]=j
		count=count+1
	filter = {}


	if intens[0]==0:
		for x in range(im2.size[1]):
			for y in range(im2.size[0]):
				pix = im2.getpixel((y,x))
				filter[pix] = pix
				if pix==intens[1]:
					imx.putpixel((y,x),intens[0])
		imx.save("output"+str(xcount)+".gif")

	for l in range(0,1):
		im3 = Image.open("output"+str(xcount)+".gif")
		im3 = im3.convert("L")	
		im4 = Image.new("L",im3.size,255)
		for x in range(0,im3.size[1]):
			 for y in range(0,im3.size[0]):
				try:
					a=x+1
					b=y+1
					c=x-1
					d=y-1
					pix1=im3.getpixel((y,a))
					pix2=im3.getpixel((b,x))
					pix3=im3.getpixel((d,x))
					pix4=im3.getpixel((y,c))
					pix5=im3.getpixel((y,x))
					if (pix1==255 and pix2==255 and pix3==255 and pix4==255):
						im3.putpixel((y,x),255)
					if ( pix2==255 and pix3==255 and pix4==255):
						im3.putpixel((y,x),255)
					if (pix1==255  and pix3==255 and pix4==255):
						im3.putpixel((y,x),255)
					if (pix1==255 and pix2==255 and pix4==255):
						im3.putpixel((y,x),255)
					if (pix1==255 and pix2==255 and pix3==255):
						im3.putpixel((y,x),255)
					if (pix2==255 and pix3==255 and pix1==0 and pix4==0):
						im3.putpixel((y,x),255)
					if (pix1==255 and pix4==255 and pix2==0 and pix3==0):
						im3.putpixel((y,x),255)
				
				except:
						im3.putpixel((y,x),255)
						continue
					

					
			
	im3.save("output"+str(xcount)+".gif")
		
	bbox = (5, 5, 100, im3.size[1])
	working_slice = im3.crop(bbox)
	working_slice.save("outputcrop"+str(xcount)+".gif")
	destinationDir='C:\Users\Prasanth\Desktop\Main Project\crops'
	if not os.path.exists(destinationDir): 
		os.makedirs(destinationDir)
	shutil.move("outputcrop"+str(xcount)+".gif", destinationDir)
      #  working_slice.save(os.path.join(outdir, "slice.png"))

