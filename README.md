# BudgetsApp
#### Video Demo:  <https://youtu.be/XIx46uEZAUs>
#### Description:

Application to manage budgets and compare to expenditures from uploaded CSV files downloaded from your bank.

When Mint.com was purchased by Credit Karma, the budgeting functionality I had relied on for years was eliminated. As an autistic person, I have a lot of systems in place to ensure that I can succeed independently, and I relied on Mint's budgeting functionality to know which bills to pay, how much, and so on, every month. Losing this tool had a profound impact on me, and I was unable to find suitable online alternatives. Taking CS50 for Python made me realize that I could code my own solution to this problem, and even include additional features I would find helpful. This is only the first build of my budgeting program. It has a lot of room for expansion, such as adding user-defined budget categories, moving to a graphical user interface, using an api to get banking transactions and incorporating AI to handle the classification of transactions based on their descriptions, but this version, even as it is, has solved my problem and provided real-world support that improves my life in a tangible way.

Throughout the program, entering 'q' will break out of the current menu back to the previous one, unless the user is already at the main menu, in which case 'q' will exit the program. There are three major components to this program: budgets, transactions, and the financial controller that interfaces them. Let's go through these independently.

##### Budgets:

BudgetCategory class: Each budget is treated as an object with the following attributes:
- General classification (such as "Income", "Food & Dining", or "Travel & Transport")
- Budget category name (such as "Groceries", "Eating Out", or "Medical")
- A list of keywords that pertain to that budget category (such as netflix, nintendo, and subscription for Entertainment, or coffee, pizza, and starbuck for Eating Out)
- Option number used to select this specific budget category
- Amount budgeted for this budget category
- Search order, which ensures that something like "animal hospital" gets mapped to "Pet Care" from the keyword 'animal' instead of to "Medical" from the keyword 'hospital'

The attributes for each BudgetCategory object are set either by reading in data from a CSV file or by getting user input, both of which pass in strings. Because of this, typing the data is centralized within the class setters, avoiding potential errors due to repeatedly converting strings to other data types each time data is read in throughout the program. This class has no methods besides __init__ and __str__, as functionality is left up to the BudgetManager class. The __str__ method shows the BudgetCategory object's labeled attributes.

BudgetManager class: The program works extensively with a collection of budget categories, and that collection is built in the BudgetManager class. We begin with a list of BudgetCategory objects representing each available budget category that will be used in the program. This is transformed into a dictionary with the budget_category attribute for each object acting as that object's key, and the objects themselves are the values. This allows the budget categories to be easily referenced throughout the program by their names while ensuring that the key names exactly match the budget_category attribute of each BudgetCategory object. The class also stores the name of the internally created and managed CSV file where budget data will be stored, a string representation of the menu, and dictionaries used to sum income and expenditures by budget category. While the main menu is generated by code, and the budget menu can be generated using the exact same code, doing so generates a tall column that takes up too much of the screen for the intended uses, so a string representation is used, instead. The setters are mostly there for data validation, and the __str__ method shows the name of the file used for storing budget data and the amounts budgeted by category for that BudgetManager object.

BudgetManager methods: The budget manager reads from and writes to the internally created and managed CSV file (creating it from default data if it doesn't find the file when trying to read it in), allows users to upate budget amounts by category, format budgets for display (this method uses the dictionaries for summing income and expenditures by category for part of the content, and the tabulate library to arrange the information for display; it also shows any category that has either a budget or expenditures to it, which I find extremely useful), and categorize a transaction based on its description. Categorization is done by searching the passed-in description for each keyword in each budget category until it finds a match, then returning the budget category that contained the matching keyword.

##### Transactions:

The idea for transactions is that the user has gone to their bank's website and downloaded a CSV file containing the transactions that occurred in whatever time period corresponds to the budgets they created. As I bank with Wells Fargo, this app is based on the structure of a Wells Fargo CSV, which has 5 columns, without headings, that contain: the transaction date, the transaction amount, a column of asterisks, a column that is blank unless the transaction has a check number associated with it, in which case it contains the check number, and the transactions' description. Amounts are positive if received into the account and negative if withdrawn from the account. This CSV file is expected to be in the project folder in order to load it.

Transaction class: Each individual transaction is treated as an object with the following characteristics:
- Name of the user-uploaded file from which the transaction came
- Program-generated transaction number
- Transaction date
- Amount, as it was shown on the user's original file
- Description
- Category

The attributes for each Transaction object are set by reading in data from a CSV file, be it the user's original CSV file or the one created and managed by the program to store transaction data, both of which pass in strings. Because of this, typing the data is centralized within the class setters, avoiding potential errors due to repeatedly converting strings to other data types each time data is read in throughout the program. This class has no methods besides __init__ and __str__, as functionality is left up to the TransactionsManager class. The __str__ method shows the transaction's labeled attributes.

TransactionsManager class: The program works extensively with a collection of transactions, and that collection is built in the TransactionManager class. In a pleasant symmetry with the BudgetManager class, we begin with a list of Transaction objects, only the default transactions consist only of a single sample transaction from the source file 'sample.csv'. This is transformed into a dictionary with the transaction_num attribute acting as the object's key and the object itself is the value. This is how transactions will be stored: as a dictionary whose values are the individual Transaction objects and whose keys are the transaction numbers of each Transaction object. The class also stores the name of the internally created and managed CSV file where transactions data will be stored and the name of the last user-uploaded transactions CSV file. The setters are mostly there for data validation and the __str__ method shows the name of the internally created and managed CSV file where transactions data will be stored, the name of the last user-uploaded transactions CSV file, the total number of transactions, and the total number of transactions by category.

TransactionsManager methods: The transactions manager reads from and writes to the internally created and managed CSV file (creating it from default data if it doesn't find the file when trying to read it in); validates, uploads and processes user-provided transactions CSV files (which can be entered either with or without the '.csv' file extension, for convenience); gets a transaction number to upate from the user and formats transactions for display using the tabulate library, sorted by a specified attribute, with transaction number being the default. Processing user-provided transaction data involves reading in the data, assigning a transaction number, reformatting the date from m/d/Y to Y-m-d for consistency with other parts of the program, and assigning the category 'Uncategorized' in preparation for upcoming steps.

##### Financial Controller:

FinancialController class: The financial controller interfaces budgets and transactions, and it is the only class with which main() directly interacts. Initialization involves creating a BudgetManager object and a TransactionsManager object, and using those objects to load the latest stored budgets and transactions. These objects will also be used to perform all other operations in the class methods.

FinancialController methods:

calculate_totals_by_category sets all categories to zero in the BudgetManager dictionaries that store income and expenditures by category, then populates those dictionaries from transactions data. This method also changes the signs of any amounts considered expenditures (as opposed to income), in keeping with familiar conventions, but the signs are only changed in the income and expenditure by category dictionaries, not in the primary data sources.

view_current_budgets uses calculate_totals_by_category to prepare the dictionaries of income and expenditures by category, then calls the BudgetManager method to display formatted budgets with expenditures.

update_budgets simply calls the BudgetManager method to update the budgets, adding no new functionality, but ensuring that main() has a single point of interaction: the controller.

categorize_all_transactions sends each transaction's description to the BudgetManager method that categorizes a single transaction based on its description, then updates that transaction's category attribute.

process_user_transactions stores the user-provided file name in the TransactionsManager attribute that holds the source file name for the collection of transactions being worked with, calls the TransactionsManager method to upload user transactions, categorizes the transactions using categorize_all_transactions, stores the updated transaction data to the internally created and managed CSV file that holds transactions data, and calculates totals by category using its own calculate_totals_by_category method. That leaves the data ready to be worked with in memory and persisted in the CSV file.

format_transactions simply calls the TransactionsManager method to format the transactions, adding no new functionality, but ensuring that main() has a single point of interaction: the controller.

recategorize_transactions first displays all transactions by category, then gets a transaction number that the user wants to recategorize. Once the user's selection has been validated, the program displays the budget menu so the user can choose a new category from the available budget categories by entering its option number. The category for that specific Transaction object is updated, the new data is persisted in the internally created and managed CSV file, totals by category are re-calculated, and both the updated budgets and transactions are displayed, followed by a prompt to choose another transaction to recategorize.

##### Other Functions:

main(): This function contains a list of dictionaries called main_menu, a FinancialController object called 'controller', and a loop that allows users to choose what they would like to do and responds to their selections. The dictionaries in main_menu consist of 'general classification' (either Budget Options or Transaction Options), 'option title' (View current budgets, Update budgets, Choose a CSV transaction file to load, View transactions by category, View transactions in original order, and Recategorize transactions), and 'option number'. The loop passes main_menu to a generate_menu function that formats it nicely for display and prints the result, then gets the user's selection and matches it to one of the available options using match/case logic. Each of the cases results in simple actions, keeping main() clean and clear, but relying on other functions to handle some user interaction as a tradeoff. The other thing main() does is print an initial greeting using Figlet and Cowsay as a playful reference to one of the CS50 lessons and because the project requirements include three functions at the same level as main() and all the useful functionality of this project is handled by classes, so I had to come up with additional, albeit extraneous, functions.

generate_menu accepts a list of dictionaries to display as a menu and a menu title that defaults to "MENU". The dictionaries passed in can have any number of keys as long as they contain the three required keys: 'general classification', 'option title' and 'option number'. The function begins by initializing a list called menu_to_display that contains a couple of line breaks then the underlined title. Then it adds to that list until it ends up containing each general classification only once, followed by the options pertaining to that general classification shown as a set number of spaces, then the option number, then a dash, then the option title. Finally, it transforms the list into a string using '\n'.join() and returns it.

validate_csv_file accepts instructions to print once, and the prompt to display each time user input is requested. It isn't especially long or complicated and could have been included within main() under the option to load a CSV file, but having it be its own function kept things clean and easy to read and understand. This function prints the instructions, then prompts the user to input a file name. If the string entered by the user doesn't end with '.csv', the function adds '.csv'. Once the file name ends with '.csv', the function checks if the file exists within the project folder, reprompts if it doesn't, and returns the filename, with the '.csv' extension, if it finds the file. There was no need to check if the file name ended with a different extension, as the point is to determine whether or not a CSV file with that name exists within the project folder, and simply reprompt if it does not. Having a function work directly with users makes it difficult to test, and I did consider moving that part to main(), but I felt the tradeoff was worth it to keep main() straighforward, and 'outsource' file validation since it really does seem to be its own thing.

generate_figlet is a silly function added to meet project requirements and provide a bit of whimsy when the project first loads up. It accepts a phrase and a Figlet font, instantiates a Figlet object with the given font, and either returns the rendered text or "Invalid Font", as appropriate. In main(), this program renders the text "CS50 Final Project:" in Figlet's 'standard' font and the text "Budgets App" in Figlet's 'banner' font.

generate_cow is another silly, whimsical function added to meet project requirements and add some playfulness specifically related to the CS50 lectures. It accepts a phrase and has one line in it that returns the output string of a cow saying the input phrase.

##### Discussion:

I started with a list of dictionaries to represent the budget categories and transactions, but that came with a lot of challenges. A seasoned programmer suggested I consider making a class for each budget category and a class for each transaction. Classes were new to me, so this was hard to get my head around, but the very fact that it was new made me eager to pursue this line of thinking. I wanted to become comfortable with these new concepts, so I scrapped my original implementation (which was almost done) and started over from scratch. What seems straightforward now started off impossible to grasp: a whole class to simply represent a single budget category or a single transaction, without any methods or anything? Then managers to work with collections of these objects? Development was slow, and sometimes frustrating, but the more I worked with it, the more I really started 'getting it'. Finally, it was time for these classes to interact.

In my original implementation of the program (the one I scrapped), I was trying to work with budgets and transactions through main(), but I kept running into problems. The same seasoned programmer recommended a class specifically designed to bridge budgets and transactions. 'But what about encapsulation?' I thought. How can you instantiate an object of a class within another class? Isn't that against the rules? Once again, my head began to swim as I looked into this idea. Eventually, slowly, I began to get my head around this, too. And it all became exciting; I could do so much with this setup! I had thought my first version of this program wouldn't even include the option to manually recategorize transactions, but, with each transaction as an object, it seemed like maybe it wouldn't be that hard. And it wasn't. So I added it! It was... easy.

One problem I ran into when I added the recategorization option was that it worked perfectly with a freshly-loaded user file, but stopped working if the transactions were coming from stored data. I knew my Transaction setters were correctly typing object attributes, but it really seemed like transaction numbers were still being treated as strings when data was read in, and I didn't know why. I looked at the code to upload user data; it assigned integer transaction numbers to each transaction. Then I looked at the code to read in stored data, and I saw it. The transaction number wasn't coming from the Transaction object, it was coming from the CSV data that indicated the transaction number. Adding a simple int() around the read-in transaction number value fixed the issue nicely.

Overall, this program was a lot of fun to code, and I am very proud of the result. It's user-friendly, error-tolerant, and real-world useful. Not only that, but I'll be using it, myself, each month to keep track of everything, pay all my bills, and give myself the gift of peace of mind. I will probably expand this project in the future, but even now, especially for my first project ever, I think it's pretty great.

