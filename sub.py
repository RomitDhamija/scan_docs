import cv2
import os

def get_images(dir= 'data'):

	data= list()

	sets= os.listdir(dir)
	for set in sets:
		files= os.listdir(os.path.join(dir,set))
		for file in files:
			ext= file.split('.')[-1]
			if ext== 'jpg':

				data.append(os.path.join(dir, set,file))

	return data

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

def crop(img, p1, p2):

	x1, y1= p1
	x2, y2= p2
	crop= img[y1: y2, x1: x2, :]

	crop= cv2.resize(crop, (250, 250))
	return crop

if __name__ == '__main__':
	
	images= get_images()
	count= 0

	for file in images:

		output_path= 'output\\'+ file.split('\\')[-2]
		
		image = cv2.imread(file)

		r,g,b= image[0,0,0], image[0,0,1], image[0,0,2] #getting rgb values to create border

		ratio = image.shape[0] / 650.0 
		orig = image.copy()
		image = resize(image, height=650) #change the aspect ratio

		image= cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_CONSTANT,value=[72, 81, 71]) #creating border to detect edges
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		edged = cv2.Canny(gray, 75, 200)
		 
		print("Detecting Edges")

		cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[1]
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
		 
		#looping over all the contour values
		try:

			for c in cnts:
				peri = cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			 
				if len(approx) == 4:
					screenCnt = approx
					break
			 
			print("Finding Contours")

			p1, p2= screenCnt[3][0], screenCnt[1][0]
			cropped= crop(image, p1, p2)

			cv2.imwrite('output/'+str(count)+'.jpg', cropped)
			count+=1
		except:
			with open('no_crop.txt','a+') as f:
				f.write(file)
				f.write("\n")
			f.close()
			
	exit()