
# coding: utf-8

# In[33]:


import regex
import sys
import datetime
from operator import itemgetter


# In[18]:


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


# In[ ]:


# TESTCASE1
f = open("C:\Users\grace\Desktop\input1.txt","r")
contents = f.read()
f.close()
print contents 


# In[ ]:


#TESTCASE2
t = open("C:\Users\grace\Desktop\input2.txt","r")
contents = t.read()
t.close()
print contents


# In[34]:


#TESTCASE3
d = open("C:\Users\grace\Desktop\input3.txt","r")
contents = d.read()
d.close()
print contents


# In[35]:


# Keep in mind we gotta hide the drivers that are speedy af or just off the clock.
all_commands = contents.splitlines()
print all_commands


# In[36]:


def getDriveTime(start, end):
    #get trip drive time in hours
    format = '%H:%M'
    startTime = datetime.datetime.strptime(start, format)
    endTime = datetime.datetime.strptime(end, format)
    diff = endTime - startTime
    hours = abs(diff).total_seconds() / 3600.0 # get time in hours
    
    return hours


# In[37]:


def getSpeed(hours, distance):
    #get average speed
    #ensure 5mph < speed < 100mph
    speed = float(distance) / float(hours)
    if float(5) < speed < float(100):
        res = speed
    else:
        res = -1
    return res


# In[38]:


# Make a dictionary to store drivers and their bullshit
drivers = dict()
for x in all_commands:
    tokens = x.split() # Put all words into a list.
    # Pull out command
    command = tokens[0]
    if command == "Driver":
        name = tokens[1] #2nd token in list is name.
        drivers[name] = {"total_distance": float(0), "total_time": float(0), "avg_speed": -1}
    elif command == "Trip":
        # If its trip we know there are 3 parts: start, stop, miles. WE need hours.
        name = tokens[1]
        start = tokens[2]
        end = tokens[3]
        miles = float(tokens[4])
        # Verify mph 5 < x < 100
        if name in drivers:
            hours = getDriveTime(start,end)
            speed = getSpeed(hours,miles)
            if speed != -1: # If it's -1, it's outside our threshold. Ignore...
                drivers[name]['total_distance'] = drivers[name]['total_distance'] + miles
                drivers[name]['total_time'] = drivers[name]['total_time'] + hours
                
                # Average speed of a bunch of different rates and distances is the TOTAL DISTANCE / TOTAL TIME.
                # We also keep all numbers as are until the moment of computation, then after computing we round up to the
                # nearest whole number and convert to an integer.
                drivers[name]['avg_speed'] = int(round(drivers[name]['total_distance'] / drivers[name]['total_time']))
            else:
                drivers[name][int(round(miles))] = int(round(speed))
            #YAY BECAUSE IT'S ALL ORGANIZED NOW THANK GOD
        else:
            drivers[name] = {}
        print sorted(drivers[name])
    else:
        # Not a specified command
        print("This is not a command. Exterminating driver...")
        exit(0)

print drivers


# In[39]:


# Sort dictionaries on-the-fly and create a sorted list with the proper text...
def create_output_and_sort(drivers):
    output_list = []
    while(bool(drivers)): # While dictionary not empty
        winner = ''
        winner_distance = float(-999) # Largest distance
        for name in drivers:
            if drivers[name]["total_distance"] > winner_distance:
                # This is our new winner!
                winner_distance = drivers[name]["total_distance"]
                winner = name

        # After checking each driver, we have found the current highest mileage one. Add in order to list, and remove
        # from the dictionary...
        if winner_distance != 0:
            output_list.append(winner + ': '+ str(round(drivers[winner]['total_distance'])) + ' miles @ ' + str(round(drivers[winner]['avg_speed'])) + ' mph')
        else:
            # Means we have a 0 miles case. (Or no speed! No significant trips)
            output_list.append(winner + ': 0 miles')
        del drivers[winner] # Removes this dude from the list.
    return output_list


# In[ ]:


#OUTPUT1
output = create_output_and_sort(drivers)
with open("C:\Users\grace\Desktop\output1.txt", "w") as text_file:
        text_file.write('\n'.join(output))


# In[ ]:


#OUTPUT2
output = create_output_and_sort(drivers)
with open("C:\Users\grace\Desktop\output2.txt", "w") as text_file:
        text_file.write('\n'.join(output))


# In[40]:


#OUTPUT3
output = create_output_and_sort(drivers)
with open("C:\Users\grace\Desktop\output3.txt", "w") as text_file:
        text_file.write('\n'.join(output))

