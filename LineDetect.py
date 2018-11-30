import numpy as np
import cv2
import os
import shutil


#TODO:for challenge vid yellow on light road not detected well, maybe reduce amount threshold for Canny so it can detect less contrast?
#TODO:Use more segments to make up each line to fit curves more accurately?
#(sort all the points found for the left line then draw a bunch of lines connecteing each point to the next) and same for right?
#TODO:maybe play around with some Canny and HoughLinesP arguments like min_line_length and max_line_gap some more

def detectLines(img):
    '''This function accepts an image containing lane lines and returns that image with the lane lines marked'''
    #convert to greyscale
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #apply gaussian blur(only odd kernelSizes)
    grayBlur=cv2.GaussianBlur(grayImg,(5,5),0)

    #run canny algorithm on greyscale img(it also does gaussian blur)
    edges=cv2.Canny(grayBlur,50,125)

    #create image with only masked section of edges to run hough on
    mask=np.zeros_like(edges)

    #fillpoly makes maskimg all white(3rd argument) in are definded with vertices(2nd argument)
    cv2.fillPoly(mask,np.array([[(0,img.shape[0]),(12*img.shape[1]/25,3*img.shape[0]/5),(52.5*img.shape[1]/100,3*img.shape[0]/5),(img.shape[1],img.shape[0])]],dtype=np.int32),255)
    maskedEdges=cv2.bitwise_and(edges,mask)

    #get lines using houghTransformation on maskedEdges img cv2.HoughLinesP(image,rhoRes,angleRes,threshold,np.array([]),min_line_length,max_line_gap)
    lines=cv2.HoughLinesP(maskedEdges,2,np.pi/180,15,np.array([]),30,20)

    #create image to mark lines on
    lineImg=np.copy(img)

    #get 2 points for each line to draw
    #these will store points from lines closest to camera and furthest from camera for each lane line(initilize them to points that will be overwritten)
    rLEnd=[-1,img.shape[0]+1]#off bottom of screen
    rLStart=[-1,-1]#off top of screen
    lLEnd=[-1,img.shape[0]+1]#off bottom of screen
    lLStart=[-1,-1]#off top of screen

    for line in lines:
        for x1,y1,x2,y2 in line:
            #check if points should be a new endpoint for right or left lines and which end
            slope=(y2-y1)/(x2-x1)#TODO:got divide by 0 error once(didn't crash though)
            if (slope<-.2)and(x1<img.shape[1]/2):#left line segments
                if y1<y2:
                    if y1<lLEnd[1]:
                        lLEnd=[x1,y1]
                    if y2>lLStart[1]:
                        lLStart=[x2,y2]
                else: #y2<y1 or y2==y1 (shouldn't happen since line's slope is not 0)
                    if y2<lLEnd[1]:
                        lLEnd=[x2,y2]
                    if y1>lLStart[1]:
                        lLStart=[x1,y1]
            if (slope>.2)and(x1>img.shape[1]/2):#right line segments
                if y1<y2:
                    if y1<rLEnd[1]:
                        rLEnd=[x1,y1]
                    if y2>rLStart[1]:
                        rLStart=[x2,y2]
                else: #y2<y1 or y2==y1(which shouldn't happen since line's slope is not 0)
                    if y2<rLEnd[1]:
                        rLEnd=[x2,y2]
                    if y1>rLStart[1]:
                        rLStart=[x1,y1]

    #calculate slope and intercept for lines(using endpoints) then draw lines using points y=top of region and y=bottom of region
    leftSlope=(lLEnd[1]-lLStart[1])/(lLEnd[0]-lLStart[0])
    rightSlope=(rLEnd[1]-rLStart[1])/(rLEnd[0]-rLStart[0])
    leftInter=lLStart[1]-(lLStart[0]*leftSlope)
    rightInter=rLStart[1]-(rLStart[0]*rightSlope)
    #y=mx+b so x=(y-b)/m

    #middle line(for testing purposes and make it clearer what is going on)
    cv2.line(lineImg,(int(img.shape[1]/2),img.shape[0]),(int(img.shape[1]/2),0),(0,0,255),2)

    #extrapolate the line at y=img.shape[0] and y=3*img.shape[0]/5
    cv2.line(lineImg,(int((img.shape[0]-leftInter)/leftSlope),img.shape[0]),(int((3*img.shape[0]/5-leftInter)/leftSlope),int(3*img.shape[0]/5)),(0,255,0),2)#left line
    cv2.line(lineImg,(int((img.shape[0]-rightInter)/rightSlope),img.shape[0]),(int((3*img.shape[0]/5-rightInter)/rightSlope),int(3*img.shape[0]/5)),(255,0,0),2)#right line
    return lineImg

def imgDir(dir):
    '''dir is path to directory where all the images(and only the images) are stored
    images can be any format, and results are outputed same type as input
    '''
    #load filenames of all the images want to detectLines in and create output folder
    filenames=os.listdir(dir)
    if os.path.exists(dir+'_output'):
        shutil.rmtree(dir+'_output')
    os.mkdir(os.path.join(os.getcwd(),dir+'_output'))

    for img in filenames:
        absImgPath=os.path.join(os.getcwd(),dir,img)
        outImg=detectLines(cv2.imread(absImgPath))#read in the image and detect lane lines
        cv2.imwrite(dir+'_output/'+img,outImg)#save image with lane lines to output directory
        cv2.imshow(img,outImg)#show image with lane lines to screen
        while True:
            if cv2.waitKey(1) & 0xFF==ord('q'):#when they hit 'q' close the image on screen and move to next one
                break
        cv2.destroyAllWindows()

imgDir('test_images')#test the function imgDir on the test_images directory

def videoDir(dir):
    '''dir is path to directory containing multiple videos to process,
    vid can be any format(that your computer has the proper codecs for)
    this will output whatever video type vid is'''
    #load filenames of all the videos want to detectLines in and create output folder
    filenames=os.listdir(dir)
    if os.path.exists(dir+'_output'):
        shutil.rmtree(dir+'_output')
    os.mkdir(os.path.join(os.getcwd(),dir+'_output'))

    for vid in filenames:
        absVidPath=os.path.join(os.getcwd(),dir,vid)
        cap=cv2.VideoCapture(absVidPath)

        #create VideoWriter object to create video file with same metadata as vid and put it into the output directory
        absOutVidPath=os.path.join(os.getcwd(),dir+'_output',vid)
        out=cv2.VideoWriter(absOutVidPath,int(cap.get(cv2.CAP_PROP_FOURCC)),cap.get(cv2.CAP_PROP_FPS),(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        while(cap.isOpened()):#while vid still playing
            ret,frame=cap.read()
            if ret==True:
                outFrame=detectLines(frame)#detect lane lines in the frame
                out.write(outFrame)#write frame with lane lines drawn on to output video
                cv2.imshow(vid,outFrame)#show fram with lane lines to screen
                if cv2.waitKey(1) & 0xFF==ord('q'):#stop processing this video when user hits 'q'
                    break
            else:
                break
        #once done close streams
        cap.release()
        out.release()
        #close window playing video
        cv2.destroyAllWindows()

videoDir('test_videos')#test videoDir on the test_videos directory
