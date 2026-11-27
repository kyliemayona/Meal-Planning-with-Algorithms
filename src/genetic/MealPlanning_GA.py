import csv
from pathlib import Path
import random

CSV_FILE = Path(__file__).resolve().parents[2] / "meal_planning_15_foods.csv" # Locate CSV file in project directory

def load_foods():
   foods = []
   # Open the CSV file and read each row into a dictionary
   with open(CSV_FILE, newline = "", encoding = "utf-8") as file:
      reader = csv.DictReader(file)
      for row in reader:
         # Convert numeric values to floats 
         foods.append({
            "name": row["food"],
            "cost": float(row["cost_usd"]),
            "calories": float(row["calories"]),
            "fat": float(row["fat_g"]),
            "protein": float(row["protein_g"]),
            "carbs": float(row["carbs_g"])
            })
   return foods

def create_chromosome(food_count): # Generate one random meal chromosome
   return [random.randint(0, 1) for _ in range(food_count)] 

# Evaluate one meal based on the foods selected in its chromosome
def evaluate_meal(chromosome, foods):
   selected = []
   cost = calories = fat = protein = carbs = 0.0 # Initialize totals

   for i in range(len(foods)):
      if chromosome[i] == 1:
         food = foods[i]
         selected.append(food["name"])
         cost += food["cost"]
         calories += food["calories"]
         fat += food["fat"]
         protein += food["protein"]
         carbs += food["carbs"]

# Return a dictionary with the meal's details, including whether it is valid (at least 3 foods selected)
   return {
      "foods": selected,
      "valid": len(selected) >= 3, 
      "cost": cost,
      "calories": calories,
      "fat": fat,
      "protein": protein,
      "carbs": carbs
   }

def main():
   foods = load_foods()
   population = [create_chromosome(len(foods)) for _ in range(50)] # Create initial population of 50 random meal plans

   print(f"Loaded {len(foods)} foods and generated {len(population)} meals.\n")

   for number, chromosome in enumerate(population[:3], start=1):
      meal = evaluate_meal(chromosome, foods)
      # Display the chromosome, selected foods, and whether the meal is valid
      print(f"Meal {number}: {chromosome}")
      print(f"Selected: {', '.join(meal['foods'])}")
      print(f"Valid: {meal['valid']}")
      # Display the nutritional information and cost of the meal
      print(f"Cost: ${meal['cost']:.2f}")
      print(f"Calories: {meal['calories']:.0f}")
      print(f"Fat: {meal['fat']:.1f}g")
      print(f"Protein: {meal['protein']:.1f}g")
      print(f"Carbs: {meal['carbs']:.1f}g\n")

if __name__ == "__main__":
   main()
