import numpy as np 
import pickle
import copy
import random

class GeneticModels:
    def __init__(self, population_size, mutation_rate, crossover_rate, mutate_val_rate, gaussian_const, chromosome_form):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.mutate_val_rate = mutate_val_rate
        self.chromosome_form = chromosome_form
        self.gaussian_const = gaussian_const
        self.best_model = None
        self.fitness_array = None

    #Funciona

    def init_population(self) -> list:
        population = []
        for i in range(self.population_size):
            population.append(self.rand_init())
        return population

    #Funciona

    def select_parents(self, population, list_of_values):
        sum_values = sum(list_of_values)
        if sum_values != 0:
            list_of_values = [x/sum_values for x in list_of_values]
            parents = random.choices(population, weights=list_of_values, k=self.population_size)
        else: 
            parents = random.choices(population, k=self.population_size)

        return parents
     
    # Funciona
    def crossover_population(self, parents):
        for i in range(0, len(parents), 2):
            if np.random.rand() < self.crossover_rate:
                parents[i], parents[i+1] = self.crossover(parents[i], parents[i+1])
            
    # Funciona
    def crossover(self, parent1, parent2):
        # Inicializar los hijos con la misma estructura que los padres
        child1 = [np.zeros_like(layer) for layer in parent1]
        child2 = [np.zeros_like(layer) for layer in parent2]
        
        # Recorrer cada tensor (capa) de los padres
        for i in range(len(parent1)):
            for j in range(len(parent1[i])):
                for k in range(len(parent1[i][j])):
                    # Decidir aleatoriamente si el gen viene de parent1 o parent2
                    if np.random.rand() < 0.5:
                        child1[i][j][k] = parent1[i][j][k]
                        child2[i][j][k] = parent2[i][j][k]
                    else:
                        child1[i][j][k] = parent2[i][j][k]
                        child2[i][j][k] = parent1[i][j][k]
        
        return child1, child2

    #Funciona
    def mutate_population(self, population):
        for i in range(len(population)):
            if np.random.rand() < self.mutation_rate:
                population[i] = self.mutate(population[i])

    # Funciona
    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            for j in range(len(chromosome[i])):
                for k in range(len(chromosome[i][j])):
                    if np.random.rand() < self.mutate_val_rate:
                        chromosome[i][j][k] += self.gaussian_const*np.random.standard_normal()

        return chromosome

    # Funciona
    def next_generation(self, current_gen, fitness_array):
        parents = self.select_parents(current_gen, fitness_array)
        self.crossover_population(parents)
        self.mutate_population(parents)
        return parents
        
    
    #Funciona
    def rand_init(self) -> np.array:
        tensor = []

        for i, j in self.chromosome_form:
            tensor.append(np.random.uniform(low=-1, high=1, size=(i, j)))
        
        return tensor

    def load(self, path):
        with open(path, 'rb') as f:
            self.best_model = pickle.load(f)

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.best_model, f)

    def compare_tensors(self, tensor1, tensor2):
        return all(np.array_equal(layer1, layer2) for layer1, layer2 in zip(tensor1, tensor2))


#generator = GeneticModels(10, 0.1, 0.9, 0.07,0.5 [(21, 8), (16, 8), (16, 1)])

#tensor1 = generator.rand_init()
#tensor2 = generator.rand_init()

#generator.best_model = tensor1

#generator.save("model.txt")
#generator.load("model.txt")

#print(generator.compare_tensors(tensor1, generator.best_model))

#vals = [10,30]




