# Optimizing Meal Planning

## Problem

The aim of our research is to analyze meal planning from an algorithmic perspective. It can be difficult to choose which combinations of food make the most economical and nutrition sense in everyday meal prep. Using a well-tuned algorithm can simplify and improve this process significantly.

Inputs in this algorithm will include:
- A list of available foods
- Cost per serving
- Nutritional information, including calories, protein, and carbs
- A nutritional goal that each meal needs to achieve
- A finite number of servings for each available food

Every solution must meet every individual nutritional goal in order to be valid. Solutions will be ranked by cost, with the lowest being the most optimal.

For example, suppose one serving of rice costs $0.50, contains 200 calories, 4 grams of protein, and 44 grams of carbs, and one serving of chicken costs $1.50, contains 150 calories, 27 grams of protein and 0 grams of carbs.

The meal would:
- Cost $2
- Contain 350 calories
- Contain 31 grams of protein
- Contain 44 grams of carbs

This meal would be compared against other combinations of foods to find the cheapest one which hits our nutritional goal.

Anyone who plans their meals or eats with a particular goal in mind can benefit from an algorithm optimizing the cost and nutritional facts of their meals.

## Why This Problem?

With meal planning being such a common issue people deal with daily, many stand to benefit from an algorithmic approach. The cheapest foods might not produce the cheapest nutritionally sufficient meal plan, so the results could be surprising.

The total number of combinations of foods for meals increases rapidly as more ingredients are considered, making efficiency very important. By using different algorithms, we will be able to compare their efficiency as well.

## Brute-Force Approach

A Brute-Force approach would check every possible combination of foods in order to find the lowest cost one.

The algorithm:
1. Calculates the total cost, calories, protein, and carbs.
2. Throws out combinations that do not meet nutritional requirements.
3. Compares the combinations that meet requirements to find the lowest cost.

If we assume each food can have 0 or 1 servings, the total number of combinations would be \(2^n\), where `n` represents the number of available foods.

As the number of foods becomes larger, the number of combinations would grow exponentially. For instance, 25 foods would make for over 33 million combinations.

Clearly, it would be impractical to find the best combination among hundreds of foods, as the amount of computing power needed would be immense.

An estimate of the time complexity would be `O(n x n^2)`.

## Proposed Third Algorithm: MILP (Mixed Integer Linear Programming)

### How the Algorithm Works

The MILP model uses decision variables, objective functions, and constraints written as linear equations to map out and solve real world problems. It uses branching to determine what the most promising options are.

It is appropriate for our problem because it treats the meal plan as a puzzle with boundaries, maps out the boundaries such as price, nutritional requirements, and structured meal slots.

It differs from brute force because brute force tests every single possibility to find the answer, while MILP uses geometric math and logic to eliminate millions of bad options simultaneously without ever looking at them.

## Research Question

How does the density of strict constraint boundaries affect the branching complexity and pruning efficiency of the Branch and Bound algorithm?

## Experimental Plan: Algorithm Comparison and Measurements

We plan to compare the brute-force, genetic, and MILP algorithms by testing how well they find the cheapest meal combinations while meeting all nutritional requirements.

To make the comparison fair, all three algorithms will use the same food data, serving limits, and nutritional goals.

We will measure:

- **Execution Time:** To see how quickly each algorithm finds a solution, as well as how the time changes as the number of available foods increases.
- **Solution Cost:** To determine whether the algorithms find the same or similar results.
- **Valid Solutions:** How often each algorithm finds a valid solution that meets every nutritional requirement.

Since brute force can check every possible combination, it can serve as a way to find the optimal solution for smaller test cases. We can then use that result to measure how close the genetic and MILP algorithms come to the optimal cost.

For the genetic algorithm, we will record the number of generations needed and run multiple trials using the same inputs because its results can vary due to randomness. We can compare the average execution time and solution cost across these trials to see how consistent its performance is.

For MILP, we will examine its execution time and, if available, the number of branching nodes or other solver statistics to better understand its performance. We may also track memory usage if it is practical to measure.

Finally, we will test different input sizes by increasing the number of available foods while keeping the nutritional requirements consistent within each test case.

We expect brute force to become much slower as the number of possible combinations grows, while the genetic and MILP algorithms may handle larger problems more efficiently.

By comparing execution time, solution quality, success rate, and performance as the problem grows, we hope to determine which algorithm is most effective for optimizing meal planning.

## Expected Challenges

As of right now, we believe that our biggest challenge will be time. Good time management is important because if we do not have time to implement, our ideas do not matter.

Each person on our team has a very busy schedule, and our schedules do not align with one another. We have also never worked on a project together, although we do all have experience working with new people.

Another challenge we expect to face is having to make sure that each algorithm follows the same requirements so that our results can be compared fairly. This is important so we can have more accurate information.

We may also encounter difficulties finding the right balance between factors such as meal cost, nutritional value, and variety, depending on what we decide to prioritize in our meal plan. Finding a good balance is important because we want to aim for both healthy and cheap food.

## Sources

Our team will use credible educational resources and academic research papers to ensure that our work is based on reliable information.

There is a lot of existing research and documentation about these different algorithms, and we want to take advantage of these resources to better understand how they work, and how they could be applied to our chosen problem of optimizing meal planning.

We will use Seljak's research article, *Computer-based dietary menu planning*, to learn how evolutionary algorithms can generate meal plans while considering multiple requirements. This research will help us understand how meal planning can be treated as an optimization problem, without examining every possible option.

We also plan on using the article *A Review on Genetic Algorithms: Past, Present, and Future* to understand how genetic algorithms work, including selection, crossover, and mutation, as well as their advantages and limitations.

A research article named *Manageability Challenges for Knowledge Incorporation in Genetic Algorithms: A Study Using the Meal Planning Problem* will help us understand some of the challenges involved in applying genetic algorithms specifically to meal planning.

### Research Articles

- [Computer-based dietary menu planning - ScienceDirect](https://www.sciencedirect.com/)
- [A Review on Genetic Algorithms: Past, Present, and Future - PMC](https://pmc.ncbi.nlm.nih.gov/)
- [Manageability Challenges for Knowledge Incorporation in Genetic Algorithms: A Study Using the Meal Planning Problem - EUDL](https://eudl.eu/)

## Group Expectations

With 3 people in this group, it is ideal for the workload to be split up into 3 equal sections.

In a perfect world, one of us could implement a brute force algorithm, one of us could implement a genetic algorithm, and one of us could implement a MILP algorithm. We think this will be our primary approach, but of course some algorithms may be harder to implement than others, so we also expect to help each other out.

We are all on a group chat together because good communication will be crucial to avoid conflict, and when conflict arises, we will simply speak our opinions in the group chat.

We will try to meet at least once a week in person and may have to join group calls on certain weeks.

We will stay aware of everything that our other group members are working on so that we become familiar with using all three algorithms, and especially so that we are prepared to help each other out and combine our thought processes together towards the end of the project.

Our team's final goal is to implement and compare the three algorithms to solve the same computational problem, and we will analyze factors like execution time, solution quality, and how each algorithm performs as the problem gets larger, to determine what type of algorithm is best for optimizing meal planning.