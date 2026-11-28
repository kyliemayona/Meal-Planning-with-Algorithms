# Meal Planning Optimization
# Makefile for running our three algorithms
PYTHON = python3

.PHONY: help genetic brute milp all

help:
	@echo "Available commands:"
	@echo "make genetic - Run Genetic Algorithm"
	@echo "make brute - Run Brute Force Algorithm"
	@echo "make milp - Run MILP Algorithm"
	@echo "make all - Run all three algorithms"

# Run Genetic Algorithm
genetic:
	$(PYTHON) src/genetic/MealPlanning_GA.py

# Run Brute Force Algorithm
brute:
	$(PYTHON) src/brute_force/mealPlanning_BF.py

milp:
	$(PYTHON) src/milp/MealPlanning_MILP.py

all: brute genetic milp