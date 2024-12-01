import matplotlib.pyplot as plt
from knapsack import Knapsack
from genetic import Genetic, UnboundedGenetic


print("1. 1-0 Knapsack\n2. Unbounded Knapsack")
choice = int(input("\\> "))
genetic = Genetic()

if choice == 2:
    genetic = UnboundedGenetic()

n, Knapsack.maximum_capacity = map(int, input().split())

for _ in range(n):
    weight, value = map(int, input().split())
    Knapsack.add_item(weight=weight, value=value)


knapsack, y = genetic.evolution(lim=500)
print(knapsack)

x = list(range(len(y)))
plt.scatter(x, y)
plt.show()
