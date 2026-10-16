import random

# Function to draw a unique card
def DrawCard(Dealer, Your):
    faceList = ["J", "Q", "K", "A"]
    suitList = ["♡", "⟡", "♠︎", "♣"]
    Draw = True
    while Draw:
        number = random.randint(2, 14)   # 11 - 14 will be J, Q, K, A respectively
        if number > 10:
            number = faceList[number - 11]
        else:
            number = str(number)
        suit = suitList[random.randint(0, 3)]
        
        card = number + suit
        if card not in DealerHand and card not in YourHand:
            Draw = False
    return card

# Function to check the value of a hand
def CheckHand(Hand):
    faceList = ["1", "J", "Q", "K", "A"]
    value = 0
    aces = False
    for card in Hand:
        if card[0] in faceList[:-1]:
            value += 10
        elif card[0] not in faceList:
            value += int(card[0])
        else:   # Initially count ace as 1
            aces = True
            value += 1
    if aces:
        if value + 10 <= 21:
            value += 10
    return value

# Function to discplay game screen
def DisplayScreen(Dealer, Your):
    print("-----------------------------")
    print()
    print("Dealers Hand")
    print(*Dealer)
    print()
    print()
    print("Your Hand")
    print(*Your)
    print()
    print()

# Function to get and validate the players choice
def Choice():
    print()
    print("if you want to hit, type hit, if you want to miss, type miss")
    choice = input("Do you want to hit or miss?     ")
    while choice != "hit" and choice != "miss":
        print()
        print("Please type a valid response")
        print("if you want to hit, type hit, if you want to miss, type miss")
        choice = input("Do you want o hit or miss?     ")
    return choice

# Main game logic
def main(Dealer, Your):

    while True:
        if CheckHand(Your) >= 21:
            break
        dec = Choice()
        if dec == "miss":
            break
        YourHand.append(DrawCard(Dealer, Your))
        DisplayScreen(Dealer, Your)

    Dealer[1] = DrawCard(Dealer, Your)
    print("Dealer reveals their hand:")
    DisplayScreen(Dealer, Your)
    print()
    your_score = CheckHand(Your)
    dealer_score = CheckHand(Dealer)
    
    if your_score > 21:
        print("You went bust")
        print("Dealer wins")

    while dealer_score < 17:
        DealerHand.append(DrawCard(Dealer, Your))
        dealer_score = CheckHand(Dealer)
        DisplayScreen(Dealer, Your)

    print("Final Results:")
    print(f"Your Total: {your_score}")
    print(f"Dealer Total: {dealer_score}")

    if dealer_score > 21:
        print("Dealer went bust")
        print("YOU WIN!!")
    elif dealer_score > your_score:
        print("Dealer wins")
    elif dealer_score < your_score:
        print("YOU WIN!!")
    else:
        print("It's a draw")


DealerHand = []
YourHand = []

YourHand.append(DrawCard(DealerHand, YourHand))
YourHand.append(DrawCard(DealerHand, YourHand))
DealerHand.append(DrawCard(DealerHand, YourHand))
DealerHand.append("#")

print("Welcome to Blackjack!")
DisplayScreen(DealerHand, YourHand)

main(DealerHand, YourHand)

