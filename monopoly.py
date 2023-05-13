import csv

MAX_PLAYERS = 8
START_MONEY = 1500
MAX_INTEREST_RATE = 100
MIN_INTEREST_RATE = 5
LOAN_FACTOR = 0.1

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.properties = []
        self.loan_amount = 0
        self.loan_interest = 0
        self.loan_box = None
        self.loan_turns = 0

    def show_profile(self):
        print(f"Name: {self.name}")
        print(f"Money: ${self.money}")
        print("Properties:")
        if self.properties:
            for property in self.properties:
                print(f"- {property.name} ({property.level})")
        else:
            print("None")
        print("Loan:")
        if self.loan_amount > 0:
            print(f"- Amount: ${self.loan_amount}")
            print(f"- Interest: {self.loan_interest:.2f}%")
            print(f"- Initial box: {self.loan_box}")
            print(f"- Remaining turns: {self.loan_turns}")
        else:
            print("None")

    def buy_property(self, property):
        if self.money >= property.price and property.owner == None:
            self.money -= property.price
            property.owner = self
            self.properties.append(property)

    def take_loan(self):
        loan_amount = int(input("Enter the amount of money you want to borrow: "))
        while loan_amount <= 0:
            print("Invalid amount. Please enter a positive number.")
            loan_amount = int(input("Enter the amount of money you want to borrow: "))
        if self.loan_amount > 0:
            print("You already have an active loan. You cannot take another one.")
            return
        interest_rate = calculate_interest_rate(self, loan_amount)
        initial_box = input("Enter the name of your current box: ")
        while initial_box not in [property.name for property in properties] + ["GO", "JAIL", "FREE PARKING", "GO TO JAIL"]:
            print("Invalid box name. Please enter a valid property or corner box name.")
            initial_box = input("Enter the name of your current box: ")
        self.loan_amount = loan_amount
        self.loan_interest = interest_rate
        self.loan_box = initial_box
        self.loan_turns = 5
        self.money += loan_amount

    def pay_loan(self):
        if self.loan_amount > 0:
            total_amount = self.loan_amount * (1 + self.loan_interest / 100)
            if self.money >= total_amount:
                self.money -= total_amount
                self.loan_amount = 0
                self.loan_interest = 0
                self.loan_box = None
                self.loan_turns = 0
            else:
                print("You do not have enough money to pay off your loan.")
                return
        else:
            print("You do not have an active loan.")
            return

class Property:
    def __init__(self, name, color, price, rent_levels):
        self.name = name
        self.color = color
        self.price = price
        self.rent_levels = rent_levels
        self.owner = None
        self.level = 0

properties = []

with open("PROPERTIES", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        property = Property(row["PROPERTY"], row["COLOUR_GROUP"], None, 0)
        properties.append(property)

def calculate_interest_rate(player, loan_amount):
    total_weight = 0
    max_weight = 0
    score = 0
    suggested_interest_rate = 0
    actual_interest_rate = 0

    for i, property in enumerate(properties):
        property_weight = (i + 1) / len(properties)
        max_weight += property_weight
        if property.owner == player:
            total_weight += property_weight
            if property.level > 0:
                house_hotel_weight = property.level / 5
                max_weight += house_hotel_weight
                total_weight += house_hotel_weight

    score = total_weight / max_weight

    suggested_interest_rate = MIN_INTEREST_RATE + (MAX_INTEREST_RATE - MIN_INTEREST_RATE) * (1 - score)

    suggested_interest_rate += LOAN_FACTOR * (loan_amount / player.money) * 100

    print(f"Suggested interest rate: {suggested_interest_rate:.2f}%")

    actual_interest_rate = float(input("Insert interest rate (0-100): "))
    while actual_interest_rate < 0 or actual_interest_rate > 100:
        print("Invalid interest rate. Please enter a number between 0 and 100.")
        actual_interest_rate = float(input("Insert interest rate (0-100): "))

    return actual_interest_rate

players = []

num_players = int(input("How many players are there? (2-8) "))
while num_players < 2 or num_players > 8:
    print("Invalid number of players. Please enter a number between 2 and 8.")
    num_players = int(input("How many players are there? (2-8) "))

for i in range(num_players):
    name = input(f"Enter the name of player {i+1}: ")
    player = Player(name, START_MONEY)
    players.append(player)

def make_changes(player):
    change_type = input("What type of change do you want to make? (type 'buy', 'sell', 'build', 'demolish', 'take', 'pay', or 'cancel'): ")
    if change_type.lower() == "buy":
        property_name = input("Enter the name of the property you want to buy: ")
        for property in properties:
            if property.name == property_name:
                player.buy_property(property)
                break
        else:
            print("No such property found. Please try again.")
    elif change_type.lower() == "sell":
        print("This is a dummy code. You need to write it yourself.")
    elif change_type.lower() == "build":
        print("This is a dummy code. You need to write it yourself.")
    elif change_type.lower() == "demolish":
        print("This is a dummy code. You need to write it yourself.")
    elif change_type.lower() == "take":
        player.take_loan()
    elif change_type.lower() == "pay":
        player.pay_loan()
    elif change_type.lower() == "cancel":
        print("No changes made.")
        return
    else:
        print("Invalid type of change. Please try again.")
        return

def main():
    running = True
    while running:
        name = input("Enter the name of the player whose profile you want to see (or type 'quit' to exit): ")
        if name.lower() == "quit":
            running = False
        else:
            for player in players:
                if player.name == name:
                    player.show_profile(
                    choice = input("Do you want to make any changes or go back? (type 'changes' or 'back'): ")
                    if choice.lower() == "changes":
                        make_changes(player)
                    break
            else:
                print("No such player found. Please try again.")

main()
