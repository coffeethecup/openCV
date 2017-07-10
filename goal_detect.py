import requests #for POST request
import pygame #plays sound
import time
import datetime
import RPi.GPIO as GPIO
import pymysql
import random
import randint
#http://www.tutorialspoint.com/python3/python_database_access.htm
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="goal",
                     db="goal")
cur = db.cursor()
#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT)
GPIO.output(17, 0)
GPIO.output(27, 0)
# waitingtime after goal to avoid double counting
waitingtime = 5

try:
	while True:
		if (GPIO.input(4)==False):
                        GPIO.output(17, 1)
                        team = "blue"
                        #time_goal = datetime.datetime.now()
                        time_goal = str(datetime.datetime.now())
                        time_goal = time_goal.replace(' ', 'T')+'Z'
                        print("Goal Team ", team, " Zeit:", time_goal)
                        cur.execute("INSERT INTO table_goal(team, timestamp) VALUES (%s, %s)",(team, time_goal))
                        db.commit()
                        #Torschrei
                        music_shuffle=(random.randint(1,9)
                        pygame.mixer.init()
                        pygame.mixer.music.load("goal%d.wav" % music_shuffle)
                        pygame.mixer.music.play()
                        pygame.mixer.stop
                        #POST webservice via requests package
                        data = {"wuzzler_id":"1","event":"goal","val":team ,"event_ts":time_goal}
                        response = requests.post("http://admin:Welcome-1@140.86.0.124:8080/ords/beconnected/beconnected/event/", json=data)
                        time.sleep(waitingtime)
                        GPIO.output(17, 0)

		if (GPIO.input(22)==False):
                        GPIO.output(27, 1)
                        team = "red"
                        #time_goal = datetime.datetime.now()
                        time_goal = str(datetime.datetime.now())
                        time_goal = time_goal.replace(' ', 'T')+'Z'
                        print("Goal Team ", team, " Zeit:", time_goal)
                        cur.execute("INSERT INTO table_goal(team, timestamp) VALUES (%s, %s)",(team, time_goal))
                        db.commit()
                        music_shuffle=(random.randint(1,9)
                        pygame.mixer.init()
                        pygame.mixer.music.load("goal%d.wav" % music_shuffle)
                        pygame.mixer.music.play()
                        pygame.mixer.stop
                        data = {"wuzzler_id":"1","event":"goal","val":team,"event_ts":time_goal}
                        response = requests.post("http://admin:Welcome-1@140.86.0.124:8080/ords/beconnected/beconnected/event/", json=data)

                        time.sleep(waitingtime)
                        GPIO.output(27, 0)
except KeyboardInterrupt:
	GPIO.cleanup()
	cur.close()
