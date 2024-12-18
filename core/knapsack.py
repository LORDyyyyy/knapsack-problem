from collections import namedtuple
from typing import List

Item = namedtuple("Item", ["weight", "value"])


class Knapsack:
    n = 0
    maximum_capacity = 0
    available_items: List[Item] = []

    def __init__(self, selected_items):
        self._weight = 0
        self._value = 0
        self.selected_items = selected_items[:]

        self._calculate_weights()

    def _calculate_weights(self):
        """Calculate total weight of selected items in the knapsack"""

        for i, take in enumerate(self.selected_items):
            self._weight += Knapsack.available_items[i].weight * take
            self._value += Knapsack.available_items[i].value * take

    def change_quantity(self, index: int, quantity: int = -1):
        """Change how much should I take an item"""

        if index < 0 or quantity < 0 or index >= Knapsack.n:
            return

        if quantity == -1:
            quantity = not self.selected_items[index]

        item = Knapsack.available_items[index]
        difference = quantity - self.selected_items[index]

        self._weight += item.weight * difference
        self._value += item.value * difference
        self.selected_items[index] = quantity

    def get_weight(self):
        """Get total weight"""

        return self._weight

    def get_value(self):
        """Get total value"""

        return self._value

    @staticmethod
    def add_item(value: int, weight: int):
        """Add new item to available items"""

        Knapsack.available_items.append(Item(weight=weight, value=value))
        Knapsack.n += 1

    def __repr__(self) -> str:
        """How the knapsack object should be printed"""

        result: str = f"Weight: {self._weight}\nValue: {
            self._value}\nTaken items: "
        for i, take in enumerate(self.selected_items):
            if take > 1:
                result += f"{i + 1}({self.selected_items[i]}) "
            elif take:
                result += f"{i + 1} "

        return result.strip()
