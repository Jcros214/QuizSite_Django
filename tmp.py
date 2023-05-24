import random
from deap import base, creator, tools

# Problem parameters
teams = list(range(18))
rounds = 12
rooms = 7
n_genes = rounds * rooms
pop_size = 100
n_generations = 100

# Fitness function
def eval_schedule(schedule):
    score = 0
    # Check each constraint and increment score for each violation
    # Add your constraint checks here
    # ...
    return score,

# Crossover function
def cx_schedule(ind1, ind2):
    size = len(ind1)
    cxpoint1 = random.randint(1, size)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else: 
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2].copy(), ind1[cxpoint1:cxpoint2].copy()
    return ind1, ind2

# Mutation function
def mut_schedule(schedule):
    # Choose a random gene and mutate it
    gene_idx = random.randint(0, len(schedule) - 1)
    schedule[gene_idx] = create_gene()
    return schedule,

# Function to create a new gene (match)
def create_gene():
    return random.sample(teams, 3)  # Returns 3 random teams

# Create the DEAP tools for the GA
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))  # Maximizing problem
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("individual", tools.initRepeat, creator.Individual, create_gene, n=n_genes)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", eval_schedule)
toolbox.register("mate", cx_schedule)
toolbox.register("mutate", mut_schedule)
toolbox.register("select", tools.selTournament, tournsize=3)

# Initialize population
pop = toolbox.population(n=pop_size)

# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses): # type: ignore
    ind.fitness.values = fit

for g in range(n_generations):
    # Select the next generation individuals
    offspring = toolbox.select(pop, len(pop))
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation
    for child1, child2 in zip(offspring[::2], offspring[1::2]): #type: ignore
        if random.random() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses): #type: ignore
        ind.fitness.values = fit

    # Replace population
    pop[:] = offspring
