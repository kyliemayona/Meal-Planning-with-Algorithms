- Kylie Maynard -

Meal Requirements: 
- Use the same CSV file as the brute-force and genetic algorithms.

- Each food item can either be selected or not selected.

- Each meal must contain at least 3 different food items.

- Cost: Minimize

- Calories: Target of 665

- Fat: Target of 20 grams

- Carbohydrates: Target of 65 grams

- Protein: Maximize

- Number of food items: At least 3

- Each category has equal importance.




My Idea for the MILP Algorithm:
- My Idea for the MILP Algorithm

- Read the 15 available food items from the CSV file.

- Store each food item's cost, calories, fat, carbohydrates, and protein.

- Assign a binary decision variable to each food item.

    - 0 means the food item is not selected.

    - 1 means the food item is selected.

- Create a constraint requiring at least 3 food items in each meal.

- Calculate the total cost and nutritional information for the selected food items.

- Calculate the absolute difference between the total calories and the target of 665 calories.

- Calculate the absolute difference between the total fat and the target of 20 grams.

- Calculate the absolute difference between the total carbohydrates and the target of 65 grams.

- Normalize each category so that differences in units do not give one category more importance than another.

- Create an objective function that minimizes cost and nutritional deviations while maximizing protein.

- Use an MILP solver to find the optimal meal combination.

- Exclude the previously selected combination and repeat the optimization process until the top 8 meals have been found.

- Display each meal's food items, total cost, calories, fat, carbohydrates, and protein.

- Record the execution time for comparison with the brute-force and genetic algorithms.

