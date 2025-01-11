import csv
import pandas as pd
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from dateutil import parser

exp_list = []
new_exp = "y"
exp_count = 0
exp_num = []
budget = 0
date_list = []
cat_list = []
amount_list = []
description_list = []
exp_dict = {"Date:": "", "Category:": "", "Amount:": "", "Description:": ""}

exp_read()

exp_dict.update({"Date:": date_list, "Category:": cat_list, "Amount:": amount_list, "Description:": description_list})

def add_expenses(exp_count, new_exp, exp_dict, date_list, cat_list, amount_list, description_list):

    while new_exp == "y":

        #print("New Expense Creation")
        exp_count = exp_count + 1
        #print("Expense Count:", exp_count)
        new_exp = str(input("Enter a new expense (y/n):"))

        if new_exp == "y":
            print("create new expense", new_exp)
        elif new_exp == "n":
            print("No new expenses")
            break
        else:
            print("You have entered an invalid option")
            break
    
        year = int(input("Start Year:"))
        month = int(input("Start Month:"))
        day = int(input("Start Day:"))

        year = str(year)
        month = str(month)
        day = str(day)
        dash = "-"


        full_date = year+dash+month+dash+day
        print("Full Date: ", full_date)
        full_date = parser.parse(full_date)
        print("Full Date Parsed: ", full_date)
        date_list.append(full_date)

        print("Please enter the expense category:")
        cat = str(input("Category:"))
        cat_list.append(cat)

        print("Please enter the amount of the expense:")
        amount = float(input("Amount:"))
        amount_list.append(amount)

        #Get expense description
        print("Please enter a description of the expense:")
        description = str(input("Description:"))
        description_list.append(description)
  
    exp_dict.update({"Date:": date_list, "Category:": cat_list, "Amount:": amount_list, "Description:": description_list})
    #print(exp_dict)

    return exp_dict, exp_count

def view_exp(exp_dict, exp_count):

    count = len(exp_dict["Date:"]) - 1

    print("Count: ", count)
    
    while count >=0:
        
        date = exp_dict["Date:"][count]
        date = str(date)
        date = date[:-8]
        cat = exp_dict["Category:"][count]
        amount = exp_dict["Amount:"][count]
        descript = exp_dict["Description:"][count]

        try:
            print("Date: ", date)
            print("Category: ", cat)
            print("Amount: ", amount)
            print("Description: ", descript)

        except:
            print("One or more values was missing or invalid")
            
        print("\n")
        count = count - 1


def budget_options(budget):

    print("Would you like to set a budget or track against an existing budget: 1 = set, 2 = track")
    budget_choice = int(input("1 Set,  2 Track:"))

    match budget_choice:

        case 1:
            print("You selected set budget option 1:")
            print("\n")
            budget = set_budget(budget)
            #print("Budget in case statement: ", budget)

        case 2:
            print("You selected track budget option 2:")
            print("\n")
            track_budget(budget)
    
    return budget
    

def track_budget(budget):

    total_spent = 0

    print("Budget has been established and set to: ", budget)
    print("Please enter the date range that you want to track:")

    s_year = int(input("Start Year:"))
    s_month = int(input("Start Month:"))
    s_day = int(input("Start Day:"))

    s_year = str(s_year)
    s_month = str(s_month)
    s_day = str(s_day)
    dash = "-"

    s_full_date = s_year+dash+s_month+dash+s_day
    print("Start Date: ", s_full_date)
    s_full_date = parser.parse(s_full_date)
    #print("Start Date: ", s_full_date)

    e_year = int(input("End Year:"))
    e_month = int(input("End Month:"))
    e_day = int(input("End Day:"))

    e_year = str(e_year)
    e_month = str(e_month)
    e_day = str(e_day)
    dash = "-"

    e_full_date = e_year+dash+e_month+dash+e_day
    print("End Date: ", e_full_date)
    e_full_date = parser.parse(e_full_date)
    #print("End Date: ", e_full_date)
    print("\n")

    print("Budget Set to: ", budget)

    count = len(exp_dict["Date:"]) - 1

    while count >=0:
    
        date_to_check = exp_dict["Date:"][count]
        #print("Date to Check: ", date_to_check)

        if s_full_date <= date_to_check <= e_full_date:
            #print("The date is within the range.")
            spent = exp_dict["Amount:"][count]
            total_spent = total_spent + spent
        
        else:
            print("No expenses found for the provided date range.")

        count = count - 1

    print("Total Spent: ", total_spent)
    
    if total_spent > budget:
        print("You have exceeded the established budget for the period by: ", total_spent - budget)
    else:
        print("You have a remaining budget of: ", budget - total_spent)

def exp_save(exp_dict):

    row_list = []
    count = len(exp_dict["Date:"]) - 1

    while count >= 0:
        #print("Date: ", exp_dict["Date:"][count])
        row = {'Date:': exp_dict["Date:"][count], 'Category:': exp_dict['Category:'][count], 'Amount:': exp_dict['Amount:'][count], 'Description:': exp_dict['Description:'][count]}
        row_list.append(row)
        print("Row List: ", row_list)
        count = count -1
    
    # Field names
    fieldnames = ['Date:', 'Category:', 'Amount:', "Description:"]

    # Writing to CSV file
    with open('Expenses.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header
        writer.writerows(row_list)

def exp_read():

    count = 0
    dates = []

    try:
        # Open the CSV file
        with open('expenses.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
    
            # Iterate over each row
            for row in reader:
                count = count + 1
                dates.append(row['Date:'])
                cat_list.append(row['Category:'])
                amount_list.append(row['Amount:'])
                description_list.append(row['Description:'])

        #exp_dict.update({"Date:": date_list, "Category:": cat_list, "Amount:": amount_list, "Description:": description_list})
        #print("From Expense Read: ", exp_dict)

        print("From Read: ", date_list)

        for i in dates:
            print("Date Unformatted: ", i)
            dates[i] = datetime.strptime(dates[i], "%m/%d/%Y")
            datelist.append(dates[i])

        return date_list, cat_list, amount_list, description_list
    
    except FileNotFoundError:
            print(f"Error: No save file was found.")
    except IOError:
            print(f"Error: An I/O error occurred while accessing the file")
    except Exception as e:
            print(f"An unexpected error occurred.")

print("Select one from the following:")
print("\n")
print("1) Add expenses:")
print("2) View expenses:")
print("3) Track budget:")
print("4) Save expenses:")
print("5) Exit the program:")
print("\n")

selection = int(input("Please make a selection"))

match selection:
    case 1:
        print("You selected option 1, Add expense")
        add_expenses(exp_count, new_exp, exp_dict, date_list, cat_list, amount_list, description_list)
    case 2:
        print("You selected option 2, View expense")
        print("\n")
        view_exp(exp_dict, exp_count)
    case 3:
        print("You selected option 3, Budget Options")
        budget = budget_options(budget)
    case 4:
        print("You selected option 4, Save expense")
        exp_save(exp_dict)
    case 5:
        print("You selected option 5, Exit the program")
    case _:
        print("\n")
        print("Incorrect value entered")
