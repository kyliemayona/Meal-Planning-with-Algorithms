import csv
from pathlib import Path
import random

CSV_FILE = Path(__file__).resolve().parents[2] / "meal_planning_15_foods.csv" # Locate CSV file in project directory

def load_foods():
   foods = []
   with open(CSV_FILE, newline = "", encoding = "utf-8") as file:
      reader = csv.DictReader(file)
      for row in reader:
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

def evaluate_meal(foods):
   selected = []
   cost = calories = fat = protein = carbs = 0.0

   for i in range(len(foods)):
      if [i] == 1:
         food = foods[i]
         selected.append(food["name"])
         cost += food["cost"]
         calories += food["calories"]
         fat += food["fat"]
         protein += food["protein"]
         carbs += food["carbs"]

   return {
      "foods": selected,
      "valid": len(selected) > 3, 
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
      print(f"Meal {number}: {chromosome}")
      print(f"Selected: {', '.join(meal['foods'])}")
      print(f"Valid: {meal['valid']}")
      print(f"Cost: ${meal['cost']:.2f}")
      print(f"Calories: {meal['calories']:.0f}")
      print(f"Fat: {meal['fat']:.1f}g")
      print(f"Protein: {meal['protein']:.1f}g")
      print(f"Carbs: {meal['carbs']:.1f}g\n")

if __name__ == "__main__":
   main()
