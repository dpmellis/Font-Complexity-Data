import drawBot
import csv
import time

from importlib import reload
import typeExtractor
reload(typeExtractor)

from typeExtractor import *

log = open('./Log/log.txt','w') #initialize log file
log.write('')
log.close()

exportData = [['Font Name', 'Family', 'Serif', 'Weight', 'Optical Size', 'Italic', 'Font Width', 'Style', 'Case', 'Glyph Name', 'Glyph Width', 'Glyph Height', 'Shape Area', 'Shape Width', 'Shape Height', 'On Curve Points', 'Total Points', 'Non Extrema Points']] #Headings for the data, 
        
lowerCase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

upperCase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

testLetters = ['A','B','C']

fileName = 'fonts' #The name of a csv file that contains the PostScript font name and typographic information about that font.
#The fields are Font Name, Family, Weight, Optical Size, Italic, Font Width, Style
#Example file is test.csv, the header row needs to be deleted before use    

fontNames =[]
with open(fileName+'.csv', newline='') as csvfile: #Opens filename.csv and loads it into fontNames
    fontReader = csv.reader(csvfile, delimiter =',')
    for name in fontReader:
        if any(name): #ignore blank rows
            fontNames.append(name)

totalNames= len(fontNames)
print(totalNames)

#Extracts data from 10 rows of fontNames at a time. The position in fontNames is given by i. This is because as of now the program slows considerably after about extracting data from 17 fonts [something to fix]
tic = time.perf_counter() 
i = 0
chunkSize = 257
print('Chunk Size: ', chunkSize)
exportData=[]
for currentFont in fontNames[i*chunkSize:(i+1)*chunkSize]: 
    #Extract uppercase data
    exportData = exportData + extractData(upperCase,currentFont + ['Upper'],1)
    #Extract lowercase data
    exportData = exportData + extractData(lowerCase,currentFont + ['Lower'],1)
    #Extract data from testLetters
#    exportData = exportData + extractData(testLetters, currentFont + ['test'])

#Write the data in a directory called dataDump labeled with i
with open('./dataDump/'+fileName+' output'+str(i)+'.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)     # creating a csv writer object
    for rows in exportData:
        csvwriter.writerow(rows) # writing the fields

toc = time.perf_counter()
print(f"Took {toc - tic:0.2f} seconds")


