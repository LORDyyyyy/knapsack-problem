import matplotlib
import matplotlib.pyplot as plt
from core import Knapsack
from core import Genetic, UnboundedGenetic

matplotlib.use("TkAgg")


def start():
    print("1. 1-0 Knapsack\n2. Unbounded Knapsack")

    choice = int(input("\\> "))
    genetic = Genetic()

    if choice == 2:
        genetic = UnboundedGenetic()

    n, Knapsack.maximum_capacity = map(
        int, input(f"Number of Items and Max Capacity: ").split()
    )

    for i in range(n):
        weight, value = map(int, input(f"Weight and Value #{i + 1}: ").split())
        Knapsack.add_item(weight=weight, value=value)

    for knapsack, y in genetic.evolution(lim=500):
        print(knapsack)

    x = list(range(len(y)))
    plt.scatter(x, y)
    plt.show()
