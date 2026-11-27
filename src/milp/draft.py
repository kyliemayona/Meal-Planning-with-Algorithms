#import libraries
import csv
import pulp#creates the milp model, decision variables, constraints, and objective function
from pathlib import Path#locates the csv file within your repository.
import time#measures execution time

#nutritional targets
target_calories = 665
target_fat = 20
target_carbs = 65

#optimization goals
#minimize cost
#maximize protein

#meal requirements
minimum_foods = 3
number_of_meals = 8

#empty list to store food items
foods = []

#locate csv file
csv_file = Path(__file__).resolve().parents[2] / "meal_planning_15_foods.csv"

#read csv file
with open(csv_file, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        foods.append({
            "name": row["food"],
            "cost": float(row["cost_usd"]),
            "calories": float(row["calories"]),
            "fat": float(row["fat_g"]),
            "carbs": float(row["carbs_g"]),
            "protein": float(row["protein_g"])
        })

print("Number of foods:", len(foods))

#make sure there are enough food items to create a meal
if len(foods) < minimum_foods:
    raise ValueError("Not enough food items to create a meal.")

#start execution timer
start_time = time.perf_counter()

#create the milp model.
model = pulp.LpProblem("Meal_Optimization", pulp.LpMinimize)

#create binary decision variables
#0 means the food is not selected 1 means it is
x = []

for i in range(len(foods)):
    x.append(
        model.add_variable(
            f"food_{i}", 0, 1, cat=pulp.LpBinary
        )
    )

#require at least three food items.
model += pulp.lpSum(x) >= minimum_foods

#create expressions for cost, calories, fat, carbohydrates, and protein.
total_cost = pulp.lpSum(
    foods[i]["cost"] * x[i]
    for i in range(len(foods))
)

total_calories = pulp.lpSum(
    foods[i]["calories"] * x[i]
    for i in range(len(foods))
)

total_fat = pulp.lpSum(
    foods[i]["fat"] * x[i]
    for i in range(len(foods))
)

total_carbs = pulp.lpSum(
    foods[i]["carbs"] * x[i]
    for i in range(len(foods))
)

total_protein = pulp.lpSum(
    foods[i]["protein"] * x[i]
    for i in range(len(foods))
)

#create variables to store nutritional deviations
calorie_dev = model.add_variable("calorie_dev", 0)
fat_dev = model.add_variable("fat_dev", 0)
carb_dev = model.add_variable("carb_dev", 0)

#calculate the difference between total calories and target calories
model += calorie_dev >= total_calories - target_calories
model += calorie_dev >= target_calories - total_calories

#calculate the difference between total fat and target fat
model += fat_dev >= total_fat - target_fat
model += fat_dev >= target_fat - total_fat

#calculate the difference between total carbs and target carbs
model += carb_dev >= total_carbs - target_carbs
model += carb_dev >= target_carbs - total_carbs

#calculate maximum values to normalize each category
max_cost = sum(food["cost"] for food in foods)
max_protein = sum(food["protein"] for food in foods)

max_calorie_dev = max(
    target_calories,
    sum(food["calories"] for food in foods) - target_calories
)

max_fat_dev = max(
    target_fat,
    sum(food["fat"] for food in foods) - target_fat
)

max_carb_dev = max(
    target_carbs,
    sum(food["carbs"] for food in foods) - target_carbs
)

#each category is worth 20 percent
weight = 0.20

#create objective function
#minimize cost and nutritional deviations while maximizing protein
model += weight * (
    total_cost / max_cost
    + calorie_dev / max_calorie_dev
    + fat_dev / max_fat_dev
    + carb_dev / max_carb_dev
    + (1 - total_protein / max_protein)
)

#empty list to store the best meal combinations
best_meals = []

#loop through the model to find the top 8 meals
for meal_number in range(number_of_meals):

    #solve the milp model
    #solve the milp model
#error: pulp cannot execute the cbc solver
#need to install cbc or fix the solver path
    model.solve(pulp.COIN_CMD(msg=False))

    #check if an optimal meal was found
    if model.status != pulp.LpStatusOptimal:
        print("No more optimal meals found.")
        break

    #empty lists to store selected and unselected food items
    selected_foods = []
    unselected_foods = []

    #determine which food items were selected
    for i in range(len(foods)):
        if x[i].varValue > 0.5:
            selected_foods.append(i)
        else:
            unselected_foods.append(i)

    #store meal information
    best_meals.append({
        "foods": [foods[i]["name"] for i in selected_foods],
        "cost": pulp.value(total_cost),
        "calories": pulp.value(total_calories),
        "fat": pulp.value(total_fat),
        "carbs": pulp.value(total_carbs),
        "protein": pulp.value(total_protein),
        "score": pulp.value(model.objective)
    })

    #exclude the current meal combination to prevent duplicates
    model += (
        pulp.lpSum(1 - x[i] for i in selected_foods)
        + pulp.lpSum(x[i] for i in unselected_foods)
        >= 1
    )

#stop execution timer
end_time = time.perf_counter()
execution_time = end_time - start_time

#display the top 8 meal combinations
for i in range(len(best_meals)):

    meal = best_meals[i]

    print("\nMeal", i + 1)

    #display selected food items
    for food in meal["foods"]:
        print(food)

    #display nutritional information and cost
    print("Cost: $", round(meal["cost"], 2))
    print("Calories:", round(meal["calories"], 2))
    print("Fat:", round(meal["fat"], 2), "grams")
    print("Carbohydrates:", round(meal["carbs"], 2), "grams")
    print("Protein:", round(meal["protein"], 2), "grams")
    print("Score:", round(meal["score"], 6))

#display execution time
print("\nExecution time:", execution_time, "seconds")