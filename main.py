
import json
import os
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Save expenses in a file beside this Python file.
DATA_FILE = Path(__file__).resolve().parent / "expenses.json"
TEMP_FILE = DATA_FILE.with_suffix(".tmp")

CATEGORIES = [
    "Food",
    "Transport",
    "School",
    "Shopping",
    "Entertainment",
    "Other",
]


def load_expenses():
    """Load saved expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses, list):
            raise ValueError("Saved data must be a list.")

        for item in expenses:
            if not isinstance(item, dict):
                raise ValueError("Invalid expense entry.")

            for key in ("amount", "date", "category", "description"):
                if not isinstance(item.get(key), str):
                    raise ValueError("An expense is missing a valid field.")

            try:
                amount = Decimal(item["amount"])
                entry_date = date.fromisoformat(item["date"])
            except (InvalidOperation, ValueError):
                raise ValueError("An expense has an invalid amount or date.")

            if not amount.is_finite() or amount <= 0:
                raise ValueError("An expense amount must be positive.")

            if amount.as_tuple().exponent < -2:
                raise ValueError("An expense has too many decimal places.")

            if entry_date.isoformat() != item["date"]:
                raise ValueError("An expense date has an invalid format.")

            if item["category"] not in CATEGORIES:
                raise ValueError("An expense has an invalid category.")

            if not item["description"].strip():
                raise ValueError("An expense has an empty description.")

        return expenses

    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(
            f"Could not safely read {DATA_FILE.name}: {error}. "
            "Check the file before restarting."
        ) from error


def save_expenses(expenses):
    """Save expenses safely using a temporary file."""
    try:
        with TEMP_FILE.open("w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=2)
            file.write("\n")

        os.replace(TEMP_FILE, DATA_FILE)
        return True

    except OSError as error:
        print(f"Could not save expenses: {error}")
        try:
            TEMP_FILE.unlink(missing_ok=True)
        except OSError:
            pass
        return False


def ask_amount():
    """Ask for a positive amount with up to two decimal places."""
    while True:
        try:
            amount = Decimal(input("Amount in SGD: ").strip())
        except InvalidOperation:
            print("Invalid amount. Example: 4.50")
            continue

        if not amount.is_finite() or amount <= 0:
            print("Amount must be greater than zero.")
            continue

        if amount.as_tuple().exponent < -2:
            print("Use no more than two decimal places.")
            continue

        return amount


def ask_date():
    """Ask for a date, defaulting to today."""
    while True:
        raw = input(
            f"Date (YYYY-MM-DD, Enter for {date.today()}): "
        ).strip()

        if not raw:
            return date.today().isoformat()

        try:
            parsed = date.fromisoformat(raw)
        except ValueError:
            print("Invalid date. Example: 2026-10-28")
            continue

        if parsed.isoformat() != raw:
            print("Use YYYY-MM-DD format.")
            continue

        if parsed > date.today():
            print("Date cannot be in the future.")
            continue

        return raw


def add_expense(expenses):
    print("\n--- Add Expense ---")

    amount = ask_amount()
    expense_date = ask_date()

    print("\nChoose a category:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            choice = int(input("Category number: ").strip())
        except ValueError:
            print("Enter a number from 1 to 6.")
            continue

        if 1 <= choice <= len(CATEGORIES):
            category = CATEGORIES[choice - 1]
            break

        print("Choose a number from 1 to 6.")

    while True:
        description = input("Description: ").strip()
        if 1 <= len(description) <= 100:
            break
        print("Description must contain 1 to 100 characters.")

    new_expense = {
        "amount": format(amount, ".2f"),
        "date": expense_date,
        "category": category,
        "description": description,
    }

    updated_expenses = expenses + [new_expense]

    if save_expenses(updated_expenses):
        expenses.append(new_expense)
        print("Expense saved successfully!")


def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    for item in sorted(
        expenses, key=lambda expense: expense["date"], reverse=True
    ):
        print(
            f"{item['date']} | {item['category']} | "
            f"SGD {Decimal(item['amount']):.2f} | "
            f"{item['description']}"
        )


def show_summary(expenses):
    print("\n--- Spending Summary ---")

    if not expenses:
        print("No expenses to summarise yet.")
        return

    total = sum(
        (Decimal(item["amount"]) for item in expenses),
        Decimal("0.00"),
    )

    print(f"Total spending: SGD {total:.2f}")

    category_totals = {}

    for item in expenses:
        category = item["category"]
        amount = Decimal(item["amount"])

        category_totals[category] = (
            category_totals.get(category, Decimal("0.00")) + amount
        )

    print("\nSpending by category:")

    for category, amount in sorted(category_totals.items()):
        print(f"{category}: SGD {amount:.2f}")


def main():
    try:
        expenses = load_expenses()
    except RuntimeError as error:
        print(f"\nData error: {error}")
        print("The app will close to protect your saved data.")
        return

    print("Welcome to your Expense Tracker!")

    while True:
        print("\n========== MENU ==========")
        print("1. Add an expense")
        print("2. View all expenses")
        print("3. View spending summary")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nApplication closed.")
