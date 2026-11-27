# name of csv file: meal_planning_15_foods.csv

import csv # will be using csv files
from itertools import combinations # built in python module that provides a combination tool which will be useful

# STEP 1
food_items = []

# opening csv file
with open("../../meal_planning_15_foods.csv", "r") as file: # read mode. forgot that the csv file is in main project folder(2 folders back)

    reader = csv.DictReader(file) # csv.DictReader(file) lets me access csv info using column names

    for row in reader:
        food_items.append(row) # goes through every row in csv file

# STEP 2 
all_combinations = [] # creating a list to store all the possible combinatinos 

# going through every possible combination size. item1-15
for number in range(1, len(food_items) + 1): # adding a 1 to food_items length is crucial because im starting the item count at 1 and the computer thinks of it as 0

    for combination in combinations(food_items, number):
        all_combinations.append(combination) # adding each combination to the list

# STEP 3

#creating a list for each category
cost_list = []
calories_list = []
fat_list =[]
carbs_list = []
protein_list = []


# STEP 4

meal_id = 1 # starting the meal id's at 1

for combination in all_combinations:
    
    if len(combination) < 3: # making sure the food_item length is at least 3
        continue # skips

    # creating variables for each category
    total_cost = 0
    total_calories = 0
    total_fat = 0
    total_carbs = 0
    total_protein = 0

    # for each combination...
    for food in combination:

        # ... calculating total for each category
        total_cost += float(food["cost_usd"]) # name in csv file is cost_usd
        total_calories += float(food["calories"])
        total_fat += float(food["fat_g"])
        total_carbs += float(food["carbs_g"])
        total_protein += float(food["protein_g"])

    # Saving the meal id and total fore each category
    cost_list.append([meal_id, total_cost])
    calories_list.append([meal_id, total_calories])
    fat_list.append([meal_id, total_fat])
    carbs_list.append([meal_id, total_carbs])
    protein_list.append([meal_id, total_protein])
    

    meal_id += 1 # moving on to the next meal id

