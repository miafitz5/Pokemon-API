#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 11:27:13 2023

@author: miafitzgerald
"""
# Name: Mia
# Assignment: Lab 05
# Title: Pokemon JSON task
# Course: CS1
# Date: 11/7/2023
# Sources consulted: Nico 

#Bugs: pics() prints images but not specfically 3 versions of the image of 5 random Pokemon.

import requests
import random
from PIL import Image
from io import BytesIO
import json
import matplotlib.pyplot as plt
from os import path

def main():
    end = 6
    print("Select an option (1-6):")
    x = int(input("1. Pokemon Within Range 2. Show Random Sprites 3. Subgroup Names & Their Moves 4. Subgroup Names by Type 5. Search for Specific Character 6. Exit "))
    while x!= end:
        if x == 1:
            printAllChar()
        elif x == 2:
            pics()
        elif x == 3:
            printAllCharMov()
        elif x == 4:
            printNamesType()
        elif x == 5:
            search_by_name()
        else:
            print("Wrong Choice")
        x = int(input("1. Pokemon Within Range 2. Show Random Sprites 3. Subgroup of Names & Their Moves 4. Subgroup Names by Type 5. Search for Specific Character 6. Exit "))
    
    
def printAllChar():
    address = "https://pokeapi.co/api/v2/pokemon/"
    r2 = requests.get(address)
    content = r2.json()
    limit = content["count"]

    while True:
        number = int(input("Enter pokemon ID: "))
        number2 = int(input("Enter a second pokemon ID: "))
        
        if number < number2 and number <= limit and number2 <= limit: 
            break
        else:
            print("The numbers given are invalid")
    dicto2 = {}
    for i in range(number,number2+1):
        full = address + str(i) 

        r = requests.get(full)
        dicto = r.json()

        print(dicto["name"])
        dicto2[dicto["name"]] = str(i)
        
    with open ("names.json", "w") as fp:
        json.dump(dicto2,fp, indent = 4)
        
def pics():
    for i in range(15):
        rand_num = random.randint(1,151)
        address = "https://pokeapi.co/api/v2/pokemon/"
        full = address + str(rand_num)
        r = requests.get(full)
        contents = r.json()
        x = contents["sprites"]
        keysD = list(x.keys())
        val = random.choice(keysD)
        while val == "other" or val == "versions":
            val = random.choice(keysD)
        sprite_url = contents["sprites"][val]
            
        if sprite_url != None:
            r = requests.get(sprite_url)
            response = requests.get(sprite_url)
            img = Image.open(BytesIO(response.content))
            img.show()
        
def printAllCharMov():
    #Print a subgroup of names of the original 151 characters and their moves
    while True:
        num = int(input("Enter numbers to use for the a range of 10: "))
        num2 = int(input("Enter a second number: "))
        
        if num < num2 and num <= 151 and num2 <= 151 and num2-num<=10: 
            break
        else:
            print("The numbers given are invalid")
    
    for i in range(num,num2+1): 
        address = "https://pokeapi.co/api/v2/pokemon/"
        full = address + str(i)
        r = requests.get(full)
        dicto = r.json()
        
        lista = dicto["moves"]
        if len(lista) < 10:
            for i in range(len(lista)):
                print(lista[i]["move"]["name"])
        elif len(lista) > 10:
            for i in range(10):
                print(lista[i]["move"]["name"])
                
        print("\n")

    with open ("names_moves.json", "w") as fp:
        json.dump(lista,fp, indent = 4)
        

def printNamesType():
    x = int(input("1. Generate Files for types 2. Ask Type 3. Plot 4. Return to previous menu "))
    
    if x == 1:
        if path.exists("names_types.json"):
            print("File already exists")
        else:
            address = "https://pokeapi.co/api/v2/pokemon/"
            limit = 151
            num1 = 1
            
            type_counts = {"grass": [], "fire": [], "water": [], "others": []}
            
            for i in range(num1, limit+1):
                full = address + str(i)
                r = requests.get(full)
                
                if r.status_code == 200:
                    dicto = r.json()
                    name = dicto["name"]
                    types = [t["type"]["name"] for t in dicto["types"]]
                    if "grass" in types:
                        type_counts["grass"].append(name)
                    elif "fire" in types:
                        type_counts["fire"].append(name)
                    elif "water" in types:
                        type_counts["water"].append(name)
                    else:
                        type_counts["others"].append(name)
                else:
                    print("Error for getting the data with that ID")
                    
                with open("names_types.json", "w") as fp:
                    json.dump(type_counts, fp, indent=4)
                    
    elif  x == 2:
        if path.exists("names_types.json"):
            type_choice = input("Enter a type in lowercase: ")
            
            with open("names_types.json") as fp:
                contents = json.load(fp)
                
            if type_choice == "grass":
                print("grass type: " + str(contents[type_choice]))
            elif type_choice == "fire":
                print("fire type: " + str(contents[type_choice]))
            elif type_choice == "water":
                print("water type: " + str(contents[type_choice]))
            elif type_choice == "others":
                print("others type: " + str(contents[type_choice]))
            else:
                print("Invalid type selected.")
                
        else:
            print("This file doesn't exist...")
            
    elif x == 3:
        if path.exists("names_types.json"):
            with open("names_types.json") as fp:
                contents1 = json.load(fp)
            x = ["grass", "fire", "water", "others"]
            freq = [len(contents1["grass"]), len(contents1["fire"]), len(contents1["water"]), len(contents1["others"])]
            plt.bar(x,freq)
            plt.ylabel("Frequency")
            plt.show()
        else:
            print("This file doesn't exist...")
            
    elif x == 4:
        main()
    
def search_by_name():
    num = input("Enter a pokemon ID to learn it's name and moves: ")
    address = "https://pokeapi.co/api/v2/pokemon/"
    full = address + num
    r = requests.get(full)
    
    if r.status_code == 200:
        r = requests.get(full)
        dicto = r.json()
        
        print("The pokemon you chose is " + str(dicto["name"]))
        print("Its moves are...")
        
        lista = dicto["moves"]
        if len(lista) < 10:
            for i in range(len(lista)):
                print(lista[i]["move"]["name"])
        elif len(lista) > 10:
            for i in range(10):
                print(lista[i]["move"]["name"])
    else:
        print("That ID doesn't exist!")
        search_by_name()

main()