#Import libraries 
import time 
import webbrowser 
import random 
import os 


# Check if the user has the songs.txt file in the same folder as alarmClock.py
if os.path.isfile("songs.txt") == False:
    print "ERROR: songs.txt file not present. Creating file..."
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY 
    filecreate = os.open("YT.txt", flags) # creating the missing 'songs.txt' file
    with os.fdopen(fisierCreat, 'w') as fileCreated:
        fileCreated.write("https://youtu.be/BZg8BhBWyo8") # writing youtube song link into the newly created file 


# The User can set the time they want to wake up. The String the user puts in must be the same as the example to work.
print "What time do you want to wake up?"
print "Use this form.\nExample: 06:30"
Alarm = raw_input("> ")

# I first need to state the Time variable so it's usable in the while-loop 
Time = time.strftime("%H:%M")

# This opens the text file with the youtube links 
with open("songs.txt") as f:
    # the urls are stored in the content variable 
    content = f.readlines()

# When the time does not equal the Alarm time string given above, print the time
while Time != Alarm:
    print "The time is " + Time 

    # Restating the Time variable allows the time to refresh 
    # When I tried keeping the variable outside of the loop it just repeated the initial time 
    Time = time.strftime("%H:%M")



