

#import libraries
import csv
import pulp#creates the milp model, decision variables, constraints, and objective function
from pathlib import Path#locates the csv file within your repository.
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
with open(csv_file, "r") as file:
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
#create the milp model.
model = pulp.LpProblem("Meal_Optimization", pulp.LpMinimize)
#create binary decision variables
#0 means the food is not selected 1 means it ids
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

#display expressions for testing
print("Cost:", total_cost)
print("Calories:", total_calories)
print("Fat:", total_fat)
print("Carbohydrates:", total_carbs)
print("Protein:", total_protein)
