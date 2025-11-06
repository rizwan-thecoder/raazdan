import csv
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Global list to store expenses
expenses = []

# Function to load expenses from CSV file
def load_expenses(filename='expenses.csv'):
    global expenses
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                row['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
                expenses.append(row)
    except FileNotFoundError:
        print("No previous expense file found. Starting fresh.")
    except Exception as e:
        print(f"Error loading expenses: {e}")

# Function to save expenses to CSV file
def save_expenses(filename='expenses.csv'):
    try:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['amount', 'category', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow({
                    'amount': expense['amount'],
                    'category': expense['category'],
                    'date': expense['date'].isoformat()
                })
        print("Expenses saved successfully.")
    except Exception as e:
        print(f"Error saving expenses: {e}")

# Function to add an expense
def add_expense():
    try:
        amount = float(input("Enter the expense amount: "))
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        category = input("Enter the category (e.g., Food, Transport): ").strip()
        if not category:
            raise ValueError("Category cannot be empty.")
        date_input = input("Enter the date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_input:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date_input, '%Y-%m-%d').date()
        expense = {'amount': amount, 'category': category, 'date': date}
        expenses.append(expense)
        print("Expense added successfully.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"Error adding expense: {e}")

# Function to view all expenses
def view_expenses():
    if not expenses:
        print("No expenses to display.")
        return
    print("All Expenses:")
    print(f"{'Category':<15} {'Amount':<10} {'Date':<12}")
    print("-" * 40)
    for expense in expenses:
        print(f"{expense['category']:<15} ${expense['amount']:<9.2f} {expense['date']}")

# Function to generate reports
def generate_report():
    if not expenses:
        print("No expenses to report.")
        return
    total_spent = sum(exp['amount'] for exp in expenses)
    print(f"Total Spent: ${total_spent:.2f}")
    
    # Spending by category
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp['category']] += exp['amount']
    print("\nSpending by Category:")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")
    
    # Highest expense
    highest = max(expenses, key=lambda x: x['amount'])
    print(f"\nHighest Expense: ${highest['amount']:.2f} in {highest['category']} on {highest['date']}")

# Function to visualize expenses
def visualize_expenses():
    if not expenses:
        print("No expenses to visualize.")
        return
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp['category']] += exp['amount']
    
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    
    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')
    plt.axis('equal')
    plt.show()

# Main menu
def main():
    load_expenses()
    while True:
        print("\nWelcome to Personal Expense Tracker!")
        print("1. Add an Expense")
        print("2. View All Expenses")
        print("3. Generate Report")
        print("4. Visualize Expenses")
        print("5. Save and Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            visualize_expenses()
        elif choice == '5':
            save_expenses()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
