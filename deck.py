#! /usr/bin/env python3

import random


# create a new deck of cards
def get_deck():
    # create our list/tuples
    deck = []
    ranks = {"Ace", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "Jack", "Queen", "King"}
    suits = {"Clubs", "Diamonds", "Spades", "Hearts"}

    # load the deck of cards
    for suit in suits:
        for rank in ranks:
            if rank == "Ace":
                card_value = 11
            elif rank == "Jack" or rank == "Queen" or rank == "King":
                card_value = 10
            else:
                card_value = int(rank)

            card = [rank, suit, card_value]
            deck.append(card)

    return deck


# Shuffle a deck of cards
def shuffle(deck):
    random.shuffle(deck)


# deal a card
def deal_card(deck):
    card = deck.pop()
    return card


# get an empty hand
def get_empty_hand():
    hand = []
    return hand


# add a card to the hand
def add_card(hand, card):
    hand.append(card)


# calculate hand point values
def calculate_hand_points(hand):
    points = 0
    ace_count = 0
    for card in hand:
        if card[0] == "Ace":
            ace_count += 1
        points += card[2]

    if ace_count > 0 and points > 21:
        points = points - (ace_count * 10)

    if ace_count > 1 and points <= 11:
        points += 10
    return points


# display a card
def display_card(card):
    return card[0] + " of " + card[1]


# main for testing
def main():
    print("Card Tester")

    deck = get_deck()
    shuffle(deck)
    for i in range(5):
        print(" ", display_card(deck[i]))
    print()

    hand = get_empty_hand()
    add_card(hand, deal_card(deck))
    add_card(hand, deal_card(deck))
    add_card(hand, deal_card(deck))

    print("HAND")
    for card in hand:
        print(" ", display_card(card))
    print("Points", calculate_hand_points(hand))


if __name__ == "__main__":
    main()

