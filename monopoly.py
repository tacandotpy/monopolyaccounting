import csv
import math
import random


MAX_PLAYERS = 8
MAX_HOUSES = 5
MAX_INTEREST_RATE = 50  # changed the maximum interest rate to 50%
MIN_INTEREST_RATE = 5
LOAN_FACTOR = 0.1
REPUTATION_FACTOR = 0.05  # added a factor to adjust the interest rate based on reputation
EVENT_MESSAGES = ["GOVERNMENT HELP FOR REAL ESTATE", "GOVERNMENT HELP FOR WEALTH", "PROPERTY TAX", "WEALTH TAX"]
event_counter = 0
properties = []


def manage_pass():  #Not in operation
    choice = input("Do you want to add or delete a pass? (add/delete): ")
    if choice == "add":
        pass_name = input("Enter the name of the pass: ")
        return pass_name
    elif choice == "delete":
        pass_name = input("Enter the name of the pass: ")
        return pass_name
    else:
        print("Invalid choice.")
        return None




class Pass:
    def __init__(self, property,owner):
        self.property = property
        self.owner = owner


class Player:
    def __init__(self, name):
        self.name = name
        self.properties = [] #Might be changed in order to show joint properties
        self.loan_amount = 0
        self.loan_interest = 0
        self.loan_box = None
        self.loan_turns = 0
        self.allies = []
        self.reputation = 0
        self.passes = []

    def show_profile(self):
        print(f"=====================================================================================\nName: {self.name}")
        print("Properties:")
        if self.properties:
            for property in self.properties:
                print(f"- {property.name} ({property.level}) [{property.color}]")
        else:
            print("None")
        print("Loan:")
        if self.loan_amount > 0:
            print(f"- Amount: €{self.loan_amount}")
            print(f"- Interest: {self.loan_interest:.2f}%")
            print(f"- Initial box: {self.loan_box}")
            print(f"- Remaining turns: {self.loan_turns}")
        else:
            print("None")
        print("Allies:")  #Section to show the allies of the player
        if self.allies:
            for ally in self.allies:
                print(f'-{ally}')
        else:
            print("None")
        print("Reputation:")
        print(f"{self.reputation}")
        print("Passes:")  #Section to show the passes of the player
        if self.passes:
            for each in self.passes:
                print(f"- {each.property.name}")
        else:
            print("None")
        print("=====================================================================================")

class Property:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.owner = None
        self.level = 0


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
    suggested_interest_rate = MIN_INTEREST_RATE + (MAX_INTEREST_RATE - MIN_INTEREST_RATE) * (1 - math.log(1 + score) / math.log(2))
    suggested_interest_rate += LOAN_FACTOR * (loan_amount / 100)
    suggested_interest_rate -= REPUTATION_FACTOR * player.reputation
    print(f"Suggested interest rate: {suggested_interest_rate:.2f}%")
    actual_interest_rate = float(input("Insert interest rate (0-100): "))
    while actual_interest_rate < 0 or actual_interest_rate > 100:
        print("Invalid interest rate. Please enter a number between 0 and 100.")
        actual_interest_rate = float(input("Insert interest rate (0-100): "))
    return actual_interest_rate


def make_changes(player):
    change_type = input("What type of change do you want to make? (type 'buy', 'sell', 'build', 'demolish', 'take', 'pay', 'form', 'break', 'trade', or 'cancel'): ")
    if change_type.lower() == "buy":
        property_name = input("Enter the name of the property you want to buy: ")
        property_accesible = False
        for property in properties:
            if property.name == property_name and property.owner == None:
                property.owner = player
                player.properties.append(property)
                update_data()
                property_accesible = True
                break
        if not property_accesible:
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
                color_group = input("Enter the name of the color group you want to share: ")  # added a line to ask for the color group to share
                while color_group not in set([property.color for property in properties]):  # added a condition to check if the color group is valid
                    print("Invalid color group. Please enter a valid one.")
                    color_group = input("Enter the name of the color group you want to share: ")
                group_properties = [property for property in properties if property.color == color_group]  # added a line to get the properties that belong to that color group
                if all([property.owner in [player, ally] for property in group_properties]):
                    player_percentage = float(input(f"Enter the percentage of {player.name} on the {color_group} properties (0-100): "))  # added a line to ask for the percentage of the player
                    while player_percentage < 0 or player_percentage > 100:  # added a condition to check if the percentage is valid
                        print("Invalid percentage. Please enter a number between 0 and 100.")
                        player_percentage = float(input(f"Enter the percentage of {player.name} on the {color_group} properties (0-100): "))
                    ally_percentage = 100 - player_percentage  # added a line to calculate the percentage of the ally
                    player.allies.append((ally, color_group, player_percentage))  # added a line to store the ally, color group and percentage as a tuple in the allies list
                    ally.allies.append((player, color_group, ally_percentage))  # added a line to store the player, color group and percentage as a tuple in the allies list
                    player.reputation += 5  # added a line to increase the reputation of the player by 1
                    ally.reputation += 5  # added a line to increase the reputation of the ally by 1
                    break
                else:
                    print("You and your ally do not own all the properties in that color group. Please try again.")  # added a line to print an error message if the alliance is not possible
            else:
                print("No such player found or you cannot form an alliance with them. Please try again.")
    elif change_type.lower() == "break":
        ally_name = input("Enter the name of the player you want to break an alliance with: ")
        for ally in players:
            if ally.name == ally_name and any([ally_tuple[0] == ally for ally_tuple in player.allies]):  # changed the condition to check if there is any alliance with that player
                color_group = input("Enter the name of the color group you want to break: ")  # added a line to ask for the color group to break
                while color_group not in set([property.color for property in properties]):  # added a condition to check if the color group is valid
                    print("Invalid color group. Please enter a valid one.")
                    color_group = input("Enter the name of the color group you want to break: ")
                for i, ally_tuple in enumerate(player.allies):  # added a loop to find and remove the alliance from the allies list
                    if ally_tuple[0] == ally and ally_tuple[1] == color_group:
                        del player.allies[i]
                        break
                for i, ally_tuple in enumerate(ally.allies):  # added a loop to find and remove the alliance from the allies list
                    if ally_tuple[0] == player and ally_tuple[1] == color_group:
                        del ally.allies[i]
                        break
                player.reputation -= 10  # added a line to decrease the reputation of the player by 2
                ally.reputation -= 10  # added a line to decrease the reputation of the ally by 2
                break
            else:
                print("No such player found or you do not have an alliance with them. Please try again.")
    elif change_type.lower() == "trade":  # added a new  type of change called "trade"
        trade_partner_name = input("Enter the name of the player you want to trade with: ") # added a line to ask for the trade partner name
        for trade_partner in players:  # added a loop to find and validate the trade partner
            if trade_partner.name == trade_partner_name and trade_partner != player:
                offer_properties = []  # added a list to store the properties offered by the player
                offer_passes = []  # added a list to store the passes offered by the player
                request_properties = []  # added a list to store the properties requested by the player
                request_passes = []  # added a list to store the passes requested by the player
                offer_type = input("What do you want to offer? (type 'property', 'pass', or 'done'): ") # added a line to ask for what type of offer is made
                while offer_type.lower() != "done":  # added a loop to allow multiple offers until done
                    if offer_type.lower() == "property":
                        property_name = input("Enter the name of the property you want to offer: ") # added a line to ask for the property name
                        for property in properties:  # added a loop to find and validate the property
                            if property.name == property_name and property.owner == player and property not in offer_properties:
                                offer_properties.append(property)  # added a line to add the property to the offer list
                                break
                            else:
                                print("No such property found or you do not own it or you have already offered it. Please try again.")   # added a line to print an error message if the property is invalid
                    elif offer_type.lower() == "pass":
                        pass_property_name = input("Enter the name of the property you want to offer a pass for: ")   # added a line to ask for the pass property name
                        for each in player.passes:   # added a loop to find and validate the pass
                            if each.property.name == pass_property_name and each not in offer_passes:
                                offer_passes.append(each)  # added a line to add the pass to the offer list
                                break
                            else:
                                print("No such pass found or you have already offered it. Please try again.")  # added a line to print an error message if the pass is invalid
                    else:
                        print("Invalid type of offer. Please try again.")  # added a line to print an error message if the offer type is invalid
                    offer_type = input("What do you want to offer? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of offer is made again
                request_type = input("What do you want to request? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of request is made
                while request_type.lower() != "done":  # added a loop to allow multiple requests until done
                    if request_type.lower() == "property":
                        property_name = input("Enter the name of the property you want to request: ")  # added a line to ask for the property name
                        for property in properties:  # added a loop to find and validate the property
                            if property.name == property_name and property.owner == trade_partner and property not in request_properties:
                                request_properties.append(property)  # added a line to add the property to the request list
                                break
                            else:
                                print("No such property found or your trade partner does not own it or you have already requested it. Please try again.") # added a line to print an error message if the property is invalid
                    elif request_type.lower() == "pass":
                        pass_property_name = input("Enter the name of the property you want to request a pass for: ") # added a line to ask for the pass property name
                        for each in trade_partner.passes:  # added a loop to find and validate the pass
                            if each.property.name == pass_property_name and each not in request_passes:
                                request_passes.append(each)  # added a line to add the pass to the request list
                                break
                            else:
                                print("No such pass found or you have already requested it. Please try again.")  # added a line to print an error message if the pass is invalid
                    else:
                        print("Invalid type of request. Please try again.")  # added a line to print an error message if the request type is invalid
                    request_type = input("What do you want to request? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of request is made again

                # Add some code to evaluate the fairness of the trade and suggest a counter-offer if needed

                offer_value = 0  # added a variable to store the value of the offer
                for property in offer_properties:  # added a loop to calculate the value of each offered property based on some heuristics
                    base_value = 10 * (properties.index(property) + 1) / len(properties)  # added a variable to store the base value of each property based on its position on the board
                    color_group_value = 5 * len([p for p in properties if p.color == property.color and p.owner == player]) / len([p for p in properties if p.color == property.color])  # added a variable to store the color group value of each property based on how many properties of the same color are owned by the player
                    level_value = 10 * property.level / MAX_HOUSES  # added a variable to store the level value of each property based on how many houses are built on it
                    ally_value = -5 * len([ally_tuple for ally_tuple in player.allies if ally_tuple[1] == property.color]) / len([p for p in properties if p.color == property.color])  # added a variable to store the ally value of each property based on how many allies share the same color group
                    offer_value += base_value + color_group_value + level_value + ally_value  # added a line to add the values of each property to the offer value

                for each in offer_passes:  # added a loop to calculate the value of each offered pass based on some heuristics
                    base_value = 5 * (properties.index(each.property) + 1) / len(properties)  # added a variable to store the base value of each pass based on its position on the board
                    owner_value = -10 if each.property.owner == trade_partner else 0  # added a variable to store the owner value of each pass based on whether the trade partner owns the property or not
                    offer_value += base_value + owner_value  # added a line to add the values of each pass to the offer value

                request_value = 0  # added a variable to store the value of the request
                for property in request_properties:  # added a loop to calculate the value of each requested property based on some heuristics
                    base_value = 10 * (properties.index(property) + 1) / len(properties)  # added a variable to store the base value of each property based on its position on the board
                    color_group_value = 5 * len([p for p in properties if p.color == property.color and p.owner == trade_partner]) / len([p for p in properties if p.color == property.color])  # added a variable to store the color group value of each property based on how many properties of the same color are owned by the trade partner
                    level_value = 10 * property.level / MAX_HOUSES  # added a variable to store the level value of each property based on how many houses are built on it
                    ally_value = -5 * len([ally_tuple for ally_tuple in trade_partner.allies if ally_tuple[1] == property.color]) / len([p for p in properties if p.color == property.color])  # added a variable to store the ally value of each property based on how many allies share the same color group
                    request_value += base_value + color_group_value + level_value + ally_value  # added a line to add the values of each property to the request value

                for each in request_passes:  # added a loop to calculate the value of each requested pass based on some heuristics
                    base_value = 5 * (properties.index(each.property) + 1) / len(properties)  # added a variable to store the base value of each pass based on its position on the board
                    owner_value = -10 if each.property.owner == player else 0  # added a variable to store the owner value of each pass based on whether the player owns the property or not
                    request_value += base_value + owner_value  # added a line to add the values of each pass to the request value

                fairness_ratio = offer_value / request_value if request_value > 0 else float("inf")  # added a variable to store the ratio between offer and request values
                print(f"Fairness ratio: {fairness_ratio:.2f}")  # added a line to print the fairness ratio

                if fairness_ratio > 1.2:  # added a condition to check if the offer is too high compared to the request
                    print("Your offer is too generous. You might want to lower it or ask for more.")  # added a line to print a warning message
                elif fairness_ratio < 0.8:
                    print("Your offer is too low. You might want to raise it or ask for less.")  # added a line to print a warning message
                    counter_offer = input("Do you want to make a counter-offer? (type 'yes' or 'no'): ")  # added a line to ask for a counter-offer
                    while counter_offer.lower() not in ["yes", "no"]:  # added a condition to check if the answer is valid
                        print("Invalid answer. Please type 'yes' or 'no'.")
                        counter_offer = input("Do you want to make a counter-offer? (type 'yes' or 'no'): ")
                    if counter_offer.lower() == "yes":  # added a condition to check if the answer is yes
                        offer_properties = []  # added a line to reset the offer properties list
                        offer_passes = []  # added a line to reset the offer passes list
                        request_properties = []  # added a line to reset the request properties list
                        request_passes = []  # added a line to reset the request passes list
                        offer_type = input("What do you want to offer? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of offer is made
                        while offer_type.lower() != "done":  # added a loop to allow multiple offers until done
                            if offer_type.lower() == "property":
                                property_name = input("Enter the name of the property you want to offer: ")  # added a line to ask for the property name
                                for property in properties:  # added a loop to find and validate the property
                                    if property.name == property_name and property.owner == player and property not in offer_properties:
                                        offer_properties.append(property)  # added a line to add the property to the offer list
                                        break
                                    else:
                                        print("No such property found or you do not own it or you have already offered it. Please try again.")  # added a line to print an error message if the property is invalid
                            elif offer_type.lower() == "pass":
                                pass_property_name = input("Enter the name of the property you want to offer a pass for: ")  # added a line to ask for the pass property name
                                for each in player.passes:  # added a loop to find and validate the pass
                                    if each.property.name == pass_property_name and each not in offer_passes:
                                        offer_passes.append(each)  # added a line to add the pass to the offer list
                                        break
                                    else:
                                        print("No such pass found or you have already offered it. Please try again.")  # added a line to print an error message if the pass is invalid
                            else:
                                print("Invalid type of offer. Please try again.")  # added a line to print an error message if the offer type is invalid
                            offer_type = input("What do you want to offer? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of offer is made again
                        request_type = input("What do you want to request? (type 'property', 'pass', or 'done'): ")  # added a line to ask for what type of request is made
                        while request_type.lower() != "done":  # added a loop to allow multiple requests until done
                            if request_type.lower() == "property":
                                property_name = input("Enter the name of the property you want to request: ")  # added a line to ask for the property name
                                for property in properties:  # added a loop to find and validate the property
                                    if property.name == property_name and property.owner == trade_partner and property not in request_properties:
                                        request_properties.append(property)  # added a line to add the property to the request list
                                        break
                                    else:
                                        print("No such property found or your trade partner does not own it or you have already requested it. Please try again.")  # added a line to print an error message if the property is invalid
                            elif request_type.lower() == "pass":
                                pass_property_name = input("Enter the name of the property you want to request a pass for: ")  # added a line to ask for the pass property name
                                for each in trade_partner.passes:  # added a loop to find and validate the pass
                                    if each.property.name == pass_property_name and each not in request_passes:
                                        request_passes.append(each)


def main():
    global event_counter  # added a line to use the global variable
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
                        event_counter += 1  # added a line to increase the event counter by 1
                        if event_counter % 10 == 0:  # added a condition to check if the event counter is divisible by 5
                            event_message = random.choice(EVENT_MESSAGES)  # added a line to choose a random event message
                            print(f"EVENT: {event_message}")  # added a line to print the event message
                            if event_message == "GOVERNMENT HELP FOR REAL ESTATE":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 5  # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} receives ${sum}")  # added a line to print the amount received by each player
                            elif event_message == "GOVERNMENT HELP FOR WEALTH":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 10  # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} receives ${sum}")  # added a line to print the amount received by each player
                            elif event_message == "PROPERTY TAX":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 10  # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} pays ${sum}")  # added a line to print the amount paid by each player
                            elif event_message == "WEALTH TAX":
                                response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                                if response.lower() == "accept":
                                    for player in players:
                                        sum = 0
                                        for property in player.properties:
                                            sum += property.level * 20  # added a line to calculate the sum based on the number of houses
                                        print(f"{player.name} pays ${sum}")  # added a line to print the amount paid by each player
                        if random.random() < 0.05:  # added a condition to create a 5% chance of an event called "GOVERNMENT AID"
                            print("EVENT: GOVERNMENT AID")
                            response = input("Do you accept this event? (type 'accept' or 'decline'): ")
                            if response.lower() == "accept":
                                for player in players:
                                    sum = 0
                                    for property in player.properties:
                                        sum += property.level * 15  # added a line to calculate the sum based on the number of houses
                                    print(f"{player.name} receives ${sum}")  # added a line to print the amount received by each player
                    break
            else:
                print("No such player found. Please try again.")


if __name__ == "__main__":
    main()
