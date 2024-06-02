from drawBot import *
import csv


def extractData(glyphSet, fontInfo, flag=1):
    data = []

    for letter in glyphSet:
       
        font(fontInfo[0],fontSize=1000)
        #This is the width of the glyph including sidebearings, assuming a em size of 1000 units
        widthBearing = int(textSize(letter)[0])
        #This should be 1000, but isn't always
        heightBearing = int(textSize(letter)[1])

        #create a bezier curve of the letter with no sidebearings
        currentLetter = BezierPath() 
        currentLetter.text(letter, font=fontInfo[0], fontSize=1000) 

        #This returns the width and height of the shape with no sidebearings and the total area. Area = 1 is a solid em-square 1000 units by 1000 units. If the flag is not 1, it skips the area calculation.
        letterSizeData = letterSize(currentLetter, fontInfo[0], flag)            
        
        #Number of on curve points, no duplicates
        onCurvePoints = len(set(currentLetter.onCurvePoints )) 
        #Total number points, duplicates are allowed for off curve points, probably not likely
        totalPoints = len(currentLetter.offCurvePoints) + onCurvePoints
          
        #Put everything together     
        data.append(fontInfo + [letter, widthBearing, heightBearing, letterSizeData[0], letterSizeData[1], letterSizeData[2], onCurvePoints, totalPoints] )
        
    #Write a logfile of font names        
    log = open('./Log/log.txt','a')
    log.write(fontInfo[0]+'\n')
    log.close()
        
    return data




def letterSize(currentLetter, fontName, flag):
    #Bounds of the shape with no sidebearings
    (xmin, ymin,xmax, ymax) = currentLetter.bounds() 
    shapeWidth = xmax-xmin #width of bounding box
    shapeHeight = ymax-ymin #height of bounding box
    currentLetter.translate(-xmin,-ymin) #Move bounding box of shape to the origin
    
    if flag ==1:
        newPage(width = shapeWidth, height = shapeHeight)    #draw a new page that just fits the letter
        font(fontName, fontSize=1000)
        drawPath(currentLetter) #draw the letter in the page
        saveImage('./Log/temp.tif') #save as a tif
        letterGray = ImageObject('./Log/temp.tif') #load the tif
        letterGray.areaAverage((0, 0, shapeWidth, shapeHeight)) #find the average color to calculate area
        shapeArea = imagePixelColor(letterGray,(0, 0))[3] * shapeWidth * shapeHeight / 1000000 #Area =1 is a full em square
    
    else:
        shapeArea=0 #may want to skip area calculation, which is slow
    
    newDrawing() #refresh the output window
    return [int(shapeWidth), int(shapeHeight), shapeArea]
