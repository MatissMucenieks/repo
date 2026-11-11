import json
import os

DATA_FILE = "warehouse_inventory.json"

def load_inventory():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not read saved inventory, starting empty.")
    return {}


def save_inventory(inventory):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)


def read_name(prompt="Item name: "):
    return input(prompt).strip().lower()


def read_quantity(prompt, allow_zero=False):
    """Ask until the user enters a valid whole number."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value < 0 or (value == 0 and not allow_zero):
            print("Amount must be positive." if not allow_zero else "Amount cannot be negative.")
            continue
        return value


def add_item(inventory):
    name = read_name()
    if not name:
        print("Name cannot be empty.")
        return
    if name in inventory:
        print(f"'{name}' already exists. Use deposit to add more stock.")
        return
    quantity = read_quantity("Starting quantity: ", allow_zero=True)
    inventory[name] = quantity
    save_inventory(inventory)
    print(f"Added '{name}' with quantity {quantity}.")


def show_inventory(inventory):
    if not inventory:
        print("Inventory is empty.")
        return
    width = max(len(name) for name in inventory)
    width = max(width, 4)
    print(f"\n{'Item':<{width}}  Quantity")
    print("-" * (width + 10))
    for name in sorted(inventory):
        print(f"{name:<{width}}  {inventory[name]:>8}")
    print()


def deposit(inventory):
    name = read_name()
    if name not in inventory:
        print(f"'{name}' not found.")
        return
    amount = read_quantity("Amount to deposit: ")
    inventory[name] += amount
    save_inventory(inventory)
    print(f"Deposited {amount}. '{name}' now has {inventory[name]}.")


def withdraw(inventory):
    name = read_name()
    if name not in inventory:
        print(f"'{name}' not found.")
        return
    amount = read_quantity("Amount to withdraw: ")
    if amount > inventory[name]:
        print(f"Not enough stock. '{name}' only has {inventory[name]}.")
        return
    inventory[name] -= amount
    save_inventory(inventory)
    print(f"Withdrew {amount}. '{name}' now has {inventory[name]}.")


def delete_item(inventory):
    name = read_name()
    if name not in inventory:
        print(f"'{name}' not found.")
        return
    confirm = input(f"Delete '{name}' (quantity {inventory[name]})? [y/N]: ").strip().lower()
    if confirm == "y":
        del inventory[name]
        save_inventory(inventory)
        print(f"Deleted '{name}'.")
    else:
        print("Cancelled.")


MENU = """
=== Warehouse Management ===
1. Add new item
2. Show inventory
3. Deposit
4. Withdraw
5. Delete item
0. Exit
"""


def main():
    inventory = load_inventory()
    actions = {
        "1": add_item,
        "2": show_inventory,
        "3": deposit,
        "4": withdraw,
        "5": delete_item,
    }
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(inventory)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()