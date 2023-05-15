import csv
import math
import random

MAX_PLAYERS = 8
MAX_HOUSES = 5
MAX_INTEREST_RATE = 50 # changed the maximum interest rate to 50%
MIN_INTEREST_RATE = 5
LOAN_FACTOR = 0.1
REPUTATION_FACTOR = 0.05 # added a factor to adjust the interest rate based on reputation


class Player:
    def __init__(self, name):
        self.name = name
        self.properties = []
        self.loan_amount = 0
        self.loan_interest = 0
        self.loan_box = None
        self.loan_turns = 0
        self.allies = [] # added a list to store the allies of the player
        self.reputation = 0 # added a variable to store the reputation of the player

    def show_profile(self):
        print(f"Name: {self.name}")
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
        print("Allies:") # added a section to show the allies of the player
        if self.allies:
            for ally in self.allies:
                print(f"- {ally.name}")
        else:
            print("None")
        print("Reputation:") # added a section to show the reputation of the player
        print(f"{self.reputation}")
class Property:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.owner = None
        self.level = 0


properties = []

with open("PROPERTIES", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        property = Property(row["PROPERTY"], row["COLOUR_GROUP"])
        properties.append(property)


def update_data():
    with open("PROPERTIES", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["PROPERTY", "COLOUR_GROUP", "OWNER", "ESTATES"])
        writer.writeheader()
        for property in properties:
            writer.writerow({"PROPERTY": property.name, "COLOUR_GROUP": property.color, "OWNER": property.owner.name if property.owner else "none", "ESTATES": property.level})


players = []

num_players = int(input("How many players are there? (2-8) "))
while num_players < 2 or num_players > 8:
    print("Invalid number of players. Please enter a number between 2 and 8.")
    num_players = int(input("How many players are there? (2-8) "))

for i in range(num_players):
    name = input(f"Enter the name of player {i+1}: ")
    player = Player(name)
    players.append(player)
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
    # change the formula to use a logarithmic function instead of a linear one
    suggested_interest_rate = MIN_INTEREST_RATE + (MAX_INTEREST_RATE - MIN_INTEREST_RATE) * (1 - math.log(1 + score) / math.log(2))
    # change the factor to use a percentage instead of a multiplier
    suggested_interest_rate += LOAN_FACTOR * (loan_amount / 100)
    # add a factor to adjust the interest rate based on reputation
    suggested_interest_rate -= REPUTATION_FACTOR * player.reputation
    print(f"Suggested interest rate: {suggested_interest_rate:.2f}%")
    actual_interest_rate = float(input("Insert interest rate (0-100): "))
    while actual_interest_rate < 0 or actual_interest_rate > 100:
        print("Invalid interest rate. Please enter a number between 0 and 100.")
        actual_interest_rate = float(input("Insert interest rate (0-100): "))
    return actual_interest_rate
def make_changes(player):
    change_type = input("What type of change do you want to make? (type 'buy', 'sell', 'build', 'demolish', 'take', 'pay', 'form', 'break', or 'cancel'): ")
    if change_type.lower() == "buy":
        property_name = input("Enter the name of the property you want to buy: ")
        for property in properties:
            if property.name == property_name and property.owner == None:
                property.owner = player
                player.properties.append(property)
                update_data()
                break
        else:
            print("No such property found or it is already owned by someone else. Please try again.")
    elif change_type.lower() == "sell":
        property_name = input("Enter the name of the property you want to sell: ")
        for property in properties:
            if property.name == property_name and property.owner == player:
                property.owner = None
                player.properties.remove(property)
                update_data()
                break
        else:
            print("No such property found or you do not own it. Please try again.")
    elif change_type.lower() == "build":
        property_name = input("Enter the name of the property you want to build on: ")
        for property in properties:
            if property.name == property_name and property.owner == player and property.level < MAX_HOUSES:
                property.level += 1
                update_data()
                break
        else:
            print("No such property found or you do not own it or it has reached the maximum level. Please try again.")
    elif change_type.lower() == "demolish":
        property_name = input("Enter the name of the property you want to demolish on: ")
        for property in properties:
            if property.name == property_name and property.owner == player and property.level > 0:
                property.level -= 1
                update_data()
                break
        else:
            print("No such property found or you do not own it or it has reached the minimum level. Please try again.")
    elif change_type.lower() == "take":
        loan_amount = int(input("Enter the amount of money you want to borrow: "))
        while loan_amount <= 0:
            print("Invalid amount. Please enter a positive number.")
            loan_amount = int(input("Enter the amount of money you want to borrow: "))
        if player.loan_amount > 0:
            print("You already have an active loan. You cannot take another one.")
            return
        interest_rate = calculate_interest_rate(player, loan_amount)
        initial_box = input("Enter the name of your current box: ")
        while initial_box not in [property.name for property in properties] + ["GO", "JAIL", "FREE PARKING", "GO TO JAIL"]:
            print("Invalid box name. Please enter a valid property or corner box name.")
            initial_box = input("Enter the name of your current box: ")
        player.loan_amount = loan_amount
        player.loan_interest = interest_rate
        player.loan_box = initial_box
        player.loan_turns = 5
    elif change_type.lower() == "pay":
        if player.loan_amount > 0:
            total_amount = player.loan_amount * (1 + player.loan_interest / 100)
            player.loan_amount = 0
            player.loan_interest = 0
            player.loan_box = None
            player.loan_turns = 0
        else:
            print("You do not have an active loan.")
            return
    elif change_type.lower() == "form":
        ally_name = input("Enter the name of the player you want to form an alliance with: ")
        for ally in players:
            if ally.name == ally_name and ally != player and ally not in player.allies:
                player.allies.append(ally)
                ally.allies.append(player)
                player.reputation += 1 # added a line to increase the reputation of the player by 1
                ally.reputation += 1 # added a line to increase the reputation of the ally by 1
                break
        else:
            print("No such player found or you cannot form an alliance with them. Please try again.")
    elif change_type.lower() == "break":
        ally_name = input("Enter the name of the player you want to break an alliance with: ")
        for ally in players:
            if ally.name == ally_name and ally in player.allies:
                player.allies.remove(ally)
                ally.allies.remove(player)
                player.reputation -= 2 # added a line to decrease the reputation of the player by 2
                ally.reputation -= 2 # added a line to decrease the reputation of the ally by 2
                break
        else:
            print("No such player found or you do not have an alliance with them. Please try again.")
    elif change_type.lower() == "cancel":
        print("No changes made.")
        return
    else:
        print("Invalid type of change. Please try again.")
        return
event_counter = 0 # added a variable to keep track of the number of events
event_messages = ["GOVERNMENT HELP FOR REAL ESTATE", "GOVERNMENT HELP FOR WEALTH", "PROPERTY TAX", "WEALTH TAX"] # added a list of possible event messages


def main():
    global event_counter # added a line to use the global variable
    running = True
    while running:
        name = input("Enter the name of the player whose profile you want to see (or type 'quit' to exit): ")
        if name.lower() == "quit":
            running = False
        else:
            for player in players:
                if player.name == name:
                    player.show_profile()
                    choice = input("Do you want to make any changes or go back? (type 'changes' or 'back'): ")
                    if choice.lower() == "changes":
                        make_changes(player)
                        event_counter += 1 # added a line to increase the event counter by 1
                        if event_counter % 5 == 0: # added a condition to check if the event counter is divisible by 5
                            event_message = random.choice(event_messages) # added a line to choose a random event message
                            print(f"EVENT: {event_message}") # added a line to print the event message
                            if event_message == "GOVERNMENT HELP FOR REAL ESTATE":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 5 # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} receives ${sum}") # added a line to print the amount received by each player
                            elif event_message == "GOVERNMENT HELP FOR WEALTH":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 10 # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} receives ${sum}") # added a line to print the amount received by each player
                            elif event_message == "PROPERTY TAX":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 10 # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} pays ${sum}") # added a line to print the amount paid by each player
                            elif event_message == "WEALTH TAX":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 20 # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} pays ${sum}") # added a line to print the amount paid by each player
                        if random.random() < 0.05: # added a condition to create a 5% chance of an event called "GOVERNMENT AID"
                            print("EVENT: GOVERNMENT AID")
                            response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                            if response.lower() == "accept":
                                for player in players:
                                    sum = 0
                                    for property in player.properties:
                                        sum += property.level * 15 # added a line to calculate the sum based on the number of houses
                                    print(f"{player.name} receives ${sum}") # added a line to print the amount received by each player
                    break
            else:
                print("No such player found. Please try again.")


if __name__ == "__main__":
    main()
