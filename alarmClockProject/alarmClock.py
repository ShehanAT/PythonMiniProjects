#Import libraries 
import time 
import webbrowser 
import random 
import os 


# Check if the user has the songs.txt file in the same folder as alarmClock.py
if os.path.isfile("songs.txt") == False:
    print("ERROR: songs.txt file not present. Creating file...")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY 
    filecreate = os.open("songs.txt", flags) # creating the missing 'songs.txt' file
    with os.fdopen(filecreate, 'w') as fileCreated:
        fileCreated.write("https://youtu.be/BZg8BhBWyo8\n") # writing youtube song link into the newly created file 
        fileCreated.write("https://www.youtube.com/watch?v=FATTzbm78cc\n")
        fileCreated.write("https://www.youtube.com/watch?v=mUT3KoxVzQg\n")
        fileCreated.write("https://www.youtube.com/watch?v=_AWIqXzvX-U\n")
        fileCreated.write("https://www.youtube.com/watch?v=0Z4cLmbw6q0\n")
        fileCreated.write("https://www.youtube.com/watch?v=TZ827lkktYs")
# The User can set the time they want to wake up. The String the user puts in must be the same as the example to work.
print("What time do you want to wake up?")
print("Use this form.\nExample: 06:30:20")
Alarm = input("> ")

# I first need to state the Time variable so it's usable in the while-loop 
Time = time.strftime("%H:%M:%S")

# This opens the text file with the youtube links 
with open("songs.txt") as f:
    # the urls are stored in the content variable 
    content = f.readlines()

# When the time does not equal the Alarm time string given above, print the time
while Time != Alarm:
    print("The time is " + Time) 

    # Restating the Time variable allows the time to refresh 
    # When I tried keeping the variable outside of the loop it just repeated the initial time 
    Time = time.strftime("%H:%M:%S") # Time will be assigned the current time

    # This keeps the loop from flooding the command line with updates of the time
    time.sleep(1) # pause the program for a second in order to increment the Time variable in seconds

# If the Time variable is equal to the Alarm string, this code activates 
if Time == Alarm:

    print("Time to Wake up!")
    # from the variable content, a random link is chosen and then that link is stored in random_video variable
    random_video = random.choice(content)
    # Using the webbrowser library, it opens this youtube video link 
    # The videos are various Aphex Twin songs 
    webbrowser.open(random_video)





