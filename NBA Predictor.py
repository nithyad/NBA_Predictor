# coding: utf-8
# This code uses Beautiful soup to scrape the web data on the NBA site, and predict which teams are most likely to win the NBA, by looking at the city they are from!

"""
#
#     Question: Which NBA team is most likely to win based on their city?
#
"""
#on a side note- DUB NATION!!!  

    #APPROACH:
    # First, I looked up to find a page that defines all NBA team mascots
    # Then, I used Beautiful soup to come up with the name of the city based on the NBA team
    # Next, I grabbed a page that ranks the popularity of team names
    # Then, I used Beautiful soup to come up witha score for each time based on the popularity of the city  

import requests
from bs4 import BeautifulSoup

def get_name_page():
    """
    Gets the names of the cities and uses Beautiful Soup to make it into a soup
    """
    city_url = "http://www.infoplease.com/toptens/largestcities.html"
    
    response = requests.get(city_url)   # requests page info

    if response.status_code == 404:                 # in case the page doesn't exist (testing purpose)
        print("Sorry, this page doesnt work")

    data_from_url = response.text                   # gets HTML text from the page
    soup = BeautifulSoup(data_from_url,"lxml")      # Beautiful Soup!!!!!!
    return soup



def find_city_score( city_name, soup ):
    """
    Gets the name of City, and gets the score from it, using the soup from above based on 11
    """
    
    #need to get the City name and score
    #inside the table, under <tr> and under middle <td align="left" class="ttcontent"> (how to get it below)
    L = soup.table.tr.td.find_all("tr")

    
    #because the city name starts only at 4, and goes +10
    for i in range(4,14):
        
        text = L[i].find_all("td")[1].text  
        #city is on "td" at 1

        text1 = L[i].find_all("td")[1].text
        num_comma = text1.find(",") #index of the comma
        #to take out the comma 
        extracted_city = text1[0:num_comma]

        #to see if the city is in the list
        if city_name == extracted_city:
                #see what the score is (if in the top)
                num_str = L[i].find_all("td")[0].text 
                num_str = num_str[:-1]
                return int(num_str)  
    
    #not in loop?
    return 11


def get_city_name(mascot):
    """
    Gives an input of a mascot, and will return a soup of the details of the team
    """
    team_url = "http://www.nba.com/teams/" + mascot.lower() #to make sure its lowercase
    print(team_url)
    response = requests.get(team_url)         
    
    if response.status_code == 404:                 
        print("For the team", team, "There was a problem with getting the page")
        print(team_url)
        
    data_url = response.text                   # the HTML text from the page
    soup = BeautifulSoup(data_url,"lxml")      # parsed with Beautiful Soup
    return soup


def extract_team_city(soup, mascot):
    """
    Will get the soup from above function, and will try and parse through to find the city name
    """
    #the city is in the text area
    T = soup.title.text 
    #the city is before the mascot 
    index = T.find(mascot)
    #take up to the mascot, without the space
    city = T[0:index].strip()
    return city



def main():
    """
    runs the program above to see which team will win, based on their city
    """
    #APPROACH:
    # First, I looked up to find a page that defines all NBA team mascots
    # Then, I used Beautiful soup to come up with the name of the city based on the NBA team
    # Next, I grabbed a page that ranks the popularity of team names
    # Then, I used Beautiful soup to come up witha score for each time based on the popularity of the city

    mascot_1 = 'Spurs'
    mascot_2 = 'Lakers'
    team_soup_1 = get_city_name(mascot_1)
    team_soup_2 = get_city_name(mascot_2)

    team_city_1 = extract_team_city( team_soup_1, mascot_1)
    team_city_2 = extract_team_city( team_soup_2, mascot_2 )

    city_soup = get_name_page()
    team1_score = find_city_score(team_city_1, city_soup)
    team2_score = find_city_score(team_city_2, city_soup)

    print("The " + mascot_1 + " are for " + team_city_1 + " with a score of " + str(team1_score))
    print("The " + mascot_2 + " are for " + team_city_2 + " with a score of " + str(team2_score))

    if (team_city_1 > team_city_2):
        return("The " + mascot_2 + " from " + team_city_2 + " are more likely to win.")
    else:
        return("The " + mascot_1 + " from " + team_city_1 + " are more likely to win.")

