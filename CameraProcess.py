"""

CameraProcess takes photos and processes them to
determine next movement in mode2

"""
# Import to get picture stream
import io
# Import to pause to make sure picutre stream is initialized correctly
import time
# Import to grab photo from picamera
import picamera
import picamera.array
# Import openCV to process images
import cv2
# Import to analyze image as a matrix
import numpy as np
# Import config which holds the shared variables
import config

class cameraProcess:

    def takePhoto(self):
        #print('f1')
        # Create the in-memory stream
        stream = io.BytesIO()
        with picamera.PiCamera() as cam:
            #picamera mounted upsidown
            cam.vflip = True
            cam.hflip = True
            # Pause to make sure picutre stream is initialized correctly
            time.sleep(2)
            with picamera.array.PiRGBArray(cam) as stream:
                # Grab an image from the cam in BGR color arangement
                cam.capture(stream, format='bgr')
                # At this point the image is available as stream.array
                image = stream.array
        self.findCircles(image)
        
        
    def findCircles(self, cimg):
        #print('f2')
        # Blur and convert image to gray
        cimg = cv2.medianBlur(cimg, 5)
        image = cv2.cvtColor(cimg, cv2.COLOR_BGR2GRAY)

        #Finds all the circles in image and returns the (x, y) coordinates
            #and the circle radii in a [1 by number of circles found by 3]
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,1, 20, param1=50,param2=30, minRadius=0, maxRadius=80)
        #print('circles: {}'.format(circles))

        # number of cicles
        circlesLength = len(circles[0,:])
        #print('circlesLength: {}'.format(circlesLength))

        #Threshold dicates the allowed horizontal distance between points
            #that will be allowed in a accepted stoplight
        Threshold = 20
            

        if(circlesLength>4):
            # noStopLightFlag goes high if no flag is found to re-initiate search
            noStopLightFlag = 0
            # Initialize a array that keeps track of each points 2 closest radii
                #matches and the difference between them
                #single point example [dif1, dif2, dif1Index, dif2Index]
            storeDif=-1*np.ones([circlesLength, 4])
            # radii is an array of the circles radii sorted smallest to largest
            radii=np.sort(circles[0,:,2])
            # sortedRadiiIndex is an array that keeps track of the radii's
                #initial position in cicles
            sortedRadiiIndex = sorted(range(len(circles[0,:,2])), key=lambda k: circles[0,:,2][k])
            #print('sortedRadiiIndex: {}'.format(sortedRadiiIndex))
            #print('radii: {}'.format(radii))

            # This code groups the circle radii in groups of the 3. The 2 most 
                #similar radii to each circle are organized into storeDif.
                # It does this by comparing the radii of a particular circle
                # with that of the circles above and below it in size. Then the
                # worst match of those two is compared with the circle two steps
                # away from the inital circle in the other direction. The two
                # circles with minimum radii size difference from the initial radii
                # are stored in that radii's row of storeDif.
            for i in range(2,circlesLength-2):
                dif2 =radii[i]-radii[i-1]
                dif4 =radii[i+1]-radii[i]
                if(dif2<=dif4):
                    storeDif[i,0]= dif2
                    storeDif[i,2]= i-1
                    dif1 = radii[i]-radii[i-2]
                    if(dif1<=dif4):
                        storeDif[i,1]= dif1
                        storeDif[i,3]= i-2
                    else:
                        storeDif[i,1]= dif4
                        storeDif[i,3]= i+1
                else:
                    storeDif[i,0]= dif4
                    storeDif[i,2]= i+1
                    dif5 = radii[i+2]-radii[i]
                    if(dif2<=dif5):
                        storeDif[i,1]= dif2
                        storeDif[i,3]= i-1
                    else:
                        storeDif[i,1]= dif5
                        storeDif[i,3]= i+2

            #print('storeDif: {}'.format(storeDif))
            # Finds3 circles that have the minimum size difference
            # Also ignore the first 2 and last 2 storeDif rows,
            # since if the stop light they should be grouped in the 3rd row
            storeDifTotal = storeDif[:,0]+storeDif[:,1]
            storeDifTotal = storeDifTotal[2:]
            storeDifTotal = storeDifTotal[:(circlesLength-4)]
            minSet = storeDifTotal.argmin(axis = 0)

            # Select right row of store dif
            minSet = minSet+2
            #print('minSet: {}'.format(minSet))
            stopLight = np.zeros([3,1])

            # Find the indexies of the 3 circles that are most similar in size
            stopLight[0] = sortedRadiiIndex[minSet]
            stopLight[1] = sortedRadiiIndex[int(storeDif[minSet,2])]
            stopLight[2] = sortedRadiiIndex[int(storeDif[minSet,3])]
            #print('stopLight: {}'.format(stopLight))

            # Check to make sure that the 3 selected cicles are within the
                #horizontal threshold of a stoplight, otherwise set noStopLightFlag high            matchedCirc = -1*np.ones([3, 3])
            matchedCirc = -1*np.ones([3,3])
            for k in range(0,3):
                matchedCirc[k,:] = circles[0,stopLight[k,0],:]
            xs=np.sort(matchedCirc[:,0])
            storeXDif=-1*np.ones([2, 1])
            for i in range(0,2):
                storeXDif[i,0] =xs[i+1]-xs[i]
            if(Threshold<storeXDif[0,0]+storeXDif[1,0]):
                noStopLightFlag = 1

        # Occurs if only 4 circles are found the pairing technique needed to be slightly
            # altered in order to prevent indexing errors, so it works similarly
            # to with more than 5 cicles, but its comparisons are only are
            # applicable to when there is 4 circles (comments in last section
            # discribe particular actions)
        elif(circlesLength==4):
            noStopLightFlag = 0
            storeDif=-1*np.ones([3, 1])
            xCoord=np.sort(circles[0,:,0])
            sortedxCoordIndex = sorted(range(len(circles[0,:,0])), key=lambda k: circles[0,:,0][k])
            stopLight = np.zeros([3,1])
            for i in range(0,3):
                storeDif[i,0] =xCoord[i+1]-xCoord[i]
            if(storeDif[0,0]>=storeDif[2,0]):
                if(Threshold> storeDif[1,0]+storeDif[2,0]):
                    stopLight[0] = sortedxCoordIndex[1]
                    stopLight[1] = sortedxCoordIndex[2]
                    stopLight[2] = sortedxCoordIndex[3]
            else:
                if(Threshold> storeDif[0,0]+storeDif[1,0]):
                    stopLight[0] = sortedxCoordIndex[0]
                    stopLight[1] = sortedxCoordIndex[1]
                    stopLight[2] = sortedxCoordIndex[2]

        # If only 3 circles are found the pairing technique then if the
            # horizontal positions are within the acceptable threshold is
            # checked to ensure its a stoplight
        elif(circlesLength==3):
            noStopLightFlag = 0
            xCoord=np.sort(circles[0,:,0])
            storeXDif=-1*np.ones([2, 1])
            stopLight = np.zeros([3,1])
            for i in range(0,2):
                storeXDif[i,0] =xCoord[i+1]-xCoord[i]
            #print('xCoord: {}'.format(xCoord))
            if(Threshold> storeXDif[0,0]+storeXDif[1,0]):
                    stopLight[0] = 0
                    stopLight[1] = 1
                    stopLight[2] = 2

        #If less than two circles are found put no stop light flag high                   
        else:
            noStopLightFlag = 1

        # If a stoplight was found the color needs to be sorted
        if(noStopLightFlag==0):
            #FIND OUT COLOR
            selectedCirc = -1*np.ones([3, 3])
            for k in range(0,3):
                selectedCirc[k,:] = circles[0,stopLight[k,0],:]
            yCoord=np.sort(selectedCirc[:,1])
            #the mean is found to determin the horizontal position to check color
            xMean = np.mean(selectedCirc[k,0])
            config.Color=0#'POWER OUTAGE?????? :O'
            if(cimg[yCoord[0], xMean, 0]<75):
                config.Color=1#'RED'
            elif(cimg[yCoord[1], xMean, 0]<75):
                config.Color=2#'YELLOW'
            elif(cimg[yCoord[2], xMean, 2]<75):
                config.Color=3#'GREEN'

            print('Color: {}'.format(config.Color))
            
###1) uncomment to show stoplight circles and pause proces found by 1st run
##            circles = np.uint16(np.around(circles))
##            for i in range(0,3):
##                #draw the outer circle
##                #print('input2: {}'.format(stopLight))
##                cv2.circle(cimg, (circles[0,stopLight[i,0],0], circles[0,stopLight[i,0],1]), circles[0,stopLight[i,0],2], (0,255,0),2)
##                #draw the center of the circle
##                cv2.circle(cimg, (circles[0,stopLight[i,0],0], circles[0,stopLight[i,0],1]), 2, (0,0,255),3)
##            
##            cv2.imshow('detected circles',cimg)
##            cv2.waitKey(0)
##            cv2.destroyAllWindows()
###uncomment to here 1

#"else" region
        # If no stoplight was found loop and try again
        else:
            print('no light found')
            config.Color=-1
            self.takePhoto()
#end of "else" region
###2) uncomment to see all circles found by houghCircles and pause proces found by 1st run
##    #to do so you must also comment out the "else" above this region (when running code the
##    #"else" region must first be re-implemented)
##        circles = np.uint16(np.around(circles))
##            
##        for i in circles[0,:]:
##            #draw the outer circle
##            cv2.circle(cimg, (i[0], i[1]), i[2], (0,255,0),2)
##            #draw the center of the circle
##            cv2.circle(cimg, (i[0], i[1]), 2, (0,0,255),3)
##        
##        cv2.imshow('detected circles',cimg)
##        cv2.waitKey(0)
##        cv2.destroyAllWindows()
###uncomment to here 2  
                
      

if __name__== '__main__':
    c = cameraProcess()
    try:
        c.takePhoto()
##        c.findCircles()
    except KeyboardInterrupt:
        print('worked?')
