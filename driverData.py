
# coding: utf-8

# In[7]:


#imports
import regex
import fileinput
import sys
import datetime
from operator import itemgetter
import unittest


# In[8]:


"""
Input:
Driver Dan
Driver Alex
Driver Bob
Trip Dan 07:15 07:45 17.3
Trip Dan 06:12 06:32 21.8
Trip Alex 12:01 13:16 42.0

Discard any trips that average a speed of less than 5 mph or greater than 100 mph.

 format of hours:minutes



OUTPUT:
Alex: 42 miles @ 34 mph
Dan: 39 miles @ 47 mph
Bob: 0 miles
"""


# In[9]:


def getDriveTime(start, end):
    #get drive-time in hours
    format = '%H:%M'
    startTime = datetime.datetime.strptime(start, format)
    endTime = datetime.datetime.strptime(end, format)
    diff = endTime - startTime
    hours = abs(diff).total_seconds() / 3600.0 # to hours
    
    return hours


# In[10]:


#get average speed
#ensure 5mph < speed < 100mph
def getSpeed(hours, distance):
    assert (hours > 0), "Can't divide by 0!"
    speed = float(distance) / float(hours)
    if float(5) < speed < float(100):
        res = speed
    else:
        res = -1
        
    return res


# In[11]:


# Separate words in text line and analyze
def separate(contents):
    all_commands = contents.splitlines()
    drivers = dict()
    for x in all_commands:
        tokens = x.split() # Words into list
        command = tokens[0] # Get command
        if command == "Driver":
            name = tokens[1] # Get driver name
            drivers[name] = {"total_distance": float(0), "total_time": float(0), "avg_speed": -1}
        elif command == "Trip":
            # Trip command has 3 parts used in calculations
            name = tokens[1]
            start = tokens[2]
            end = tokens[3]
            miles = float(tokens[4])
            if name in drivers:
                hours = getDriveTime(start,end)
                speed = getSpeed(hours,miles)
                if speed != -1: # -1 is outside threshold
                    drivers[name]['total_distance'] = drivers[name]['total_distance'] + miles
                    drivers[name]['total_time'] = drivers[name]['total_time'] + hours
                
                    # round speed and cast to integer value
                    drivers[name]['avg_speed'] = int(round(drivers[name]['total_distance'] / drivers[name]['total_time']))
                else:
                    drivers[name][int(round(miles))] = int(round(speed))
            else:
                drivers[name] = {}
        else:
            # Not a known command
            print("This is not a command. Exterminating driver...")
            exit(0)
            
    return drivers


# In[12]:


# Sort dictionaries and create sorted list
def createOutputAndSort(drivers):
    output_list = []
    while(bool(drivers)): # While dictionary not empty
        winner = ''
        winner_distance = float(-999) # Largest distance
        for name in drivers:
            if drivers[name]["total_distance"] > winner_distance:
                # New largest distance
                winner_distance = drivers[name]["total_distance"]
                winner = name

        if winner_distance != 0:
            output_list.append(winner + ': '+ str(round(drivers[winner]['total_distance'])) + ' miles @ ' + str(round(drivers[winner]['avg_speed'])) + ' mph')
        else:
            # Means we have a 0 miles case. (Or no speed! No significant trips)
            output_list.append(winner + ': 0 miles')
        del drivers[winner] # Removes this dude from the list.
        
    return output_list


# In[13]:


# Output to text file
def toFile(output_list, outFile):
    i = 0
    while (i < len(output_list)):
        outFile.write(output_list[i] + "\n")
        i+=1


# In[14]:


class MyTest(unittest.TestCase):
    
    # Test getSpeed() method
    def testSpeed1(self):
        # speed > 100 mph returns -1
        hours = 2.00
        distance = 450.2
        speed = getSpeed(hours, distance) #225.1 mph
        self.assertEqual(int(round(speed)), -1)
    def testSpeed2(self):
        # speed < 5 mph returns -1
        hours = 10.00
        distance = 20.0
        speed = getSpeed(hours, distance) #2 mph
        self.assertEqual(int(round(speed)), -1)
    def testSpeed3(self):
        # speed = 57 mph returns 57
        hours = 3.50
        distance = 200.0
        speed = getSpeed(hours, distance) # 57.1 mph
        self.assertEqual(int(round(speed)), 57)
    
    # Test getDriveTime() method
    def testDriveTime1(self):
        # driveTime starting at 00:00
        start = '00:00'
        end = '01:00'
        driveTime = getDriveTime(start, end)
        self.assertEqual(driveTime, 1.0)
    def testDriveTime2(self):
        # driveTime ending at 23:59
        start = '23:00'
        end = '23:59'
        driveTime = getDriveTime(start, end)
        self.assertEqual(driveTime, 0.9833333333333333) # 16 values after decimal
    def testDriveTime3(self):
        # driveTime across multiple hours
        start = '10:00'
        end = '14:30'
        driveTime = getDriveTime(start, end)
        self.assertEqual(driveTime, 4.5)
        
    # Test separate() method
    def testSep1(self):
        # Provided input text
        f = open("C:\Users\grace\Desktop\input1.txt","r")
        contents = f.read()
        f.close()
        dExpected = {'Dan': {'total_time': 0.8333333333333333, 'avg_speed': 47, 'total_distance': 39.1}, 'Alex': {'total_time': 1.25, 'avg_speed': 34, 'total_distance': 42.0}, 'Bob': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}}
        drivers = separate(contents)
        self.assertEqual(drivers, dExpected)
    def testSep2(self):
        # Star Wars input text
        t = open("C:\Users\grace\Desktop\input2.txt","r")
        contents = t.read()
        t.close()
        dExpected = {'JarJar': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Luke': {'total_time': 5.583333333333333, 'avg_speed': 63, 'total_distance': 350.0}, 'Leia': {'total_time': 23.983333333333334, 'avg_speed': 60, 'total_distance': 1440.0}, 'Anakin': {'total_time': 1.0, 'avg_speed': 55, 'total_distance': 55.2}, 'Lando': {'total_time': 2.0, 'avg_speed': 50, 'total_distance': 100.0}}
        drivers = separate(contents)
        self.assertEqual(drivers, dExpected)
    def testSep3(self):
        # Lord of the Rings input text
        d = open("C:\Users\grace\Desktop\input3.txt","r")
        contents = d.read()
        d.close()
        dExpected = {'Arwen': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Frodo': {'total_time': 2.55, 'avg_speed': 20, 4: -1, 'total_distance': 50.0}, 'Gollum': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Legolas': {'total_time': 1.95, 'avg_speed': 10, 'total_distance': 20.0}}
        drivers = separate(contents)
        self.assertEqual(drivers, dExpected)
        
    # Test createOutputAndSort() method
    def testSort1(self):
        # Provided input text
        drivers = {'Dan': {'total_time': 0.8333333333333333, 'avg_speed': 47, 'total_distance': 39.1}, 'Alex': {'total_time': 1.25, 'avg_speed': 34, 'total_distance': 42.0}, 'Bob': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}}
        expectedList = ['Alex: 42.0 miles @ 34.0 mph', 'Dan: 39.0 miles @ 47.0 mph', 'Bob: 0 miles']
        self.assertEqual(createOutputAndSort(drivers), expectedList)
    def testSort2(self):
        drivers = {'JarJar': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Luke': {'total_time': 5.583333333333333, 'avg_speed': 63, 'total_distance': 350.0}, 'Leia': {'total_time': 23.983333333333334, 'avg_speed': 60, 'total_distance': 1440.0}, 'Anakin': {'total_time': 1.0, 'avg_speed': 55, 'total_distance': 55.2}, 'Lando': {'total_time': 2.0, 'avg_speed': 50, 'total_distance': 100.0}}
        expectedList = ['Leia: 1440.0 miles @ 60.0 mph', 'Luke: 350.0 miles @ 63.0 mph', 'Lando: 100.0 miles @ 50.0 mph', 'Anakin: 55.0 miles @ 55.0 mph', 'JarJar: 0 miles'] 
        self.assertEqual(createOutputAndSort(drivers), expectedList)
    def testSort3(self):
        drivers = {'Arwen': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Frodo': {'total_time': 2.55, 'avg_speed': 20, 4: -1, 'total_distance': 50.0}, 'Gollum': {'total_time': 0.0, 'avg_speed': -1, 'total_distance': 0.0}, 'Legolas': {'total_time': 1.95, 'avg_speed': 10, 'total_distance': 20.0}}
        expectedList = ['Frodo: 50.0 miles @ 20.0 mph', 'Legolas: 20.0 miles @ 10.0 mph', 'Arwen: 0 miles', 'Gollum: 0 miles'] 
        self.assertEqual(createOutputAndSort(drivers), expectedList)
        
        
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


# In[17]:


#Main prompt
inFile = raw_input("Please provide path of input file: ")
outFile = raw_input("Please provide path of output file: ")
inputData = open(inFile,"r")
outputData = open(outFile, "w")
contents = inputData.read()
inputData.close()
drivers = separate(contents)
output_list = createOutputAndSort(drivers)
toFile (output_list, outputData)
outputData.close()

