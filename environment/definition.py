import random , time , json 
import requests
#import pygame 
from filelock import FileLock
from ollama import AsyncClient
import asyncio , requests

lock = FileLock("environment.json.lock")

characters = {"iuno" : [-1,-1] , 
              "aoi" : [-1,-1] , 
              "ishan" : [-1,-1]
            }
rooms = {
    "living-room" : {"index": [0,50 , 0 ,50] , "people": []} , 
    "gallery" : {"index": [51 , 100 , 0 , 50] , "people": []} ,
    "bedroom" : {"index": [51 , 100 , 51 , 100] , "people": []} ,
    "entrance" : {"index": [0, 50 , 51, 100] , "people": []}
    }

# -------------------

mapping = [["" for i in range(100)] for j in range(100)]

def call_json():
    global rooms , characters
    data = [characters , rooms]
    with lock:
        file = open(r"environment\environment.json" , "r")
        data = json.load(file)
        file.close()
    rooms = data[1]
    characters = data[0]

def send_json():
    global rooms , characters
    data = [characters , rooms]
    with lock:
        file = open(r"environment\environment.json" , "w")
        json.dump(data, file , indent = 4)
        file.close()

def initaite_position():
    for all in characters.keys():
        for i in range(2):
            characters[all][i] = random.randint(0,100)
        print(f"{all} spawned at {characters[all]}")

def identify_position():
    for all in characters.keys():
        set = 0
        for r in rooms.keys():
            if characters[all][0] >= rooms[r]["index"][0] and characters[all][0] <= rooms[r]["index"][1] and characters[all][1] >= rooms[r]["index"][2] and characters[all][1] <= rooms[r]["index"][3]:
                for room in rooms.keys():
                    if all in rooms[room]["people"] and room != r :
                        rooms[room]["people"].remove(all)
                    if not all in rooms[r]["people"]:
                        rooms[r]["people"].append(all)
                        print(f"{all} is in {r}")
                        set = 1
        if set == 0:
            print(f"couldnt find room of {all} , position : {characters[all]}")


#while True:
    # this is the world clock later ill replace with pygame

# reset to initial 
send_json()
s = time.time()
for i in range(1000):
    call_json()
    initaite_position()
    identify_position()
    send_json()
e = time.time()
print(str(e-s) + "seconds")

            


