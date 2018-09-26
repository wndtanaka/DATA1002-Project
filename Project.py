import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)

# GET the data using panda
global_SES = pd.read_csv("Data/GlobalSES.csv")
happiness_df = pd.read_csv("Data/Happiness_2017.csv")

# General Variables
quit_application = False

# Dictionaries
all_countries_list = {}
high_class_countries = {}
middle_class_countries = {}
low_class_countries = {}
happiness_rank = {}

# Average SES
all_avg_ses = 0
low_avg_ses = 0
middle_avg_ses = 0
high_avg_ses = 0

# Average GDP
all_avg_gdp = 0
low_avg_gdp = 0
middle_avg_gdp = 0
high_avg_gdp = 0

# Average Years of education
all_avg_edu = 0
low_avg_edu = 0
middle_avg_edu = 0
high_avg_edu = 0


# FUNCTIONS
# COUNT and PRINT average SES
def count_avg_ses(countries_list, total, cls):
    for country in countries_list:
        total += countries_list[country]['SES']
    print("Average SES of {} class countries is {}".format(cls, (round(total / len(countries_list), 2))))
    print()


# COUNT and PRINT average GDP
def count_avg_gdp(countries_list, total, cls):
    for country in countries_list:
        total += countries_list[country]['GDPPC']
    print("Average GDP of {} class countries is {}".format(cls, (round(total / len(countries_list), 2))))
    print()


# COUNT and PRINT average education years
def count_avg_edu(countries_list, total, cls):
    for country in countries_list:
        total += countries_list[country]['Edu']
    print("Average education years of {} class countries is {}".format(cls, (round(total / len(countries_list), 2))))
    print()


# PRINT the data in a table like structure
def countries_table(countries_list):
    print("{:<20} {:<8} {:<10} {:<10}".format('Country', 'SES', 'GDPPC', 'Education Average'))
    for country in sorted(countries_list):
        print("{:<20} {:<8,.2f} {:<10,.2f} {:<10,.2f}".format(country, countries_list[country]['SES'],
                                                              countries_list[country]['GDPPC'],
                                                              countries_list[country]['Edu']))
    print()


''' How to do in Pandas
# for country in country_list:
#     if country not in countries_with_class:
#         countries_with_class[country] = global_SES['class'][(global_SES.country == country) & (global_SES.year == 2010)]
# for key in countries_with_class:
#     print(key, countries_with_class[key].to_string(header=None, index=None))
'''

# DATA CLEANING and data wrangling in Python for SES
is_first_line = True
for row in open("Data/GlobalSES.csv"):
    if is_first_line:
        is_first_line = False
    else:
        values = row.split(",")
        # GET all the values by the column
        country = values[2]
        year = values[3]
        ses = float(values[4])
        class_level = values[5]
        gdppc = float(values[6])
        years_education = float(values[7])
        # CLEAN -- Change C?te d'Ivoire to Ivory Coast
        if country == "C?te d'Ivoire":
            country = "Ivory Coast"
        if country not in all_countries_list and year == '2010':
            all_countries_list[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        # CLEAN -- Change the description to make it more neat and store the require values in a dictionary
        if class_level == "High(core)":
            class_level = "High"
            if country not in high_class_countries and year == '2010':
                high_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        elif class_level == "Middle(semi-per)":
            class_level = "Middle"
            if country not in middle_class_countries and year == '2010':
                middle_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        elif class_level == "Low(periphery)":
            class_level = "Low"
            if country not in low_class_countries and year == '2010':
                low_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}

# DATA CLEANING and data wrangling in Python for Happiness Level
is_first_line = True
for row in open("Data/Happiness_2017.csv"):
    if is_first_line:
        is_first_line = False
    else:
        values = row.split(",")
        # GET all the values by the column
        country = values[0]
        rank = values[1]
        life_expectancy = values[7]
        freedom = values[8]
        generosity = values[9]
        govt_trust = values[10]
        if country not in happiness_rank:
            happiness_rank[country] = {"Rank": rank, "LifeExp": life_expectancy, "Freedom": freedom,
                                       "Generosity": generosity, "GovtTrust": govt_trust}
for country in happiness_rank:
    print(country, happiness_rank[country])
# global_SES.plot.scatter(x='gdppc', y='yrseduc', marker='^')
# plt.show()

# while not quit_application:
#     welcome = input("Please type your selection number\n"
#                     "1. Print Table for countries\n"
#                     "2. SES\n"
#                     "3. GDP per capita\n"
#                     "4. Years of education\n"
#                     "0. Quit program\n"
#                     "> ")
#     os.system('cls')
#     # PRINT the data in a table like structure
#     while welcome == '1':
#         command = input("Please type your selection number country table\n"
#                         "1. All countries\n"
#                         "2. Low class countries\n"
#                         "3. Middle class countries\n"
#                         "4. High class countries\n"
#                         "0. Back to main menu\n"
#                         "> ")
#         os.system('cls')
#         if command == '1':
#             countries_table(all_countries_list)
#         elif command == '2':
#             countries_table(low_class_countries)
#         elif command == '3':
#             countries_table(middle_class_countries)
#         elif command == '4':
#             countries_table(high_class_countries)
#         elif command == '0':
#             break
#         else:
#             print("Your input is invalid")
#     # PRINT Average SES
#     while welcome == '2':
#         command = input("Please type your selection number for SES stats\n"
#                         "1. Average all countries\n"
#                         "2. Average low class countries\n"
#                         "3. Average middle class countries\n"
#                         "4. Average high class countries\n"
#                         "0. Back to main menu\n"
#                         "> ")
#         os.system('cls')
#         if command == '1':
#             cls = 'all'
#             count_avg_ses(all_countries_list, all_avg_ses, cls)
#         elif command == '2':
#             cls = 'low'
#             count_avg_ses(low_class_countries, low_avg_ses, cls)
#         elif command == '3':
#             cls = 'middle'
#             count_avg_ses(middle_class_countries, middle_avg_ses, cls)
#         elif command == '4':
#             cls = 'high'
#             count_avg_ses(high_class_countries, high_avg_ses, cls)
#         elif command == '0':
#             break
#         else:
#             print("Your input is invalid")
#     # PRINT Average GDP per capita
#     while welcome == '3':
#         command = input("Please type your selection number for GDP stats\n"
#                         "1. Average all countries\n"
#                         "2. Average low class countries\n"
#                         "3. Average middle class countries\n"
#                         "4. Average high class countries\n"
#                         "0. Back to main menu\n"
#                         "> ")
#         os.system('cls')
#         if command == '1':
#             cls = 'all'
#             count_avg_gdp(all_countries_list, all_avg_gdp, cls)
#         elif command == '2':
#             cls = 'low'
#             count_avg_gdp(low_class_countries, low_avg_gdp, cls)
#         elif command == '3':
#             cls = 'middle'
#             count_avg_gdp(middle_class_countries, middle_avg_gdp, cls)
#         elif command == '4':
#             cls = 'high'
#             count_avg_gdp(high_class_countries, high_avg_gdp, cls)
#         elif command == '0':
#             break
#         else:
#             print("Your input is invalid")
#     # PRINT Average Education years
#     while welcome == '4':
#         command = input("Please type your selection number for Years of Education stats\n"
#                         "1. Average all countries\n"
#                         "2. Average low class countries\n"
#                         "3. Average middle class countries\n"
#                         "4. Average high class countries\n"
#                         "0. Back to main menu\n"
#                         "> ")
#         os.system('cls')
#         if command == '1':
#             cls = 'all'
#             count_avg_edu(all_countries_list, all_avg_edu, cls)
#         elif command == '2':
#             cls = 'low'
#             count_avg_edu(low_class_countries, low_avg_edu, cls)
#         elif command == '3':
#             cls = 'middle'
#             count_avg_edu(middle_class_countries, middle_avg_edu, cls)
#         elif command == '4':
#             cls = 'high'
#             count_avg_edu(high_class_countries, high_avg_edu, cls)
#         elif command == '0':
#             break
#         else:
#             print("Your input is invalid")
#     # Invalid input
#     if welcome != '1' and welcome != '2' and welcome != '3' and welcome != '4' and welcome != '5' and welcome != '0':
#         os.system('cls')
#         print("Your input is invalid")
#     # QUIT the program
#     if welcome == '0':
#         os.system('cls')
#         print("Thank you for using this program")
#         quit_application = True
#         break
