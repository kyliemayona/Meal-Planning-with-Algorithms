import time
import csv
from pathlib import Path
import random
from contextlib import redirect_stdout

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
   return -score

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

def mutate(chromosome, mutation_rate=0.05): # Mutate a chromosome based on the mutation rate
   mutated = chromosome.copy() # Create a copy of the chromosome to mutate
   for i in range(len(mutated)):
      if random.random() < mutation_rate: # Randomly decide whether to mutate each gene
         mutated[i] = 1 - mutated[i] # Flip the gene (0 becomes 1 or 1 becomes 0)
   return mutated
 
def main():
   start_time = time.time() # Start the timer for performance measurement
   foods = load_foods()
   population = [create_chromosome(len(foods)) for _ in range(50)] # Create initial population of 50 random meal plans

   # Store every unique valid meal found
   best_meals = {}
   best_ever = None
   best_ever_fitness = float("-inf")

   # Repeat genetic algorithm for 200 generations
   for generation in range(201):
      # Find the best chromosome in the current population
      generation_best = None
      generation_fitness = float("-inf")

      # Compare the fitness of the remaining chromosomes in the population
      for chromosome in population:
         meal = evaluate_meal(chromosome, foods)
         if not meal["valid"]:
            continue  # Skip invalid meals

         fitness = calculate_fitness(meal, foods)
         chromosome_key = tuple(chromosome)  # Use the chromosome as a key for uniqueness
         if chromosome_key not in best_meals:
            best_meals[chromosome_key] = fitness

         # Save the best chromosome of the current generation
         if fitness > generation_fitness:
            generation_best = chromosome
            generation_fitness = fitness

      if generation_best is None:
         print("No valid meals found.")
         break

      # Update the best ever chromosome if the current generation's best is better
      if generation_fitness > best_ever_fitness:
         best_ever = generation_best.copy()
         best_ever_fitness = generation_fitness
      
      # Show progress every 20 generations
      if generation % 20 == 0:
         print(f"Generation {generation}: Best Fitness = {generation_fitness:.4f}")
         print(f"Best Ever Fitness = {best_ever_fitness:.4f}")

      # Stop after 200 generations
      if generation == 200:
         break

      # Start the next population with the best chromosome
      new_population = [best_ever.copy()]

      # Generate children until 50 meals in population
      while len(new_population) < 50:
         parent1 = tournament_selection(population, foods)
         parent2 = tournament_selection(population, foods)

         child1, child2 = crossover(parent1, parent2)

         child1 = mutate(child1)
         child2 = mutate(child2)

         new_population.append(child1)
         if len(new_population) < 50:  # Ensure we don't exceed the population size
            new_population.append(child2)

      population = new_population # Replace old population with new population

   sorted_meals = sorted(
      best_meals.items(),
      key=lambda item: item[1],
      reverse=True
   )

   # Print the top 8 meals found
   top_8_meals = sorted_meals[:8]

   print(f"\nTotal unique valid meals found: {len(best_meals)}")
   print("\nTop 8 Meals Found\n")

   # Print the details of the top 8 meals
   for number, (chromosome, fitness) in enumerate(top_8_meals, start=1):
      meal = evaluate_meal(list(chromosome), foods)
      print(f"Meal {number}")
      print(f"Chromosome: {list(chromosome)}")
      print(f"Selected Foods: {', '.join(meal['foods'])}")
      print(f"Cost: ${meal['cost']:.2f}")
      print(f"Calories: {meal['calories']:.0f} kcal")
      print(f"Fat: {meal['fat']:.1f} g")
      print(f"Protein: {meal['protein']:.1f} g")
      print(f"Carbs: {meal['carbs']:.1f} g")
      print(f"Fitness Score: {fitness:.4f}")

   end_time = time.time() # Stop the timer
   print(f"\nExecution Time: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
   results_folder = Path(__file__).resolve().parents[2] / "MainResults"
   results_file = results_folder / "genetic_main_results.txt"
   with open(results_file, "a", encoding="utf-8") as file:
      with redirect_stdout(file):
         print(f"\n\n--- Genetic Algorithm Meal Planning Results ---\n")
         main()
   print("Results saved to MainResults/genetic_main_results.txt")
   