import csv
import random
import pandas as pd

def get_name():
    while True:
        # strip function - removes spaces from the beginning and end
        name=input("Please enter your name: ").strip()
        if name == "":
            print("Name cannot be empty")
        else:
            return name

def get_age():
    while True:
        try:
            age=float(input("Please enter your age: "))
            if 0< age <= 130:
                return age
            else:
                print("Your age must be between 130 and 0")
        except ValueError:
            print("Invalid age. Please enter a numeric value")

def get_gender():
    while True:
        sex=input("Please enter your gender: ").strip().lower()
        if sex in ["female","male"]:
            return sex
        else:
            print("Invalid gender. Please enter either 'male' or 'female'")

def get_fare(min_fare, max_fare):
    while True:
        try:
            fare = float(input("Enter your fare: "))
            if min_fare <= fare <= max_fare:
                return fare
            else:
                print(f"Fare must be between {min_fare} and {max_fare}.")

        except ValueError:
            print("Invalid input. Please enter a number.")

def get_class_ranges():
    ranges={1:{"min":float("inf"),"max":float("-inf")},
            2:{"min":float("inf"),"max":float("-inf")},
            3:{"min":float("inf"),"max":float("-inf")}}
    with open("titanic3.csv","r",encoding="utf-8-sig") as f:
        #utf-8-sig = removes the BOM at the start
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if row["pclass"] == "" or row["fare"] == "":
                    continue
                pclass=int(row["pclass"])
                fare=float(row["fare"])
                if pclass in ranges:
                    if fare < ranges[pclass]["min"]:
                        ranges[pclass]["min"] = fare
                    if fare > ranges[pclass]["max"]:
                        ranges[pclass]["max"] = fare

            except (ValueError, KeyError):
                continue
    return ranges
def determine_class(fare, ranges):
    for pclass in [1, 2, 3]:
        if ranges[pclass]["min"] <= fare <= ranges[pclass]["max"]:
            return pclass
    return None

def initialize_used_tickets_file():
    used_tickets = set()
    try:
        with open("used_ticket_numbers.txt", "r", encoding="utf-8") as f:
            if f.read().strip() != "":
                return
    except FileNotFoundError:
        pass
    with open("titanic3.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ticket = row["ticket"].strip()
                if ticket.isdigit() and len(ticket) == 6:
                    used_tickets.add(ticket)
            except (KeyError, AttributeError):
                continue
    with open("used_ticket_numbers.txt", "w", encoding="utf-8") as f:
        for ticket in used_tickets:
            f.write(ticket + "\n")

def get_used_tickets():
    used_tickets = set()
    try:
        with open("used_ticket_numbers.txt", "r", encoding="utf-8") as f:
            for line in f:
                ticket = line.strip()
                if ticket != "":
                    used_tickets.add(ticket)
    except FileNotFoundError:
        pass
    return used_tickets
def generate_ticket_number(used_tickets):
    while True:
        ticket_number = str(random.randint(100000, 999999))
        if ticket_number not in used_tickets:
            return ticket_number

def add_ticket_to_used_file(ticket_number):
    with open("used_ticket_numbers.txt", "a", encoding="utf-8") as f:
        f.write(str(ticket_number) + "\n")

def save_ticket(name, age, gender, fare, passenger_class, ticket_number):
    with open("tickets.txt", "a", encoding="utf-8") as f:
        f.write("--------------------------------------------------------\n")
        f.write(f"| ticket: {str(ticket_number):<18}| fare: {str(fare):<18}|\n")
        f.write("--------------------------------------------------------\n")
        f.write(f"| age: {str(age):<21}| class: {str(passenger_class):<17}|\n")
        f.write("--------------------------------------------------------\n")
        f.write(f"| sex: {gender:<21}| name: {name:<18}|\n")
        f.write("--------------------------------------------------------\n\n")

def get_age_group(age):
    if age <= 12:
        return "child"
    elif age <= 18:
        return "teen"
    elif age <= 40:
        return "adult"
    else:
        return "older"

def calculate_survival_chance(gender, passenger_class, age):
    titanic_df = pd.read_csv("titanic3.csv", encoding="utf-8-sig")
    titanic_df = titanic_df.dropna(subset=["sex", "pclass", "survived", "age"])
    titanic_df["sex"] = titanic_df["sex"].str.strip().str.lower()
    titanic_df["age_group"] = titanic_df["age"].apply(get_age_group)
    user_group = get_age_group(age)
    matched = titanic_df.loc[
        (titanic_df["sex"] == gender) &
        (titanic_df["pclass"] == passenger_class) &
        (titanic_df["age_group"] == user_group)
    ]
    if len(matched) == 0:
        return 0.0
    survived_count = len(matched.loc[matched["survived"] == 1])
    survival_percent = (survived_count / len(matched)) * 100
    return survival_percent

def main():
    initialize_used_tickets_file()

    ranges = get_class_ranges()

    min_fare = min(ranges[c]["min"] for c in ranges)
    max_fare = max(ranges[c]["max"] for c in ranges)

    name = get_name()
    age = get_age()
    gender = get_gender()
    fare = get_fare(min_fare, max_fare)

    passenger_class = determine_class(fare, ranges)

    used_tickets = get_used_tickets()
    ticket_number = generate_ticket_number(used_tickets)

    add_ticket_to_used_file(ticket_number)
    save_ticket(name, age, gender, fare, passenger_class, ticket_number)

    # print("Passenger details:")
    # print("Name:", name)
    # print("Age:", age)
    # print("Gender:", gender)
    # print("Fare:", fare)
    # print("Class:", passenger_class)
    # print("Ticket Number:", ticket_number)

    survival = calculate_survival_chance(gender, passenger_class, age)
    death = 100 - survival

    print(f"\nDear {name}, your chances to die on our trip are {death:.1f}%.")
    print("Enjoy your trip ☺")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


