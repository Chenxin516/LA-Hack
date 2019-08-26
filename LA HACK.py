#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 20:10:05 2019

@author: liujunyou
"""
import time
import requests
import os
import operator
from urllib.parse import quote


STREET_SCORE = "street_score_t"
os.system('touch ' + STREET_SCORE + "1")
os.system('touch ' + STREET_SCORE + "2")
os.system('touch ' + STREET_SCORE + "3")
os.system('touch ' + STREET_SCORE + "4")
os.system('touch ' + STREET_SCORE + "5")
os.system('touch ' + STREET_SCORE + "6")
os.system('touch ' + STREET_SCORE + "7")
os.system('touch ' + STREET_SCORE + "8")
os.system('touch ' + STREET_SCORE + "9")
os.system('touch ' + STREET_SCORE + "10")
os.system('touch ' + STREET_SCORE + "11")
os.system('touch ' + STREET_SCORE + "12")

os.system('touch ' + "new_data.csv")




OLD_FILE = "copy.csv"
NEW_FILE = "new_data.csv"



street_to_score_list = [dict() for x in range(12)]


 

def change_address():
    new_file = open(NEW_FILE, "w")
    old_file = open(OLD_FILE, "r")

    all_lines = old_file.readlines()
    all_lines = all_lines[1:]
    request1 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
    request3="&inputtype=textquery&fields=formatted_address&key=%20AIzaSyBugXsNlBMRTPFRxsMYAqTlIcie0DzJseM"
    for line_content in all_lines:
        columns = line_content.split(",")
        old_address = columns[23] 
        request2 = quote(old_address)
        request = request1 + request2 + request3        
        r = requests.get(request)
        raw = str(r.text)
        new_address = ""
        try:
            new_address = raw.split(",")[0].split('"')[5]
        except:
            new_address = ""
        
        if new_address == "":
            continue
        columns[23] = new_address
        
        for i in range(24):
            columns[i] += ","
        new_line_content = "".join(columns)
        new_file.write(new_line_content)
    
    new_file.close()
    old_file.close()
    
        
        #columns[23] = correct_address
        
'''
def get_address(address):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/")
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div/div[1]/div/div[1]/input").send_keys(address)
    driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div/div[3]/center/input[1]").click() #click search
    
    if "Search instead for" in driver.page_source:
        driver.find_element_by_xpath("//*[@id='fprsl']").click()
    if "Did you mean:" in driver.page_source:
        driver.find_element_by_xpath("//*[@id='taw']/div[2]/div/p/a").click()

        

    
    while True:
        try:
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='tsf']/div[2]/div/div[3]/center/input[1]").click() #click search
            time.sleep(1)
            if "shopping" in driver.page_source:
                break
        except:
            continue
    
        
    correct = driver.find_element_by_class_name("desktop-title-content")
    return str(correct.text)
    
'''

def calc_street_score():   
    with open(NEW_FILE) as crime_file:
        all_lines = crime_file.readlines()
        all_lines = all_lines[1:]
        #print(all_lines[0])
    
        for line_content in all_lines:
            columns = line_content.split(",")
            score = 10 - int(columns[7])/100
            '''
            Reliability check: got the same results when used a different scoring system
            
            score = int(columns[7])/100
            if score > 4:
                score = 0
            else:
                score = 5 - score
            #california crime code's first digit can be a number from 1-9. By California convention,
            #1 = serious crime.  9 = less serious crime.
            #Only level 1-4 is of physical violence, so we'll disregard crimes 5-9.
            #We'll assign a danger score of 4 to level 1 crimes, a score of 3 of level 2 crimes... and 1 for level 4.
            '''
            address = columns[23]
            
            if address == "": #sanity check for the address to not be empty string
                print(line_content)
                print(columns)
            
            
            time = str(columns[3])
            length = len(time)
            if length == 4: 
                time = int(time[0:2])
            elif length == 1 or 3:
                time = int(time[0])
            elif length == 2: #see case such as 30, intepret as 0030
                time = 0
            
            #put the info in the correct dictionary 
            index = time//2 #integer division, from 0 to 11
            
            #try except statement to initialied address value pairs
            try:
                if (street_to_score_list[index][address] == 0):  
                    pass
            except:#it's not intialized yet (address - score pair not created yet)
                street_to_score_list[index][address] = 0
            
            street_to_score_list[index][address] = street_to_score_list[index][address] + score
    crime_file.close()
    write_to_database()
    return street_to_score_list

def write_to_database(): 
    for i in range(12):
        database = open(STREET_SCORE + str(i+1), "w")
        cur_dict = street_to_score_list[i]
        for key,value in cur_dict.items():
            line_content = key + "," + str(value)
            database.write(line_content + "\n")
        database.close()
        
            
            


def main():
    #change_address()
    
    calc_street_score()
    
    for i in range(12):
        print( max(street_to_score_list[i].items(), key=operator.itemgetter(1)) )
    
    

    
if __name__ == "__main__":
    main()
