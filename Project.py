import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import csv
from sklearn.tree import DecisionTreeRegressor

pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1000)

# GET the data using panda
global_SES = pd.read_csv("Data/GlobalSES.csv", index_col=['country'])
happiness_df = pd.read_csv("Data/Happiness_2017.csv", index_col=['Country'])

# General Variables
quit_application = False

# Dictionaries
all_countries_list = {}
high_class_countries = {}
middle_class_countries = {}
low_class_countries = {}
happiness_rank = {}
avg_data_per_year = {}

high_five_country_ses = {}
middle_five_country_ses = {}
low_five_country_ses = {}

high_country_happiness = {}

# Average SES
all_avg_ses = 0
low_avg_ses = 0
middle_avg_ses = 0
high_avg_ses = 0
yearly_avg_ses = 0

# Average GDP
all_avg_gdp = 0
low_avg_gdp = 0
middle_avg_gdp = 0
high_avg_gdp = 0
yearly_avg_gdp = 0

# Average Years of education
all_avg_edu = 0
low_avg_edu = 0
middle_avg_edu = 0
high_avg_edu = 0
yearly_avg_edu = 0

# Average Happiness
all_avg_happiness = 0
low_avg_happiness = 0
middle_avg_happiness = 0
high_avg_happiness = 0

# Misc
low_class_counter = 0
middle_class_counter = 0
high_class_counter = 0


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


def yearly_avg_table(yearly_list):
    print("{:<5} {:<9} {:<12} {:<8}".format('Year', 'SES', 'GDP', 'Education Average'))
    for year in yearly_list:
        print("{:<5} {:<9,.2f} {:<12,.2f} {:<8,.2f}".format(year, yearly_list[year]['SES'],
                                                            yearly_list[year]['GDPPC'],
                                                            yearly_list[year]['Edu']))
    print()


def top_each_class(country_list, cls, amount):
    i = 0
    print("{:<20} {:<6} {:<10} {:<12} {:<8}".format('Country', 'SES', 'Happiness', 'GDP', 'Education Average'))
    if cls == 'low':
        sorted_names = sorted(country_list, key=lambda x: country_list[x])
    else:
        sorted_names = sorted(country_list, key=lambda x: country_list[x], reverse=True)
    for country in sorted_names:
        if i < amount:
            print("{:<20} {:<6,.2f} {:<10,.2f} {:<12,.2f} {:<8,.2f}".format(country, country_list[country],
                                                                            happiness_df['Happiness.Score'].loc[
                                                                                country],
                                                                            global_SES.gdppc[
                                                                                (global_SES.year >= 2010)].loc[country],
                                                                            global_SES.yrseduc[
                                                                                (global_SES.year >= 2010)].loc[
                                                                                country]))
            i += 1
    print()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# DATA CLEANING and data wrangling in Python for SES
is_first_line = True
for row in open("Data/GlobalSES.csv"):
    if is_first_line:
        is_first_line = False
    else:
        values = row.split(",")
        # GET all the values by the column
        country = values[2]
        year = int(values[3])
        ses = float(values[4])
        class_level = values[5]
        gdppc = float(values[6])
        years_education = float(values[7])
        # CLEAN -- IF there are unrecognized character in the Country Name, it will be skipped
        if not country.isalpha():
            continue
        # CLEAN -- Change the description to make it more neat and store the require values in a dictionary
        if class_level == "High(core)":
            class_level = "High"
            if country not in high_class_countries and year == 2010:
                high_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        elif class_level == "Middle(semi-per)":
            class_level = "Middle"
            if country not in middle_class_countries and year == 2010:
                middle_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        elif class_level == "Low(periphery)":
            class_level = "Low"
            if country not in low_class_countries and year == 2010:
                low_class_countries[country] = {"SES": ses, "GDPPC": gdppc, "Edu": years_education}
        if country not in all_countries_list and year == 2010:
            all_countries_list[country] = {"SES": round(ses,2), "GDPPC": round(gdppc,2), "Edu": round(years_education,2), "Class": class_level}
        if country not in high_five_country_ses and year == 2010 and class_level == 'High':
            high_five_country_ses[country] = ses
        if country not in middle_five_country_ses and year == 2010 and class_level == 'Middle':
            middle_five_country_ses[country] = ses
        if country not in low_five_country_ses and year == 2010 and class_level == 'Low':
            low_five_country_ses[country] = ses
        while 1880 <= year <= 2010:
            if year not in avg_data_per_year:
                avg_data_per_year[year] = {'SES': 0, 'GDPPC': 0, 'Edu': 0}
            avg_data_per_year[year]['SES'] += ses
            avg_data_per_year[year]['GDPPC'] += gdppc
            avg_data_per_year[year]['Edu'] += years_education
            break

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
        happiness_score = float(values[2])
        gdp = float(values[5])
        life_expectancy = float(values[7])
        freedom = float(values[8])
        generosity = float(values[9])
        govt_trust = float(values[10])
        # CLEAN
        if country == 'Hong Kong S.A.R. China':
            country = 'Hong Kong'
        elif country == 'Taiwan Province of China':
            country = 'Taiwan'
        elif country == 'Palestinian Territories':
            country = 'Palestine'
        if country not in happiness_rank:
            happiness_rank[country] = {"Rank": rank, 'Happiness': round(happiness_score, 2), 'GDP': round(gdp, 2),
                                       "LifeExp": round(life_expectancy, 2), "Freedom": round(freedom, 2),
                                       "Generosity": round(generosity, 2), "GovtTrust": round(govt_trust, 2)}
        if country in high_class_countries:
            high_avg_happiness += happiness_score
            high_class_counter += 1
        if country in middle_class_countries:
            middle_avg_happiness += happiness_score
            middle_class_counter += 1
        if country in low_class_countries:
            low_avg_happiness += happiness_score
            low_class_counter += 1
        all_avg_happiness += happiness_score
all_avg_happiness = all_avg_happiness / len(happiness_rank)
high_avg_happiness = high_avg_happiness / high_class_counter
middle_avg_happiness = middle_avg_happiness / middle_class_counter
low_avg_happiness = low_avg_happiness / low_class_counter

# Create a new csv file of clean data for SES data set and Happiness data set
ses_output = open('clean_SES_data.csv', 'w', newline='')
ses_writer = csv.writer(ses_output)
ses_writer.writerow(['Country', 'SES', 'GDP per capita', 'Average Education Years', 'Class Level'])
for key in sorted(all_countries_list):
    ses_writer.writerow(
        [key, all_countries_list[key]['SES'], all_countries_list[key]['GDPPC'], all_countries_list[key]['Edu'],
         all_countries_list[key]['Class']])

# Create a new csv file of clean data for Happiness data set
ses_writer.writerow([])
ses_writer.writerow(
    ['Country', 'Rank', 'Happiness Score', 'GDP per capita', 'Life Expectancy', 'Freedom Score', 'Generosity Score',
     'Goverment Trust'])
for key in happiness_rank:
    ses_writer.writerow(
        [key, happiness_rank[key]['Rank'], happiness_rank[key]['Happiness'], happiness_rank[key]['GDP'],
         happiness_rank[key]['LifeExp'], happiness_rank[key]['Freedom'], happiness_rank[key]['Generosity'],
         happiness_rank[key]['GovtTrust']])

# Main Program
while not quit_application:
    welcome = input("Please type your selection number\n"
                    "1. Print Table for countries\n"
                    "2. SES\n"
                    "3. GDP per capita\n"
                    "4. Years of education\n"
                    "5. Top countries in each class\n"
                    "6. Output a chart\n"
                    "7. Prediction\n"
                    "0. Quit program\n"
                    "> ")
    clear_terminal()
    # PRINT the data in a table like structure
    while welcome == '1':
        command = input("Please type your selection number\n"
                        "1. All countries stats\n"
                        "2. Low class countries stats\n"
                        "3. Middle class countries stats\n"
                        "4. High class countries stats\n"
                        "5. Yearly stats for all countries\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            countries_table(all_countries_list)
        elif command == '2':
            countries_table(low_class_countries)
        elif command == '3':
            countries_table(middle_class_countries)
        elif command == '4':
            countries_table(high_class_countries)
        elif command == '5':
            yearly_avg_table(avg_data_per_year)
        elif command == '0':
            break
        else:
            print("Your input is invalid")
    # PRINT Average SES
    while welcome == '2':
        command = input("Please type your selection number for SES stats\n"
                        "1. Average all countries\n"
                        "2. Average low class countries\n"
                        "3. Average middle class countries\n"
                        "4. Average high class countries\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            cls = 'all'
            count_avg_ses(all_countries_list, all_avg_ses, cls)
        elif command == '2':
            cls = 'low'
            count_avg_ses(low_class_countries, low_avg_ses, cls)
        elif command == '3':
            cls = 'middle'
            count_avg_ses(middle_class_countries, middle_avg_ses, cls)
        elif command == '4':
            cls = 'high'
            count_avg_ses(high_class_countries, high_avg_ses, cls)
        elif command == '0':
            break
        else:
            print("Your input is invalid")
    # PRINT Average GDP per capita
    while welcome == '3':
        command = input("Please type your selection number for GDP stats\n"
                        "1. Average all countries\n"
                        "2. Average low class countries\n"
                        "3. Average middle class countries\n"
                        "4. Average high class countries\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            cls = 'all'
            count_avg_gdp(all_countries_list, all_avg_gdp, cls)
        elif command == '2':
            cls = 'low'
            count_avg_gdp(low_class_countries, low_avg_gdp, cls)
        elif command == '3':
            cls = 'middle'
            count_avg_gdp(middle_class_countries, middle_avg_gdp, cls)
        elif command == '4':
            cls = 'high'
            count_avg_gdp(high_class_countries, high_avg_gdp, cls)
        elif command == '0':
            break
        else:
            print("Your input is invalid")
    # PRINT Average Education years
    while welcome == '4':
        command = input("Please type your selection number for Years of Education stats\n"
                        "1. Average all countries\n"
                        "2. Average low class countries\n"
                        "3. Average middle class countries\n"
                        "4. Average high class countries\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            cls = 'all'
            count_avg_edu(all_countries_list, all_avg_edu, cls)
        elif command == '2':
            cls = 'low'
            count_avg_edu(low_class_countries, low_avg_edu, cls)
        elif command == '3':
            cls = 'middle'
            count_avg_edu(middle_class_countries, middle_avg_edu, cls)
        elif command == '4':
            cls = 'high'
            count_avg_edu(high_class_countries, high_avg_edu, cls)
        elif command == '0':
            break
        else:
            print("Your input is invalid")
    while welcome == '5':
        command = input("Please type your selection number\n"
                        "1. Low Class country\n"
                        "2. Middle Class country\n"
                        "3. High Class country\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            print("How many countries do you want to display? ")
            amount = input("> ")
            if amount.isdigit():
                if 0 <= int(amount) <= 10:
                    cls = 'low'
                    top_each_class(low_five_country_ses, cls, int(amount))
                else:
                    clear_terminal()
                    print("Please input between 1 - 10")
            else:
                clear_terminal()
                print('Input invalid')
        elif command == '2':
            print("How many countries do you want to display? ")
            amount = input("> ")
            if amount.isdigit():
                if 0 <= int(amount) <= 10:
                    cls = 'middle'
                    top_each_class(middle_five_country_ses, cls, int(amount))
                else:
                    clear_terminal()
                    print("Please input between 1 - 10")
            else:
                clear_terminal()
                print('Input invalid')
        elif command == '3':
            print("How many countries do you want to display? ")
            amount = input("> ")
            if amount.isdigit():
                if 0 <= int(amount) <= 10:
                    cls = 'high'
                    top_each_class(high_five_country_ses, cls, int(amount))
                else:
                    clear_terminal()
                    print('Please input between 1 - 10')
            else:
                clear_terminal()
                print('Input invalid')
        elif command == '0':
            break
        else:
            clear_terminal()
            print("Your input is invalid")
    while welcome == '6':
        command = input("Please select chart you want to output\n"
                        "1. GDP vs Education\n"
                        "2. SES vs Education\n"
                        "3. Happiness vs Life expectancy\n"
                        "4. Happiness vs GDP per capita\n"
                        "0. Back to main menu\n"
                        "> ")
        clear_terminal()
        if command == '1':
            # Scatter plot comparing GDP v Years of Education
            global_SES.plot.scatter(x='gdppc', y='yrseduc')
            plt.suptitle('GDP vs Education')
            plt.xlabel('GDP per capita')
            plt.ylabel('Average years of education')
            plt.show()
        if command == '2':
            # Scatter plot comparing SES v Years of Education
            global_SES.plot.scatter(x='ses', y='yrseduc')
            plt.suptitle('SES vs Education')
            plt.xlabel('Social Economic Status')
            plt.ylabel('Average years of education')
            plt.show()
        if command == '3':
            # Scatter plot comparing Happiness score v Life expectancy
            happiness_df.plot.scatter(x='Happiness.Score', y='Health..Life.Expectancy.')
            plt.suptitle('Happiness vs Life expectancy')
            plt.xlabel('Happiness')
            plt.ylabel('Life Expectancy')
            plt.show()
        if command == '4':
            # Scatter plot comparing Happiness score v GDP
            happiness_df.plot.scatter(x='Happiness.Score', y='Economy..GDP.per.Capita.')
            plt.suptitle('Happiness vs GDP per capita')
            plt.xlabel('Happiness')
            plt.ylabel('GDP per capita')
            plt.show()
        elif command == '0':
            break
    while welcome == '7':
        score = happiness_df['Happiness.Score']
        data_features = ['Economy..GDP.per.Capita.', 'Health..Life.Expectancy.', 'Freedom', 'Generosity',
                         'Trust..Government.Corruption.', 'Dystopia.Residual']
        columns = happiness_df[data_features]
        data_model = DecisionTreeRegressor(random_state=1)
        data_model.fit(columns, score)
        print("Making predictions for the following top ten countries happiness score:")
        print(columns.head(10))
        print("The predictions are")
        print(data_model.predict(columns.head(10)))
        print()
        # Prediction
        break
    # Invalid input
    if welcome != '1' and welcome != '2' and welcome != '3' and welcome != '4' and welcome != '5' and welcome != '6' and welcome != '7' and welcome != '0':
        clear_terminal()
        print("Your input is invalid")
    # QUIT the program
    if welcome == '0':
        clear_terminal()
        print("Thank you for using this program")
        quit_application = True
        break

'''
For future project

# Make a dataset:
# height = [low_avg_happiness, middle_avg_happiness, high_avg_happiness]
# bars = ('A', 'B', 'C')
# y_pos = np.arange(len(bars))

# Create bars
# plt.bar(y_pos, height)

# Create names on the x-axis
# plt.xticks(y_pos, bars)

# Show graphic
# plt.show()

# Scatter plot from Happiness dataset, comparing Happiness score v Life expectancy
# happiness_df.plot.scatter(x='Happiness.Score', y='Health..Life.Expectancy.')
# plt.suptitle('Test Title')
# plt.xlabel('Happiness')
# plt.ylabel('Life Expectancy')
# plt.show()

# Scatter plot from Happiness dataset, comparing Happiness score v GDP
# happiness_df.plot.scatter(x='Happiness.Score', y='Economy..GDP.per.Capita.')
# plt.suptitle('Test Title')
# plt.xlabel('Happiness')
# plt.ylabel('GDP per Capita')
# plt.show()

# global_SES.plot.scatter(x='gdppc', y='yrseduc', marker='^')
# plt.show()
'''
