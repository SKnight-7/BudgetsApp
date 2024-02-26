import sys
import csv
import os
from datetime import datetime
from tabulate import tabulate
from pyfiglet import Figlet, FigletError
import cowsay


class BudgetCategory:
    """
    Represents a budget category with its associated attributes. BudgetCategory objects are expected to be created and modified
    either by reading in data from a CSV file or via user input. Since both of these methods provide data as strings,
    class attributes are correctly typed by the class setters to ensure consistency.

    Search order is used to prevent miscategorization. For example, 'animal hospital' should be mapped to Pet Care, not Medical,
    so pet care is searched first. Also, any outlets (such as 'grocery outlet') should be checked for other keywords
    before being mapped to shopping due to 'outlet', and 'amazon prime video' should be mapped to Entertainment due to 'video'
    before being mapped to Other Shopping due to 'amazon', so shopping should be searched last.

    Attributes:
        general_classification (str): The general classification of the budget category.
        budget_category (str): The name of the budget category.
        keywords (str): Keywords associated with the budget category, separated by '|'.
        option_num (str): The option number of the budget category.
        amt_budgeted (str): The amount budgeted for the category.
        search_order (str): The search order of the budget category.
    """

    def __init__(self, general_classification: str, budget_category: str, keywords: str, option_num: str, amt_budgeted: str, search_order: str):
        """
        Initializes a BudgetCategory object with the provided attributes.

        Args:
            general_classification (str): The general classification of the budget category.
            budget_category (str): The name of the budget category.
            keywords (str): Keywords associated with the budget category, separated by '|'.
            option_num (str): The option number of the budget category.
            amt_budgeted (str): The amount budgeted for the category.
            search_order (str): The search order of the budget category.
        """
        self.general_classification = general_classification
        self.budget_category = budget_category
        self.keywords = keywords
        self.option_num = option_num
        self.amt_budgeted = amt_budgeted
        self.search_order = search_order

    def __str__(self):
        """
        Returns a string representation of the BudgetCategory object's attributes as stored in memory.
        Keywords are stored in memory as a list, option number and search order as integers, and amount budgeted as a float.

        Returns:
            str: The string representation of the BudgetCategory object's attributes, labeled.
        """
        return f"General Classification: {self.general_classification}\nBudget Category: {self.budget_category}\nKeywords: {self.keywords}\nOption Number: {self.option_num}\nAmount Budgeted: {self.amt_budgeted}\nSearch Order: {self.search_order}"

    @property
    def keywords(self):
        """
        Getter method for the keywords attribute.

        Returns:
            list: The list of keywords associated with the budget category.
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords: str):
        """
        Setter method for the keywords attribute. Transforms a string of keywords separated by '|' into a list of keywords stored in memory.

        Args:
            keywords (str): The keywords to set for the budget category. Expects a list of keywords separated by '|'.

        Raises:
            ValueError: If the provided keywords are not a string.
        """
        if not isinstance(keywords, str):
            raise ValueError("Keywords must be entered as a string.")
        self._keywords = keywords.split('|')

    @property
    def option_num(self):
        """
        Getter method for the option_num attribute.

        Returns:
            int: The option number of the budget category.
        """
        return self._option_num

    @option_num.setter
    def option_num(self, option_num: str):
        """
        Setter method for the option_num attribute. Transforms a numerical string into an integer and ensures input is non-negative.

        Args:
            option_num (str): The option number to set for the budget category.

        Raises:
            ValueError: If the provided option number is negative or cannot be cast to an integer.
        """
        try:
            option_num = int(option_num)
            if option_num < 0:
                raise ValueError('Option number must be non-negative')
        except ValueError:
            raise ValueError('Option number must be an integer')
        self._option_num = option_num

    @property
    def amt_budgeted(self):
        """
        Getter method for the amt_budgeted attribute.

        Returns:
            float: The amount budgeted for the category.
        """
        return self._amt_budgeted

    @amt_budgeted.setter
    def amt_budgeted(self, amt_budgeted: str):
        """
        Setter method for the amt_budgeted attribute. Transforms a string to a float and ensures the input is non-negative.

        Args:
            amt_budgeted (str): The amount budgeted to set for the category.

        Raises:
            ValueError: If the provided amount is negative or cannot be cast to a float.
        """
        try:
            amt_budgeted = round(float(amt_budgeted), 2)
            if amt_budgeted < 0:
                raise ValueError('Budgeted amount must be non-negative')
        except ValueError:
            raise ValueError(
                'Must be a dollar amount without a currency symbol (ex: 25.75, not $25.75)')
        self._amt_budgeted = amt_budgeted

    @property
    def search_order(self):
        """
        Getter method for the search_order attribute.

        Returns:
            int: The search order of the budget category.
        """
        return self._search_order

    @search_order.setter
    def search_order(self, search_order: str):
        """
        Setter method for the search_order attribute. Transforms a numerical string into an integer and ensures input is non-negative.

        Args:
            search_order (str): The search order to set for the budget category.

        Raises:
            ValueError: If the provided search order is negative or cannot be cast to an integer.
        """
        try:
            search_order = int(search_order)
            if search_order < 0:
                raise ValueError('Search order must be non-negative')
        except ValueError:
            raise ValueError('Search order must be an integer')
        self._search_order = search_order


class Transaction:
    """
    Represents a financial transaction with its associated attributes. Transaction objects are expected to be created and modified
    either by reading in data from a CSV file or via user input. Since both of these methods provide data as strings,
    class attributes are correctly typed by the class setters to ensure consistency.

    Attributes:
        source_file (str): The source file of the transaction.
        transaction_num (str): The transaction number.
        transaction_date (str): The date of the transaction.
        amount (str): The amount of the transaction.
        description (str): The description of the transaction.
        category (str): The category of the transaction (default: 'Uncategorized').
    """

    def __init__(self, transaction_num: str, transaction_date: str, amount: str, description: str, category: str = 'Uncategorized', source_file: str = 'sample.csv'):
        """
        Initializes a Transaction object with the provided attributes.

        Args:
            transaction_num (str): The transaction number.
            transaction_date (str): The date of the transaction.
            amount (str): The amount of the transaction.
            description (str): The description of the transaction.
            category (str): The category of the transaction (default: 'Uncategorized').
            source_file (str): The name of the user-provided CSV file from which this transaction was uploaded (default: 'sample.csv').
        """
        self.source_file = source_file
        self.transaction_num = transaction_num
        self.transaction_date = transaction_date
        self.amount = amount
        self.description = description
        self.category = category

    def __str__(self):
        """
        Returns a string representation of the Transaction object's attributes as stored in memory.
        Transaction number is stored as an integer, transaction date as a datetime object, and amount as a float.

        Returns:
            str: The string representation of the Transaction object's attributes, labeled.
        """
        return f"Source: {self.source_file}\nTransaction Number: {self.transaction_num}\nDate: {self.transaction_date}\nAmount: {self.amount}\nDescription: {self.description}\nCategory: {self.category}"

    @property
    def source_file(self):
        """
        Getter method for the source_file attribute. This indicates the name of the user-uploaded CSV file from which the transaction data originally came.

        Returns:
            str: The source file of the transaction.
        """
        return self._source_file

    @source_file.setter
    def source_file(self, source_file: str):
        """
        Setter method for the source_file attribute.

        Args:
            source_file (str): The source file name to set for the transaction.

        Raises:
            ValueError: If the provided source file is not of type CSV.
        """
        if not source_file.endswith('.csv'):
            raise ValueError(f'Source files must be of type CSV')
        self._source_file = source_file

    @property
    def transaction_num(self):
        """
        Getter method for the transaction_num attribute.

        Returns:
            int: The transaction number.
        """
        return self._transaction_num

    @transaction_num.setter
    def transaction_num(self, transaction_num: str):
        """
        Setter method for the transaction_num attribute. Transforms a numerical string into an integer and ensures input is non-negative.

        Args:
            transaction_num (str): The transaction number to set.

        Raises:
            ValueError: If the provided transaction number is negative, or cannot be cast to an integer.
        """
        try:
            transaction_num = int(transaction_num)
            if transaction_num < 0:
                raise ValueError('Transaction number must be non-negative')
        except ValueError:
            raise ValueError('Transaction number must be an integer')
        self._transaction_num = transaction_num

    @property
    def transaction_date(self):
        """
        Getter method for the transaction_date attribute.

        Returns:
            datetime: The date of the transaction.
        """
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date: str):
        """
        Setter method for the transaction_date attribute. Transforms a string formatted as YYYY-MM-DD into a datetime object.

        Args:
            transaction_date (str): The transaction date to set.

        Raises:
            ValueError: If the provided transaction date is not a valid date.
        """
        try:
            transaction_date = datetime.strptime(transaction_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Must be a valid date')
        self._transaction_date = transaction_date

    @property
    def amount(self):
        """
        Getter method for the amount attribute.

        Returns:
            float: The amount of the transaction.
        """
        return self._amount

    @amount.setter
    def amount(self, amount: str):
        """
        Setter method for the amount attribute. Transforms a string to a float and ensures the input is non-negative.

        Args:
            amount (str): The amount to set for the transaction.

        Raises:
            ValueError: If the provided amount is negative or cannot be cast to a float.
        """
        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise ValueError(
                'Must be a dollar amount without a currency symbol (ex: 25.75, not $25.75)')
        self._amount = amount


class BudgetManager:
    """
    Manages budget categories and performs budget-related operations.

    Attributes:
        budgets_csv_file (str): The internally created and managed CSV file storing the budget data (default: 'current_budgets.csv').
        budget_categories (dict): Dictionary mapping budget categories to BudgetCategory objects.
        budget_menu (str): String representation of the budget menu display.
        income_by_category (dict): Dictionary mapping income categories to their respective totals.
        expenditures_by_category (dict): Dictionary mapping expenditure categories to their respective totals.
    """

    def __init__(self, budgets_csv_file: str = 'current_budgets.csv'):
        """
        Initializes a BudgetManager object and sets the name of the internally created and managed CSV file for storing budget data.

        Args:
            budgets_csv_file (str): The CSV file name for storing budget data (default: 'current_budgets.csv').
        """
        self.budgets_csv_file = budgets_csv_file

        # Dictionary with BudgetCategory objects as values, and their budget_category attribute as keys
        self.budget_categories = self.initialize_default_budget_categories()
        self.budget_menu = self.initialize_budget_menu() # String representation of menu display

        # Used to calculate expenditures by budget category
        self.income_by_category = {}
        self.expenditures_by_category = {'Uncategorized': 0}

        # Create two dictionaries with budget categories as keys and totals by budget category as values
        for category in self.budget_categories:
            if self.budget_categories[category].general_classification == 'Income':
                self.income_by_category[category] = 0
            else:
                self.expenditures_by_category[category] = 0

    def initialize_default_budget_categories(self):
        """
        Initializes the default budget categories. Takes a list of BudgetCategory objects,
        then makes those objects the values of the dictionary, with their own budget_category attributes as keys.

        Returns:
            dict: Dictionary mapping budget categories to BudgetCategory objects.
        """

        self.category_objects = [
            BudgetCategory('Income', 'Paycheck', 'payroll', '1', '0', '1'),
            BudgetCategory('Income', 'Other Income', 'cashout', '2', '0', '2'),
            BudgetCategory('Monthly Household Bills', 'Mortgage & Rent',
                           'apartments|mortgage', '3', '0', '3'),
            BudgetCategory('Monthly Household Bills', 'Utilities',
                           'utility|gas|electric|water|smud|pge', '4', '0', '4'),
            BudgetCategory('Monthly Household Bills', 'Phone',
                           'verizon|metropcs|mobile', '5', '0', '5'),
            BudgetCategory('Monthly Household Bills', 'Internet, Cable, Satellite',
                           'internet|comcast|xfinity|at&t|cable|satellite', '6', '0', '6'),
            BudgetCategory('Food & Dining', 'Groceries',
                           'safeway|kroger|aldi|publix|meijer|piggly|albertson|costco|trader joe|co-op|food|market|grocery', '7', '0', '7'),
            BudgetCategory('Food & Dining', 'Eating Out',
                           'mcdonald|starbuck|peets|chipotle|subway|panera|dunkin|taco|pizza|wings|burger|steak|coffee|yogurt', '8', '0', '8'),
            BudgetCategory('Travel & Transport', 'Car (Payment, Gas, Repair, Ride Share, Tolls, Parking)',
                           'dealership|auto|uber|lyft|toll|parking|shell|chevron|exxonmobil|bp|gas', '9', '0', '9'),
            BudgetCategory('Travel & Transport', 'Public Transit',
                           'transit| rt ', '10', '0', '10'),
            BudgetCategory('Travel & Transport', 'Trips & Travel',
                           'hotel|motel|airline', '11', '0', '14'),
            BudgetCategory('Health & Fitness', 'Medical',
                           'hospital|doctor|kaiser|medical|insurance|wellness|pharm|rx', '12', '0', '17'),
            BudgetCategory('Health & Fitness', 'Gym & Other Fitness',
                           'fitness|gym|pilates|dance|running', '13', '0', '13'),
            BudgetCategory('Financial', 'Pay Loans & Credit Cards',
                           'bank|loan|capital one|merrick|hsbc|american express|visa|mastercard|student ln|synchrony| cc ', '14', '0', '11'),
            BudgetCategory('Shopping', 'Home Improvement', 'lowe|home|hardware', '15', '0', '15'),
            BudgetCategory('Shopping', 'Other Shopping',
                           'amazon|amzn|ebay|macy|nordstrom|target|walmart|outlet|google', '16', '0', '999'),
            BudgetCategory('Other', 'Self Care',
                           'spa | hair|nail|salon|barber|massage|beauty', '17', '0', '17'),
            BudgetCategory('Other', 'Pet Care',
                           'chewy|animal|vet|kitty|cat |dog|hound|pup', '18', '0', '12'),
            BudgetCategory('Other', 'Laundry', 'csc', '19', '0', '19'),
            BudgetCategory('Other', 'Entertainment',
                           'netflix|hulu|disney|video|spotify|audible|cinemark|amc|theater|theatre|playstation|nintendo|xbox|steam|nexus mods|game|subscription|youtube|channel|television|tv',
                           '20', '0', '20'),
        ]
        return {category_obj.budget_category: category_obj for category_obj in self.category_objects}

    def initialize_budget_menu(self):
        """
        Initializes the budget menu display.

        Returns:
            str: String representation of the budget menu display.
        """
        budget_menu = "\nAVAILABLE CATEGORIES:\n\n"
        budget_menu += "\x1B[4mINCOME\x1B[0m             \x1B[4mMONTHLY HOUSEHOLD\x1B[0m      \x1B[4mFOOD & DINING\x1B[0m          \x1B[4mTRAVEL & TRANSPORT\x1B[0m\n"
        budget_menu += " 1: Paycheck        3: Mortgage & Rent     7: Groceries           9: Car (Payment, Gas, Repair,\n"
        budget_menu += " 2: Other Income    4: Utilities           8: Eating Out             Ride Share, Tolls, Parking)\n"
        budget_menu += "                    5: Phone                                     10: Public Transit\n"
        budget_menu += "                    6: Internet, Cable,                          11: Trips & Travel\n"
        budget_menu += "                       Satellite\n\n"
        budget_menu += "\x1B[4mHEALTH & FITNESS\x1B[0m   \x1B[4mFINANCIAL\x1B[0m              \x1B[4mSHOPPING\x1B[0m               \x1B[4mOTHER\x1B[0m\n"
        budget_menu += "12: Medical        14: Pay Loans &        15: Home Improvement   17: Self Care\n"
        budget_menu += "13: Gym & Other        Credit Cards       16: Other Shopping     18: Pet Care\n"
        budget_menu += "    Fitness                                                      19: Laundry\n"
        budget_menu += "                                                                 20: Entertainment"

        return budget_menu

    @property
    def budgets_csv_file(self):
        """
        Getter method for the budgets_csv_file attribute.

        Returns:
            str: The CSV file storing the budget data.
        """
        return self._budgets_csv_file

    @budgets_csv_file.setter
    def budgets_csv_file(self, budgets_csv_file: str):
        """
        Setter method for the budgets_csv_file attribute.

        Args:
            budgets_csv_file (str): The CSV file to set for storing the budget data.

        Raises:
            ValueError: If the provided file is not of type CSV.
        """
        if not budgets_csv_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._budgets_csv_file = budgets_csv_file

    @property
    def budget_categories(self):
        """
        Getter method for the budget_categories attribute.

        Returns:
            dict: Dictionary mapping budget categories to BudgetCategory objects.
        """
        return self._budget_categories

    @budget_categories.setter
    def budget_categories(self, budget_categories: dict):
        """
        Setter method for the budget_categories attribute.

        Args:
            budget_categories (dict): Dictionary mapping budget categories to BudgetCategory objects.

        Raises:
            TypeError: If the provided budget_categories is not a dictionary.
            ValueError: If any value in budget_categories is not a BudgetCategory instance.
        """
        if not isinstance(budget_categories, dict):
            raise TypeError("budget_categories must be a dictionary")
        if not all(isinstance(category, BudgetCategory) for category in budget_categories.values()):
            raise ValueError("All values in budget_categories must be BudgetCategory instances")
        self._budget_categories = budget_categories

    @property
    def expenditures_by_category(self):
        """
        Getter method for the expenditures_by_category attribute.

        Returns:
            dict: Dictionary mapping expenditure categories to their respective totals.
        """
        return self._expenditures_by_category

    @expenditures_by_category.setter
    def expenditures_by_category(self, expenditures_by_category):
        """
        Setter method for the expenditures_by_category attribute.

        Args:
            expenditures_by_category (dict): Dictionary mapping expenditure categories to their respective totals.

        Raises:
            TypeError: If the provided expenditures_by_category is not a dictionary.
            ValueError: If any key in expenditures_by_category is not a string or any value is not a number.
        """
        if not isinstance(expenditures_by_category, dict):
            raise TypeError("expenditures_by_category must be a dictionary")
        if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in expenditures_by_category.items()):
            raise ValueError(
                "All keys in expenditures_by_category must be strings and all values must be numbers")
        self._expenditures_by_category = expenditures_by_category

    @property
    def income_by_category(self):
        """
        Getter method for the income_by_category attribute.

        Returns:
            dict: Dictionary mapping income categories to their respective totals.
        """
        return self._income_by_category

    @income_by_category.setter
    def income_by_category(self, income_by_category):
        """
        Setter method for the income_by_category attribute.

        Args:
            income_by_category (dict): Dictionary mapping income categories to their respective totals.

        Raises:
            TypeError: If the provided income_by_category is not a dictionary.
            ValueError: If any key in income_by_category is not a string or any value is not a number.
        """
        if not isinstance(income_by_category, dict):
            raise TypeError("expenditures_by_category must be a dictionary")
        if not all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in income_by_category.items()):
            raise ValueError(
                "All keys in expenditures_by_category must be strings and all values must be numbers")
        self._income_by_category = income_by_category

    def __str__(self):
        """
        Returns a string representation of the BudgetManager object.
        Creates a list of strings consisting of available budget categories with their budgeted amounts
        Then joins the strings in the list into one string with the items displayed on their own lines.

        Returns:
            str: The string representation of the BudgetManager object that shows the name of the file used for
            storing budget data and the amounts budgeted by category.
        """
        categories_and_amounts = '\n'.join([f"{category}: ${obj.amt_budgeted}" for category, obj in self.budget_categories.items()])
        return f"Internal data storage file: {self.budgets_csv_file}\nCurrent budgets:\n{categories_and_amounts}"

    def get_stored_budgets(self):
        """
        Reads in the stored budget data from the CSV file.
        If the file doesn't exist, initializes it with default data.
        """
        if not os.path.exists(self.budgets_csv_file):
            self.update_stored_budgets()  # Initialize the file with default data
        else:
            with open(self.budgets_csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.budget_categories = {}  # Prepare to load categories from file
                for row in reader:
                    self.budget_categories[row['budget_category']] = BudgetCategory(
                        row['general_classification'],
                        row['budget_category'],
                        row['keywords'],
                        row['option_num'],
                        row['amt_budgeted'],
                        row['search_order'])

    def get_budget_category_to_update(self):
        """
        Prompts the user to enter the option number of the budget category to update or 'q' to exit.

        Returns:
            str: The selected budget category or 'q' if the user chooses to exit.
            None: If the user enters an invalid option number.
        """
        try:
            selection = input("Enter option number of selected budget category or 'q' to exit: ")
        except EOFError:
            sys.exit("Goodbye!")  # Assume EOFError indicates user wants to quit out of program
        if selection.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:
            for category in self.budget_categories.values():
                if int(selection) == category.option_num:
                    return category.budget_category
        except ValueError:
            return None

    def get_new_budget_amt(self, category):
        """
        Prompts the user to enter a new budget amount for the specified category or 'q' to choose a different category.

        Args:
            category (str): The budget category to update.

        Returns:
            float: The new budget amount entered by the user.
            'q': If the user chooses to quit out of the current menu.
            None: If the user enters an invalid budget amount.
        """
        proposed_budget_amount = input(
            f"Please enter a budget amount for {category} in the format #####.## or 'q' to choose a different category:\n")
        if proposed_budget_amount.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:  # Ensure amount is a number
            new_budget = round(float(proposed_budget_amount), 2)
        except (ValueError, TypeError):
            return None
        return new_budget

    def update_budget_amount(self):
        """
        Prompts the user to update the budget amount for a selected budget category.
        Displays the updated budgets with expenditures after the update.
        """
        while True:
            print(f"{self.budget_menu}\n\nPlease select a budget to update. To delete a budget, please update the budgeted amount to 0")
            # Gets the key in the self.budget_categories dictionary
            category_to_update = self.get_budget_category_to_update()
            if not category_to_update:
                # Let the user know their selection was invalid before reprompting
                print("Invalid option, please try again.")
                continue
            if category_to_update == 'q':
                return 'q'  # Lets calling function know user wants to quit out of budget menu
            while True:
                new_budget_amt = self.get_new_budget_amt(category_to_update)
                if not new_budget_amt:
                    print('Invalid entry')
                    continue  # Let user try entering the budget amount again, in case they just used the wrong format or miskeyed the input
                if new_budget_amt == 'q':   # If user enters 'q' instead of an amount, they may have meant to choose a different category
                    break
                if new_budget_amt < 0:  # Validate user input as positive or zero
                    print("Budget amount must be 0.00 or greater")
                    continue
                self.budget_categories[category_to_update].amt_budgeted = new_budget_amt
                self.update_stored_budgets()
                print(self.format_budgets_with_expenditures())
                break

    def update_stored_budgets(self):
        """
        Updates the stored budget data in the CSV file with the current budget data.
        Overwrites whatever was in the file with the data currently in memory.
        """
        with open(self.budgets_csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                                    'general_classification', 'budget_category', 'keywords', 'option_num', 'amt_budgeted', 'search_order'])
            writer.writeheader()
            for category_obj in self.budget_categories.values():
                writer.writerow({
                    'general_classification': category_obj.general_classification,
                    'budget_category': category_obj.budget_category,
                    'keywords': '|'.join(category_obj.keywords),
                    'option_num': str(category_obj.option_num),
                    'amt_budgeted': f"{category_obj.amt_budgeted:.2f}",
                    'search_order': str(category_obj.search_order)
                })

    def format_budgets_with_expenditures(self, transactions_source=None):
        """
        Formats the budgets with expenditures for display.

        Args:
            transactions_source (str): The filename from which this collection of transactions was originally uploaded by the user (default: None).

        Returns:
            str: The formatted string representing the budgets with expenditures.
        """
        # Initialize headers and lists for income and expenditures
        income_headers = ['Income Category', 'Expected', 'Received', 'Pending']
        expenditures_headers = ['Budget Category', 'Budgeted', 'Expended', 'Remaining']
        income_data, expenditures_data = [], []

        # Initialize totals
        total_expected_income, total_budgeted_expenses, total_received, total_expended = 0, 0, 0, 0

        # Process each budget category
        for category in self.budget_categories.values():
            if category.general_classification == 'Income':
                received = self.income_by_category.get(category.budget_category, 0)
                pending = category.amt_budgeted - received
                if category.amt_budgeted != 0 or received != 0:
                    total_expected_income += category.amt_budgeted
                    total_received += received
                    income_data.append(
                        [category.budget_category, category.amt_budgeted, received, pending])
            else:
                expended = self.expenditures_by_category.get(category.budget_category, 0)
                remaining = category.amt_budgeted - expended
                if category.amt_budgeted != 0 or expended != 0:
                    total_budgeted_expenses += category.amt_budgeted
                    total_expended += expended
                    expenditures_data.append(
                        [category.budget_category, category.amt_budgeted, expended, remaining])

        if not income_data and not expenditures_data:
            return "\nThere are no budgets to display.\n"

        # Calculate available to allocate and unspent balance
        available_to_allocate = total_expected_income - total_budgeted_expenses
        unspent_balance = total_budgeted_expenses - total_expended

        # Format the data for display using tabulate
        income_table = tabulate(income_data, headers=income_headers, tablefmt="grid", floatfmt=',.2f')
        expenditures_table = tabulate(expenditures_data, headers=expenditures_headers, tablefmt="grid", floatfmt=',.2f')

        # Build the display string
        header = f"\n\n\x1B[4mYOUR CURRENT BUDGETS\x1B[0m\nBased on transactions from: {transactions_source if transactions_source else 'N/A'}"

        income_section = f"{income_table}\nTotal Expected Income: ${total_expected_income:,.2f}\nTotal Received: ${total_received:,.2f}\nAvailable to allocate: ${available_to_allocate:,.2f}"
        expenditure_section = f"{expenditures_table}\nUncategorized: ${self.expenditures_by_category.get('Uncategorized', 0):,.2f}\n\nTotal Budgeted: ${total_budgeted_expenses:,.2f}\nTotal Expended: ${total_expended:,.2f}\nUnspent balance: ${unspent_balance:,.2f}"

        # Concatenate all the sections into the final display string
        return f"{header}\n\n{income_section}\n\n{expenditure_section}"

    def categorize_transaction(self, description):
        """
        Categorizes a transaction based on its description.

        Args:
            description (str): The description of the transaction.

        Returns:
            str: The category assigned to the transaction.
        """
        sorted_categories = sorted(self.budget_categories.values(), key=lambda x: x.search_order) # Sorted function returns a list
        for category in sorted_categories:
            for keyword in category.keywords:
                if keyword.lower() in description.lower():
                    return category.budget_category
        return 'Uncategorized'


class TransactionsManager:
    """
    Manages financial transactions and performs transaction-related operations.

    Attributes:
        source_file (str): The name of the user-provided CSV file from which this collection of transactions was uploaded (default: 'sample.csv').
        transactions_csv_file (str): The name of the internally created and managed CSV file storing the transaction data (default: 'last_uploaded_transactions.csv').
        transactions (dict): Dictionary mapping transaction numbers to Transaction objects.
    """
    def __init__(self, source_file='sample.csv', transactions_csv_file='last_uploaded_transactions.csv'):
        """
        Initializes a TransactionsManager object with the provided source file and transactions CSV file.

        Args:
            source_file (str): The name of the user-provided CSV file from which this collection of transactions was uploaded (default: 'sample.csv').
            transactions_csv_file (str): The name of the internally created and managed CSV file storing the transaction data (default: 'last_uploaded_transactions.csv').
        """
        self.source_file = source_file
        self.transactions_csv_file = transactions_csv_file

        # Dictionary with BudgetCategory objects as values, and their budget_category attribute as keys
        self.transactions = self.make_transactions_dictionary()

    def make_transactions_dictionary(self, transaction_objects=[Transaction('0', '1900-01-01', '0', 'Sample', 'Uncategorized', 'sample.csv')]):
        """
        Creates a dictionary mapping transaction numbers to Transaction objects.

        Args:
            transaction_objects (list): List of Transaction objects (default: [Transaction('0', '1900-01-01', '0', 'Sample', 'Uncategorized', 'sample.csv')]).

        Returns:
            dict: Dictionary mapping transaction numbers to Transaction objects.
        """
        self.transaction_objects = transaction_objects
        return {transaction_obj.transaction_num: transaction_obj for transaction_obj in self.transaction_objects}

    @property
    def source_file(self):
        """
        Getter method for the source_file attribute.

        Returns:
            str: The name of the user-provided CSV file from which this collection of transactions was uploaded.
        """
        return self._source_file

    @source_file.setter
    def source_file(self, source_file: str):
        """
        Setter method for the source_file attribute.

        Args:
            source_file (str): The source file to set for the transactions.

        Raises:
            ValueError: If the provided source file is not of type CSV.
        """
        if not source_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._source_file = source_file

    @property
    def transactions_csv_file(self):
        """
        Getter method for the transactions_csv_file attribute.

        Returns:
            str: The name of the internally created and managed CSV file storing the transaction data.
        """
        return self._transactions_csv_file

    @transactions_csv_file.setter
    def transactions_csv_file(self, transactions_csv_file: str):
        """
        Setter method for the transactions_csv_file attribute.

        Args:
            transactions_csv_file (str): The name of the CSV file to set for storing the transaction data.

        Raises:
            ValueError: If the provided file is not of type CSV.
        """
        if not transactions_csv_file.endswith('.csv'):
            raise ValueError(f'File must be of type CSV')
        self._transactions_csv_file = transactions_csv_file

    @property
    def transactions(self):
        """
        Getter method for the transactions attribute.

        Returns:
            dict: Dictionary mapping transaction numbers to Transaction objects.
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions: dict):
        """
        Setter method for the transactions attribute.

        Args:
            transactions (dict): Dictionary mapping transaction numbers to Transaction objects.

        Raises:
            TypeError: If the provided transactions is not a dictionary.
            ValueError: If any value in transactions is not a Transaction instance.
        """
        if not isinstance(transactions, dict):
            raise TypeError("Collection of transactions must be a dictionary")
        if not all(isinstance(transaction, Transaction) for transaction in transactions.values()):
            raise ValueError("All values in budget_categories must be BudgetCategory instances")
        self._transactions = transactions

    def __str__(self):
        """
        Returns a string representation of the TransactionsManager object as labeled data such as
        the internally created and managed CSV file name used for storing transactions data,
        the user-uploaded CSV file name from which this collection of transactions came,
        the number of transactions in this collection, and the number of transactions by budget category.

        Returns:
            str: The string representation of the TransactionsManager object.
        """
        total_transactions = len(self.transactions)
        transactions_by_category = {}
        for transaction in self.transactions.values():
            if transaction.category in transactions_by_category:
                transactions_by_category[transaction.category] += 1
            else:
                transactions_by_category[transaction.category] = 1

        output = f"Internal data storage file: {self.transactions_csv_file}\n"
        output += f"Last uploaded transactions: {self.source_file}\n"
        output += f"Total transactions: {total_transactions}\n"
        output += "Transactions by category:\n"
        for category, count in transactions_by_category.items():
            output += f"{category}: {count} transactions\n"

        return output

    def get_stored_transactions(self):
        """
        Reads in the stored transaction data from the CSV file. Since the transaction number isn't coming
        directly from the Transaction object, whose setters will transform the data to an int,
        manually transforms the transaction number from a numerical string to an integer.
        If the file doesn't exist, initializes it with default data.
        """
        if not os.path.exists(self.transactions_csv_file):
            self.update_stored_transactions()  # Initialize the file with default data
        else:
            source_files_in_data = []
            with open(self.transactions_csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.transactions = {}  # Prepare to load transactions from file
                for row in reader:
                    self.transactions[int(row['transaction_num'])] = Transaction(
                        row['transaction_num'],
                        row['transaction_date'],
                        row['amount'],
                        row['description'],
                        row['category'],
                        row['source_file'])
                    if row['source_file'] not in source_files_in_data:
                        source_files_in_data.append(row['source_file'])
            self.source_file = ', '.join(source_files_in_data)

    def update_stored_transactions(self):
        """
        Updates the stored transaction data in the CSV file with the current transactions.
        Overwrites whatever was in the file with the data currently in memory.
        """
        with open(self.transactions_csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                                    'transaction_num', 'transaction_date', 'amount', 'description', 'category', 'source_file'])
            writer.writeheader()
            for transaction_obj in self.transactions.values():
                writer.writerow({
                    'transaction_num': str(transaction_obj.transaction_num),
                    'transaction_date': transaction_obj.transaction_date.strftime('%Y-%m-%d'),
                    'amount': f"{transaction_obj.amount:.2f}",
                    'description': transaction_obj.description,
                    'category': transaction_obj.category,
                    'source_file': transaction_obj.source_file})

    def load_user_transactions(self):
        """
        Loads user transactions from the source file. Expects a CSV file in the project folder that was downloaded from the user's bank and
        contains transactions information. Designed based on Wells Fargo CSV files, which contain the following columns (no headers):
        date, amount, asterisk, blank or check number, description.

        Returns:
            bool: True if the transactions were loaded successfully, False otherwise.
        """
        try:
            with open(self.source_file, 'r', newline='') as file:
                reader = csv.reader(file)
                self.transactions = {} # Prepare to load transactions from file
                i = 0
                for i, row in enumerate(reader, start=1):
                    self.transactions[i] = Transaction(
                        i, # Transaction number
                        datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'), # Date (reformatted)
                        row[1], # Amount
                        row[4] if len(row) >= 5 else "", # Description
                        'Uncategorized',
                        self.source_file)
        except (FileNotFoundError, IndexError, csv.Error):
            return False
        self.update_stored_transactions() # Stores initial data
        return True

    def get_transaction_to_update(self):
        """
        Prompts the user to enter a transaction number to update or 'q' to exit.

        Returns:
            int: The transaction number to update.
            'q': If the user chooses to quit out of the current menu.
            None: If the user enters an invalid transaction number.
        """
        try:
            selection = input("Enter transaction number or 'q' to exit: ")
        except EOFError:
            sys.exit("Goodbye!")  # Assume EOFError indicates user wants to quit out of program
        if selection.lower() == 'q':
            return 'q'  # Lets calling function know user wants to quit out of current menu
        try:
            selection = int(selection)
            if selection not in self.transactions:
                raise ValueError
        except ValueError:
            return None
        return selection

    def formatted_transactions(self, sorted_by='Transaction number', ascending=True):
        """
        Formats the transactions for display, sorted by the specified criteria.

        Args:
            sorted_by (str): The criteria to sort the transactions by (default: 'Transaction number').
            ascending (bool): Whether to sort in ascending order (default: True).

        Returns:
            str: The formatted string representing the transactions.
         """
        match sorted_by:
            case 'Transaction number':
                sort_key = lambda x: x.transaction_num
            case 'Transaction date':
                sort_key = lambda x: x.transaction_date
            case 'Amount':
                sort_key = lambda x: x.amount
            case 'Category':
                sort_key = lambda x: x.category
            case _:
                print (f"Cannot sort by {sorted_by}")
                sort_key = lambda x: x.transaction_num

        sorted_transactions = sorted(self.transactions.values(), key=sort_key, reverse=not ascending) # Sorted function returns a list

        transactions_for_display = [{
            'Transaction #': transaction.transaction_num,
            'Date': transaction.transaction_date.strftime('%Y-%m-%d'),
            'Amount': f"{transaction.amount:,.2f}",
            'Description': transaction.description,
            'Category': transaction.category
        } for transaction in sorted_transactions]

        # Use tabulate to format the transactions for display
        display = tabulate(transactions_for_display, headers='keys', tablefmt='grid', floatfmt=".2f")
        return f"\n\n\x1B[4mLAST UPLOADED TRANSACTIONS\x1B[0m\nTransactions from: {self.source_file}\n\n{display}"


class FinancialController:
    """
    Controls financial operations by managing budgets and transactions.

    Attributes:
        budget_manager (BudgetManager): The budget manager object.
        transactions_manager (TransactionsManager): The transactions manager object.
    """
    def __init__(self):
        """
        Initializes a FinancialController object and loads the most recent budgets and transactions data into memory.
        """
        self.budget_manager = BudgetManager()
        self.transactions_manager = TransactionsManager()

        # Load most recent data into memory
        self.budget_manager.get_stored_budgets()
        self.transactions_manager.get_stored_transactions()

    def calculate_totals_by_category(self):
        """
        Calculates the totals for income and expenditures by category.
        """
        self.budget_manager.income_by_category = {category: 0.0 for category in self.budget_manager.income_by_category}
        self.budget_manager.expenditures_by_category = {category: 0.0 for category in self.budget_manager.expenditures_by_category}

        # Bank CSV files treat transactions coming into the account as positive, and transactions going out of the account as negative.
        # Switch the signs of expenditures to display as positive amounts
        for transaction in self.transactions_manager.transactions.values():
            if transaction.category in self.budget_manager.income_by_category:
                self.budget_manager.income_by_category[transaction.category] += transaction.amount
            elif transaction.category in self.budget_manager.expenditures_by_category:
                self.budget_manager.expenditures_by_category[transaction.category] -= transaction.amount
            else:
                self.budget_manager.expenditures_by_category['Uncategorized'] -= transaction.amount

    def view_current_budgets(self):
        """
        Calculates the totals by category and returns the formatted budgets with expenditures.

        Returns:
            str: The formatted string representing the current budgets with expenditures.
        """
        self.calculate_totals_by_category()
        return self.budget_manager.format_budgets_with_expenditures(self.transactions_manager.source_file)

    def update_budgets(self):
        """
        Calls the BudgetManager method, ensuring main() interacts solely with the FinancialController, not directly with the other classes.
        Updates the budget amounts through user interaction.
        """
        self.budget_manager.update_budget_amount()

    def categorize_all_transactions(self):
        """
        Categorizes all transactions based on their descriptions.
        """
        for transaction in self.transactions_manager.transactions.values():
            transaction.category = self.budget_manager.categorize_transaction(transaction.description.lower())

    def process_user_transactions(self, user_filename):
        """
        Processes user transactions from the specified file: Stores the file name in the TransactionsManager object,
        reads in the data, categorizes each transaction, updates the internal CSV file that stores transactions data,
        and calculates total income and expenditures by budget category.

        Args:
            user_filename (str): The name of the file containing user transactions.

        Returns:
            bool: True if the transactions were processed successfully, False otherwise.
        """
        self.transactions_manager.source_file = user_filename
        if not self.transactions_manager.load_user_transactions(): # Try to load user transactions into memory
            return False
        self.categorize_all_transactions()
        self.transactions_manager.update_stored_transactions()
        self.calculate_totals_by_category()
        return True

    def format_transactions(self, sort_by='Transaction number', ascending=True):
        """
        Calls the TransactionsManager method, ensuring main() interacts solely with the FinancialController,
        not directly with the other classes. Formats the transactions for display, sorted by the specified criteria.

        Args:
            sort_by (str): The criteria to sort the transactions by (default: 'Transaction number').
            ascending (bool): Whether to sort in ascending order (default: True).

        Returns:
            str: The formatted string representing the transactions.
        """
        return self.transactions_manager.formatted_transactions(sort_by, ascending)

    def recategorize_transactions(self, sort_order='Category'):
        """
        Allows the user to recategorize transactions through user interaction.
        Process: Transactions by category are displayed. When the user selects a transaction number to reclassify, the budget categories
        are displayed. When the user selects a budget category by option number, the chosen transaction is reclassified to that budget category.
        Changes to both the transactions and the budgets with expenditures that result from recategorization are displayed, and the user can
        select another transaction number to recategorize. The process continues until the user enters 'q'.

        Args:
            sort_order (str): The order in which to sort the transactions for display (default: 'Category').

        Returns:
            str: 'q' if the user chooses to quit out of the current menu.
        """
        while True:
            print(self.transactions_manager.formatted_transactions(sort_order))
            # Gets and validates transaction number
            transaction_to_update = self.transactions_manager.get_transaction_to_update()
            if not transaction_to_update:
                # Let the user know their selection was invalid before reprompting
                print("Invalid transaction number. Please try again.")
                continue
            if transaction_to_update == 'q':
                return 'q'  # Lets calling function know user wants to quit out of current menu
            while True:
                print(self.budget_manager.budget_menu)
                new_category = self.budget_manager.get_budget_category_to_update()
                if not new_category:
                    print('Please select from the available categories')
                    continue  # Let user try entering the category again, in case they just miskeyed the input
                if new_category == 'q':   # If user enters 'q' instead of an amount, they may have meant to choose a different transaction
                    break
                self.transactions_manager.transactions[transaction_to_update].category = new_category
                self.transactions_manager.update_stored_transactions()
                self.calculate_totals_by_category()
                print(self.budget_manager.format_budgets_with_expenditures(self.transactions_manager.source_file))
                break

def generate_figlet(phrase, user_font):
    """
    Generates a FIGlet text art representation of a given phrase using the specified font.

    Args:
        phrase (str): The phrase to be converted into FIGlet text art.
        user_font (str): The name of the FIGlet font to be used.

    Returns:
        str: The FIGlet text art representation of the phrase if the font is valid.
        str: "Invalid Font" if the specified font is not available or invalid.
    """
    try:
        figlet = Figlet(font=user_font)
        return figlet.renderText(phrase)
    except FigletError:
        return f"Invalid Font"

def generate_cow(phrase):
    """
    Generates a cowsay representation of a given phrase.

    Args:
        phrase (str): The phrase to be displayed in the cowsay output.

    Returns:
        str: The cowsay representation of the phrase.
    """
    return cowsay.get_output_string('cow', phrase)


def generate_menu(menu_options, menu_title='MENU'):
    """
    Generates a formatted menu string based on the provided menu options.

    Args:
        menu_options (list): A list of dictionaries representing the menu options.
        menu_title (str): The title of the menu (default: 'MENU').

    Returns:
        str: The formatted menu string.
    """
    required_keys = ['general classification', 'option title', 'option number']

    for dictionary in menu_options:
        for key in required_keys:
            if key not in dictionary:
                return f"Unable to load menu. Please ensure your data contains the keys '{required_keys[0]}', '{required_keys[1]}' and '{required_keys[2]}', then try again."

    menu_to_display = [f"\n\n\x1B[4m{menu_title}\x1B[0m"]  # Start with underlined menu title

    current_classification = None  # We only want to print the overall classification when it changes
    # Sort by option number
    for item in sorted(menu_options, key=lambda x: int(x[required_keys[2]])):
        if item[required_keys[0]] != current_classification:  # Only add the category name if we have a new category
            menu_to_display.append(f"\n{item[required_keys[0]]}:")
            current_classification = item[required_keys[0]]
        # Add the subcategory with its option number
        menu_to_display.append(f"    {item[required_keys[2]]} - {item[required_keys[1]]}")
    # Insert a blank line to separate the menu from the user input request
    menu_to_display.append("")

    return '\n'.join(menu_to_display)


def validate_csv_file(instructions='', input_prompt=''):
    """
    Validates a CSV file based on user input.

    Args:
        instructions (str): The instructions to display to the user.
        input_prompt (str): The prompt to display when asking for user input.

    Returns:
        str: The validated CSV file name or 'q' if the user chooses to quit.
    """
    print(instructions)
    while True:
        proposed_file = input(input_prompt).strip()
        if proposed_file.lower() == 'q':
            return 'q'
        if not proposed_file.endswith('.csv'):
            proposed_file += '.csv'  # Since only CSV files are accepted, add the extension then look for the given name in the project folder as a CSV file
        if not os.path.exists(proposed_file):
            print(f"The file '{proposed_file}' is invalid. Please try again, or enter 'q' to return to main menu:")
            continue
        return proposed_file


def main():
    """
    The main function that runs the financial management program.
    """
    main_menu = [
        {'general classification': 'Budget Options',
         'option title': 'View current budgets',
         'option number': '1',
         },
        {'general classification': 'Budget Options',
         'option title': 'Update budgets',
         'option number': '2',
         },
        {'general classification': 'Transaction Options',
         'option title': 'Choose a CSV transaction file to load',
         'option number': '3',
         },
        {'general classification': 'Transaction Options',
         'option title': 'View transactions by category',
         'option number': '4',
         },
        {'general classification': 'Transaction Options',
         'option title': 'View transactions in original order',
         'option number': '5',
         },
        {'general classification': 'Transaction Options',
         'option title': 'Recategorize transactions',
         'option number': '6',
         }]

    controller = FinancialController()

    title1 = generate_figlet('CS50\nFinal Project :', 'standard')
    title2 = generate_figlet('Budgets App', 'banner')
    cowified = generate_cow('Welcome to my project!')
    print(f'\n\n\n\n{title1}\n\n{title2}\n{cowified}')


    while True:
        print(generate_menu(main_menu, "MAIN MENU"))
        try:
            selection = input("Please enter option number or 'q' to exit: ")
            if selection.lower() == 'q':
                raise EOFError  # Treat both EOF characters and 'q' as simple exit requests without needing to differentiate between them
        except EOFError:
            sys.exit("Goodbye!")

        match selection:
            case '1':  # View current budgets
                print(controller.view_current_budgets())
            case '2':  # Update budgets
                print(controller.view_current_budgets())
                controller.update_budgets()
            case '3':  # Choose a CSV transaction file to load
                # Pass instructions and input prompt to validator function and receive validated file name
                valid_file = validate_csv_file("Please enter the name of a CSV file located in this project folder or 'q' to return to main menu.", "Filename: ")
                if valid_file.lower() == 'q':
                    continue  # Go back to main menu
                if not controller.process_user_transactions(valid_file):
                    print("There was a problem uploading the data. Please try again or select a different file uploaded to the project folder.")
                    continue # Go back to main menu
                print(controller.view_current_budgets())
            case '4':  # View transactions by category
                print(controller.format_transactions('Category'))
            case '5':  # View transactions in original order
                print(controller.format_transactions('Transaction number'))
            case '6':  # Recategorize transactions
                controller.recategorize_transactions()
            case _:
                # Let the user know their selection was invalid before reprompting
                print("Invalid option, please try again.")


if __name__ == '__main__':
    main()
