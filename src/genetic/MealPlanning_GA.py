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

def calculate_fitness(meal, foods):
   # Meal must be valid (at least 3 foods selected) 
   if not meal["valid"]:
      return float("-inf")

   # Calculate the maximum possible cost and protein based on the available foods
   max_cost = sum(food["cost"] for food in foods)
   max_protein = sum(food["protein"] for food in foods)

   # Calculate the maximum deviation for calories, fat, and carbs based on the target values
   max_calorie_deviation = max(665, sum(food["calories"] for food in foods) - 665)
   max_fat_deviation = max(20, sum(food["fat"] for food in foods) - 20)
   max_carb_deviation = max(65, sum(food["carbs"] for food in foods) - 65)

   # Calculate normalized scores
   cost_score = meal["cost"] / max_cost
   calorie_score = abs(meal["calories"] - 665) / max_calorie_deviation
   fat_score = abs(meal["fat"] - 20) / max_fat_deviation
   carb_score = abs(meal["carbs"] - 65) / max_carb_deviation
   protein_score = 1 - (meal["protein"] / max_protein)

   weight = 0.20 # Each category receives equal weight in the fitness calculation

   score = weight * (cost_score + calorie_score + fat_score + carb_score + protein_score)
   return score

def tournament_selection(population, foods): # Select parent chromosome using tournament selection
   competitors = random.sample(population, 3) # Randomly select 3 competitors from the population
   best_chromosome = competitors[0]  # Assume the first competitor is the best initially
   best_meal = evaluate_meal(best_chromosome, foods)
   best_fitness = calculate_fitness(best_meal, foods)
   # Compare the fitness of the remaining competitors to find the best one
   for cromosome in competitors[1:]:
      meal = evaluate_meal(cromosome, foods)
      fitness = calculate_fitness(meal, foods)
      if fitness > best_fitness:
         best_chromosome = cromosome
         best_fitness = fitness
   return best_chromosome.copy() # Return a copy of the best chromosome   

def crossover(parent1, parent2): # Perform single-point crossover between two parent chromosomes
   point = random.randint(1, len(parent1) - 1) # Randomly select a crossover point
   child1 = parent1[:point] + parent2[point:] # Create first child by combining segments from both parents
   child2 = parent2[:point] + parent1[point:] # Create second child by combining segments from both parents
   return child1, child2 # Return the two new child chromosomes

def main():
   foods = load_foods()
   population = [create_chromosome(len(foods)) for _ in range(50)] # Create initial population of 50 random meal plans

   print(f"Loaded {len(foods)} foods and generated {len(population)} meals.\n")

   for number, chromosome in enumerate(population[:3], start=1):
      meal = evaluate_meal(chromosome, foods)
      fitness = calculate_fitness(meal, foods)

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
      print(f"Fitness Score: {fitness:.3f}\n")
   
   print("Tournament Selection\n")

   # Select two parents using tournament selection
   parent1 = tournament_selection(population, foods)
   parent2 = tournament_selection(population, foods)

   meal1 = evaluate_meal(parent1, foods)
   meal2 = evaluate_meal(parent2, foods)

   fitness1 = calculate_fitness(meal1, foods)
   fitness2 = calculate_fitness(meal2, foods)

   # Display results of the tournament selection
   print(f"Parent 1: {parent1}")
   print(f"Selected Foods: {', '.join(meal1['foods'])}")
   print(f"Fitness Score: {fitness1:.3f}\n")

   print(f"Parent 2: {parent2}")
   print(f"Selected Foods: {', '.join(meal2['foods'])}")
   print(f"Fitness Score: {fitness2:.3f}\n")


   print("\nCrossover\n") # Peform crossover using the two selected parents

   child1, child2 = crossover(parent1, parent2)
   child_meal1 = evaluate_meal(child1, foods)
   child_meal2 = evaluate_meal(child2, foods)

   child_fitness1 = calculate_fitness(child_meal1, foods)
   child_fitness2 = calculate_fitness(child_meal2, foods)

   print(f"Child 1: {child1}")
   print(f"Selected Foods: {', '.join(child_meal1['foods'])}")
   print(f"Valid: {child_meal1['valid']}")
   print(f"Fitness Score: {child_fitness1:.4f}\n")

   print(f"Child 2: {child2}")
   print(f"Selected Foods: {', '.join(child_meal2['foods'])}")
   print(f"Valid: {child_meal2['valid']}")
   print(f"Fitness Score: {child_fitness2:.4f}\n")

if __name__ == "__main__":
   main()
