#! /usr/bin/env python3

import deck
import db
import locale as lc
from datetime import time, datetime

# set locale
result = lc.setlocale(lc.LC_ALL, "")
if result[0] == "C":
    lc.setlocale(lc.LC_ALL, "en_us")


def display_header(start_time):
    # print header
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print("Enter 'x' for bet to exit")
    print("Start Time: ", start_time.strftime("%I:%M:%S %p"))


def get_starting_amount():
    # get the starting amount from the file
    try:
        player_money = db.read_money()
    except FileNotFoundError:
        print("Data file is missing, resetting starting amount to 1000.")
        player_money = 1000
        db.write_money(player_money)

    # if amount < 5, reset to 1000
    if player_money < 5:
        print("You don't have enough to play, resetting back to 1000.")
        player_money = 1000
        db.write_money(player_money)

    print("Player's money", lc.currency(player_money, grouping=True))
    print()
    return player_money


def get_bet_amount(player_money):
    # get the bet amount from the user
    while True:
        bet_amount = input("Bet Amounts: ")
        if bet_amount == "x":
            return bet_amount

        try:
            bet_amount = float(bet_amount)
        except ValueError:
            print("Invalid entry, please try again.\n")
            continue

        if bet_amount < 5:
            print("The minimum bet is 5. Please try again")
        elif bet_amount > 1000:
            print("The minimum bet is 1000. Please try again")
        elif bet_amount > player_money:
            print("You don't have enough money to make that bet. Please try again")
        else:
            return bet_amount


def play_player_hand(deck_of_cards, hand):
    while True:
        player_choice = input("Hit or Stand? (h/s): ")
        print()

        if player_choice.lower() == "h":
            deck.add_card(hand, deck.deal_card(deck_of_cards))
            display_cards(hand, "YOUR CARDS:")
            if deck.calculate_hand_points(hand) > 21:
                break
        elif player_choice.lower() == "s":
            break
        else:
            print("not a valid choice, please try again.")
    return hand


def display_cards(hand, title):
    print(title.upper())
    for card in hand:
        print(deck.display_card(card))
    print()


def display_outcome(player_points, player_hand, dealer_points, dealer_hand, bet_amount, player_money):
    if player_points > 21:
        print("Sorry, you busted. You lose.")
        player_money -= bet_amount
    elif player_points == 21 and len(player_hand) == 2:
        if dealer_points == 21 and len(dealer_hand) == 2:
            print("Bad luck,you both got BlackJack! Nobody wins.")
        else:
            print("Blackjack!")
            player_money += bet_amount * 1.5
    elif dealer_points == 21 and len(dealer_hand) == 2:
        print("The dealer got BlackJack, you lose.")
        player_money -= bet_amount
    elif dealer_points > 21:
        print("The dealer busted. You won!")
        player_money += bet_amount
    elif player_points > dealer_points:
        print("You won!")
        player_money += bet_amount
    elif dealer_points > player_points:
        print("You Lose.")
        player_money -= bet_amount
    else:
        print("You and the dealer pushed")

    return player_money


def exit_program(start_time):
    # Get the stop time
    stop_time = datetime.now()

    # Calculate the elapsed time
    elapse_time = stop_time - start_time

    elapsed_minutes = elapse_time.seconds // 60
    elapsed_seconds = elapse_time.seconds % 60

    elapsed_hours = elapsed_minutes // 60
    elapsed_minutes = elapsed_minutes % 60

    # Create the elapsed time object
    elapsed_time_object = time(elapsed_hours, elapsed_minutes, elapsed_seconds)

    # display the elapsed and end time
    print("Stop Time: ", stop_time.strftime("%I:%M:%S %p"))
    print('Time Played: ', elapsed_time_object)

    # print application has ended message
    print("Come back again soon!")


def main():
    start_time = datetime.now()
    display_header(start_time)
    player_money = get_starting_amount()

    # create a loop
    while True:
        # get the bet amount from the user
        bet_amount = get_bet_amount(player_money)

        # check to see if the user wants to exit
        if bet_amount == "x":
            break

        bet_amount = float(bet_amount)
        print()

        deck_of_cards = deck.get_deck()
        deck.shuffle(deck_of_cards)

        dealer_hand = deck.get_empty_hand()
        player_hand = deck.get_empty_hand()

        deck.add_card(player_hand, deck.deal_card(deck_of_cards))
        deck.add_card(dealer_hand, deck.deal_card(deck_of_cards))
        deck.add_card(player_hand, deck.deal_card(deck_of_cards))

        display_cards(dealer_hand, "DEALER'S SHOW CARD: ")
        display_cards(player_hand, "YOUR CARDS: ")

        # player the player hand
        player_hand = play_player_hand(deck_of_cards, player_hand)

        deck.add_card(dealer_hand, deck.deal_card(deck_of_cards))
        if deck.calculate_hand_points(player_hand) <= 21:
            while deck.calculate_hand_points(dealer_hand) < 17:
                deck.add_card(dealer_hand, deck.deal_card(deck_of_cards))

        display_cards(dealer_hand, "DEALER'S CARDS: ")

        # display points
        dealer_points = deck.calculate_hand_points(dealer_hand)
        player_points = deck.calculate_hand_points(player_hand)
        print("YOUR POINTS:\t", player_points)
        print("DEALER POINTS:\t", dealer_points)
        print()

        player_money = display_outcome(player_points, player_hand, dealer_points, dealer_hand, bet_amount, player_money)

        # print the outcome
        print("Player's money", lc.currency(round(player_money, 2), grouping=True))
        print()

        db.write_money(player_money)

        if player_money < 5:
            print("You are out of money.")
            break

        play_again = input("Play again? (y/n): ")

        if play_again.lower() != "y":
            print("\nCome again soon!")
            break

    # Exit Program
    exit_program(start_time)


main()
