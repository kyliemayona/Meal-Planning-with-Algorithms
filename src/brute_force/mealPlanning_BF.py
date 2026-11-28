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

meal_items = {} # storing the food items belonging to each meal so that i can display actual names of food and not just an id 


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
    
    meal_items[meal_id] = combination

    meal_id += 1 # moving on to the next meal id

    


# STEP 5
# meal information is stored like this cost_list = [[1, 4.25], [2, 3.25]]. position 0 is meal id. position 1 is total cost
# lambda creates a smalltemporary function. used to tell python what value to use when sorting (witout needing a seperate function)

# sorting from lowest to highest
cost_list.sort(key=lambda meal: meal[1]) 

# closest to 665
calories_list.sort(key=lambda meal: abs(meal[1] - 665)) # using absolute value because 660 and 670 should both be 5 apart

# closest to 20
fat_list.sort(key=lambda meal: abs(meal[1] - 20))

# closest to 65
carbs_list.sort(key=lambda meal: abs(meal[1] - 65)) 

# highest to lowest
protein_list.sort(key=lambda meal: meal[1], reverse=True) # reversing because i want highest to lowest


# STEP 6
meal_scores = {} # creating a dictionary to store each meal's total points

for meal in cost_list: # giving each meal an ititial score of 0
    meal_scores[meal[0]] = 0


def give_points(category_list, target=None, highest=False):
    previous_value = None # storing the previous meals value to check for ties
    current_rank = 0 # starting the meal ranking at 0

    # going through each mel in the sorted list
    for position in range(len(category_list)):

        meal = category_list[position] # getting the meal at the current position in the list

        # checking if there is a terget number...
        if target is not None:
            current_value = abs(meal[1] - target) # finding how far the meal is from the target. smaller the difference the better

        elif highest: # ... or if higher numbers are better...
            current_value = -meal[1] # using a negative numbe so highest protein reanks first

        else: # ... using actual value (for cost )
            current_value = meal[1]

        # this gives tied meals the same placement, checking if this is the first meal or if its value is diff from the prev meal
        if position == 0 or current_value != previous_value:
            current_rank = position + 1 # position starts at 0 so adding 1

        # adding the placement points to the meal's score. meal[0] is the meal id
        meal_scores[meal[0]] += current_rank

        # remembered to save the current value to compare with the next meal
        previous_value = current_value

# giving points for all 5 categories 
give_points(cost_list)
give_points(calories_list, target=665)
give_points(fat_list, target=20)
give_points(carbs_list, target=65)
give_points(protein_list, highest=True)



# STEP 7

# sorting meals (lowest score is best)
ranked_meals = sorted(meal_scores.items(), key=lambda meal: meal[1]) 

# finding the score of the eight meal
# [1] = total points
eighth_score = ranked_meals[7][1] # using the sorted list. using [7] because python starts counting at 0


with open(r"C:\Users\ivett\OneDrive\Documents\Algorithms\Meal-Planning-with-Algorithms\MainResults/brute_force_main_results.txt", "w") as file: # opening a file in write mode because im sending the results to it
# r tells python that backslashes are regular characters
    # title:)
    file.write(" ---------------------------- BRUTE FORCE RESULTS ---------------------------- \n\n")

     # only displaying tp 8 meals
    for meal_id, score in ranked_meals:

        # keeping meals with scores less than or equal to 8th place
        if score <= eighth_score:

            # writing the total points
            file.write("Total Points: " + str(score) + "\n")

            # writing the meal itss
            file.write("Food Items:\n")

            for food in meal_items[meal_id]:
                file.write("- " + food["food"] + "\n")

            # Add an empty line between meals
            file.write("\n")

# Tell the user that the results were saved
print("Results saved to brute_force_main_results.txt")

