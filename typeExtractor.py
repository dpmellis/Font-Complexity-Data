from drawBot import *
import csv
import AppKit
import time
import cmath
import math
import operator
import typeDataUtilities 

def extractData(glyphSet, fontInfo, flag=1):
    data = []

    for letter in glyphSet:
       
        font(fontInfo[0],fontSize=1000)
        #This is the width of the glyph including sidebearings, assuming a em size of 1000 units
        widthBearing = int(textSize(letter)[0])
        #This should be 1000, but isn't always
        heightBearing = int(textSize(letter)[1])

        
        #This returns the width and height of the shape with no sidebearings, and the number of on curve and offcurve points
        letterSizeData = letterSize(letter, fontInfo[0])            
        
        #This returns the total area of the glyph. Area = 1 is a solid em-square 1000 units by 1000 units. If the flag is not 1, it skips the area calculation and returns 0.
        letterAreaData = letterArea(letter, fontInfo[0], flag, 200)
    
       #Put everything together     
        data.append(fontInfo + [letter, widthBearing, heightBearing] + letterAreaData + letterSizeData )
        
    #Write a logfile of font names        
    log = open('./Log/log.txt','a')
    log.write(fontInfo[0]+' '+time.asctime() + '\n')
    log.close()
        
    return data

def letterArea(letter, fontName, flag, resolution=200):

    if flag == 1:
        letterGray = ImageObject()
        pool = AppKit.NSAutoreleasePool.alloc().init()
        try:
            ... # use code that creates autoreleased objects
            with letterGray:
                #create a bezier curve of the letter with no sidebearings
                currentLetter = BezierPath() 
                currentLetter.text(letter, font=fontName, fontSize=resolution) 

                #Bounds of the shape with no sidebearings
                (xmin, ymin,xmax, ymax) = currentLetter.bounds() 
                shapeWidth = xmax-xmin #width of bounding box
                shapeHeight = ymax-ymin #height of bounding box
    
                size(width = shapeWidth, height = shapeHeight)    #draw a new page that just fits the letter
                currentLetter.translate(-xmin,-ymin) #Move bounding box of shape to the origin
                drawPath(currentLetter) #draw the letter in the page
            letterGray.areaAverage((0, 0, shapeWidth, shapeHeight)) #find the average color to calculate area
            shapeArea = imagePixelColor(letterGray,(0, 0))[3] * shapeWidth * shapeHeight / resolution**2 #Area =1 is a full em square

        finally:
            del pool
        
        
    else:
        shapeArea=0 #may want to skip area calculation, which is slow

    newDrawing() #refresh the output window
    endDrawing()
    return [shapeArea]

def letterSize(letter, fontName):
    #create a bezier curve of the letter with no sidebearings
    currentLetter = BezierPath() 
    currentLetter.text(letter, font=fontName, fontSize=1000) 

    #Bounds of the shape with no sidebearings
    (xmin, ymin,xmax, ymax) = currentLetter.bounds() 
    shapeWidth = xmax-xmin #width of bounding box
    shapeHeight = ymax-ymin #height of bounding box
        
    #Number of on curve points, no duplicates
    onCurvePoints = len(set(currentLetter.onCurvePoints )) 
    #Total number points, duplicates are allowed for off curve points, probably not likely
    totalPoints = len(currentLetter.offCurvePoints) + onCurvePoints
    
    nonExtremaPoints = nonExtrema(currentLetter, tolerance=4)
          
    return [int(shapeWidth), int(shapeHeight), onCurvePoints, totalPoints, nonExtremaPoints]
    
    
def nonExtrema(currentLetter, tolerance = 1, verbose = False):
    nonExtremaCounter = 0
    for contour in currentLetter:
        index1 = list(range(1,len(contour) ) ) #The 0th element in contour is always a single point, the next element is either another point or a bezier curve connecting them
        #We want to compare the last handles of the current arc with the first handle of the next one. the last arc gets compared with the arc defined by contour[1]
        index2 = list(range(2,len(contour) ) )
        index2.append(1)

        for i, j in zip(index1, index2):
            
            if j==1 and len(contour[i])==3: #At the last point, we need to make sure the point at contour[i][3] is the same as contour[0][0]
                if contour[0][0] != contour[i][2]:
                    continue
                
            
            if len(contour[i])==3 and len(contour[j])==3: 
#if the current arc has 3 sets of coordinates and the next arc also has three sets of coordinates then there are two handles coming out of the point at contour[i+1], so we want to see if they are parallel and not vertical or horizontal
                handle1 = tuple(map(operator.sub,  contour[i][2], contour[i][1])) #subtract the handle from the point

                handle2 = tuple(map(operator.sub,  contour[j][0], contour[i][2]))#subtract the point from the next handle
                
                handleAngle1 = cmath.phase( complex(*handle1) )
                handleAngle2 = cmath.phase( complex(*handle2) )
            
                #Only want to care about points where the handles are parallel, need to have a tolerance in here because of the em grid of type design. We can have the abs_tol = 1° or .017 radians
                if angleChecker(handleAngle1,handleAngle2, tolerance):
                    nonExtremaCounter += 1
                    
                    if verbose:
                        print('angle1 = ',handleAngle1*180/math.pi )
                        print('angle2 = ',handleAngle2*180/math.pi )
                        print('point is', contour[i][2])
                        print('difference = ', abs(handleAngle2*180/math.pi-handleAngle1*180/math.pi), '\n')
                        fill(1,.5,0)
                        oval(contour[i][2][0]-5,contour[i][2][1]-5, 10, 10)
                    
        if verbose:
            print('###')           
    return nonExtremaCounter
                

def angleChecker(angle1,angle2, tolerance):
    tolerance = tolerance *math.pi/180 #Want to be able to put in degree tolerances
    badAngles = [0, math.pi/2, math.pi, -math.pi, -math.pi/2] #we don't want to count handles pointing in any of these directions
    for angle in badAngles:
        if math.isclose(angle1,angle,abs_tol=tolerance):
            return False
            
    if math.isclose(angle1, angle2, abs_tol=tolerance):
        return True #if the handles are close, it counts as an off Extrema smooth point, don't have to worry about -180°≈180° since we don't care about those angles anyway
    else:
        return False #if the handles aren't close, then it isn't a smooth point
    