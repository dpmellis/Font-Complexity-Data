import drawBot
from importlib import reload
import typeDataUtilities 
reload(typeDataUtilities)

from typeDataUtilities import *

currentFont = 'GillSans'
letter = 'O'

font(currentFont, fontSize=1000)
currentLetter = BezierPath() #initializing bezier curve
currentLetter.text(letter, font=currentFont, fontSize=1000)
#currentLetter.translate(100,100)
print(textSize(letter) )


print(len(currentLetter.onCurvePoints))
print(currentLetter.onCurvePoints)
drawPointsHandles(currentLetter)

# import csv
# fileName = 'test'
# fontNames =[]
# with open(fileName+'.csv', newline='') as csvfile:
#     fontReader = csv.reader(csvfile, delimiter =',')
#     for name in fontReader:
#         fontNames.append(name)

# for currentFont in fontNames:
# #    currentFont = name[0]
#     print(currentFont+[0],'\n')

print(font(fontFilePath()) )

