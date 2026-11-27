Import necessary libraries

Read food data from the CSV file

Store each food item's:
    Name
    Cost
    Calories
    Fat
    Carbohydrates
    Protein

Set meal requirements:
    Target calories = 665
    Target fat = 20 grams
    Target carbohydrates = 65 grams
    Minimum food items = 3
    Number of meals to find = 8

Initialize MILP minimization problem

FOR each food item:
    Create a binary decision variable
    0 = Food is not selected
    1 = Food is selected
END FOR

Create constraint:
    Total number of selected foods >= 3

Define expressions for:
    Total cost
    Total calories
    Total fat
    Total carbohydrates
    Total protein

Create nonnegative deviation variables for:
    Calorie deviation
    Fat deviation
    Carbohydrate deviation

Add constraints to represent absolute differences
between nutritional totals and their target values

Determine normalization factors for each category

Create objective function:
    Minimize normalized cost
    Minimize normalized calorie deviation
    Minimize normalized fat deviation
    Minimize normalized carbohydrate deviation
    Maximize normalized protein

Give all five categories equal weight

Create an empty list to store the best meals

Start execution timer

FOR meal number = 1 through 8:

    Solve MILP problem

    IF an optimal solution is found:

        Identify selected food items

        Calculate total cost and nutritional values

        Calculate overall objective score

        Store meal information in the list

        Add a constraint excluding this exact
        food combination from future solutions

    ELSE:

        Report solver status
        Exit loop

    END IF

END FOR

Stop execution timer

Display each meal:
    Meal ranking
    Selected food items
    Total cost
    Total calories
    Total fat
    Total carbohydrates
    Total protein
    Objective score

Display total execution time