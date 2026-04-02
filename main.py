import csv
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
            if 0<= age <= 130:
                print("Your age must be between 130 and 0")
            else:
                return age
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
    with open("titanic3.csv","r",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pclass=int(row["pclass"])
                fare=float(row["fare"])
                if row["pclass"] == "" or row["fare"] == "":
                    continue
                if pclass in ranges:
                    if fare < ranges[pclass]["min"]:
                        ranges[pclass]["min"] = fare
                    if fare > ranges[pclass]["max"]:
                        ranges[pclass]["max"] = fare

            except (ValueError, KeyError):
                continue
    return ranges


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


