import random

class player(object):
    def __init__(self,name):
        self.hand=[]
        self.name=name

    def get_name(self):
        return self.name

    def add_card_to_hand(self,card):
        if card != None:
            self.hand.append(card)

    def remove_card_from_hand(self,card):
        self.hand.remove(card)
    
    def hand_size(self):
        return len(self.hand)

class cardDeck(object):
    def __init__(self):
        heart='2H,3H,4H,5H,6H,7H,8H,9H'
        diamond='2D,3D,4D,5D,6D,7D,8D,9D'
        spade='2S,3S,4S,5S,6S,7S,8S,9S'
        club='2C,3C,4C,5C,6C,7C,8C,9C'

        self.deck=heart.split(',')+diamond.split(',')+spade.split(',')+club.split(',')

    def get_card(self):
        if len(self.deck) < 1:
            return None
        card=random.choice(self.deck)
        self.deck.remove(card)
        return card

    def compare_card(self,card1,card2):
        if card1[0]>card2[0]:
            return card1
        elif card1[0]<card2[0]:
            return card2
        elif card1[1]>card2[1]:
            return card1
        else:
            return card2

name1=input('player1 name : ')            
player1=player(name1)
name2=input('player2 name : ')
player2=player(name2)
deck=cardDeck()

while True:
    player1_card=deck.get_card()
    player2_card=deck.get_card()
    player1.add_card_to_hand(player1_card)
    player2.add_card_to_hand(player2_card)
    if player1_card == None or player2_card == None:
        print('game over')
        print(name1,': card number ',player1.hand_size())
        print(name2,': card number ',player2.hand_size())
        print('winner')
        if player1.hand_size() > player2.hand_size():
            print(name2,'winner')
        elif player1.hand_size() < player2.hand_size():
            print(name1,'winner')
        else:
            print('draw')
        break
    else:
        print(name1,':',player1_card)
        print(name2,':',player2_card)
        if deck.compare_card(player1_card,player2_card)==player1_card:
            player1.remove_card_from_hand(player1_card)
            player2.add_card_to_hand(player1_card)
        else:
            player2.remove_card_from_hand(player2_card)
            player1.add_card_to_hand(player2_card)