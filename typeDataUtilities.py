from drawBot import *
import csv







def pointPlot(listOfPoints, diameter=5): #given a list of tuples representing points, plot them and use color to indicate order
    colorGradient = 0 #color the first point black, change to red as it goes around the shape
    for (x,y) in listOfPoints:
        fill(colorGradient,0,0)
        oval(x-diameter/2,y-diameter/2,diameter,diameter)
        colorGradient += 1/(len(listOfPoints)-1)

    return None


def onCurvePoints(contourCurve): #given a contour of a curve, return all of the on curve points
    CurvePoints = []

    for segment in contourCurve:

        # If it is a curve, extract the on curve point
        if len(segment) == 3:
        
             x,y = segment[2][0], segment[2][1]        
             CurvePoints.append( (x,y ) )            

        # If it is a line, extract the point 

        if len(segment) == 1:
            x,y = segment[0][0], segment[0][1]
            CurvePoints.append( (x,y ) )     
    return CurvePoints     

def resizeForShape(shape, margin=20): #Resizes canvas to fit shape + a margin
    (xmin, ymin,xmax, ymax) = shape.bounds() #find the bounds of the glyph
    shape.translate(-xmin+margin,-ymin + margin) #Move the curve to the corner with margin
    (xmin, ymin,xmax, ymax) = shape.bounds() #Find new bounds
    size(xmax+margin,ymax+margin) #Remake the canvas size to fit the glyph with margin
    return None


def normalizeContourCorner(contour): #takes a Glyph Contour returns a Glyph Path where the first point has the smallest value of x + y, only for cubic beziers

    minXY = min( x+y for (x,y) in onCurvePoints(contour)  )  #Find the lowest x+y coordinate sum of all of the points
    minXYindex = [ x+y for (x,y) in onCurvePoints(contour) ].index(minXY) #use the sum to find the corresponding point Caution this will not distinguish between two points if they have the same value
    
    if [x+y for (x,y) in onCurvePoints(contour)].count(minXY)>1 & minXYindex != 0:
        print('Warning min x+y value is not unique')

    if contour[0][-1]==contour[-1][-1]: #Need to distinguish between open and closed contours
        flag = 1
    else:
        flag = 0 

    newContour = BezierPath() #initialize re-indexed path
    newContour.moveTo( contour[minXYindex][-1]  ) #start the new path at the minXYindex point

    for segment in contour[ (minXYindex+1):] : #start adding points from index point to the end
        if len(segment) == 1:
            newContour.lineTo(segment[0])
        else:
            newContour.curveTo( segment[0],segment[1], segment[2] )
        
    for segment in contour[flag:(minXYindex+1)]: #now start from the beginning, need to distinguish between contours where the first point is the same as the last, and those where that isn't true
        if len(segment) == 1:
            newContour.lineTo(segment[0])
        else:
            newContour.curveTo( segment[0],segment[1], segment[2] )
        
    newContour.endPath()                    
    return newContour

def normalizeGlyphCorner(glyph):
    newGlyph = BezierPath() #initialize re-indexed Glyph

    for contour in glyph:
        newGlyph.appendPath(normalizeContourCorner(contour))


    return newGlyph

def drawPointsHandles(glyphShape, diam=5): #given a Bezier curve, draws the curve and the on and off curve points, diam is the size of the dots and squares
    stroke(0,0,0)
    fill(None)
    drawPath(glyphShape)
    diameter = diam

    for contour in glyphShape.contours:
        # DEFINE STARTING POINT

        x3,y3 = (contour[0][0][0],contour[0][0][1])
    
        for segment in contour:
            x0,y0 = x3,y3
            # IF IT'S A CURVE DRAW A CURVE
            if len(segment) == 3:
                x1,y1 = segment[0][0], segment[0][1]
                x2,y2 = segment[1][0], segment[1][1]
                x3,y3 = segment[2][0], segment[2][1]

            
            
                #DRAW A LINE
                stroke(0,1,0)
                line((x2,y2),(x3,y3))
                line((x0,y0),(x1,y1))
            
            
                # SHOW THE OFF CURVE POINTS
                fill(1,0,0)
                stroke(None)
                oval(x1-diameter/2,y1-diameter/2,diameter,diameter)
                oval(x2-diameter/2,y2-diameter/2,diameter,diameter)
            
                # SHOW THE ON CURVE POINTS
                fill(0,0,0)
                stroke(None)
                rect(x3-diameter/2,y3-diameter/2,diameter,diameter)
            
            
            # IF IT'S A LINE DRAW A LINE
           # IF IT'S A LINE DRAW A LINE
            if len(segment) == 1:
                x3,y3 = segment[0][0], segment[0][1]
            
                #SHOW POINTS
                fill(0,0,0)
                rect(x3-diameter/2,y3-diameter/2,diameter,diameter)

    return