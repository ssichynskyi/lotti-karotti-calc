# -*- coding: utf-8 -*-
from random import shuffle


class Card:
    """
    Class of the card which is used in the game Lotti Karotti to define
    the turn
    """
    def __init__(self, move: int, rotate: int):
        self._move = move
        self._rotate = rotate

    @property
    def move(self) -> int:
        """
        :return: how many of the effective fields the rabbit shall jump
        during the turn
        """
        return self._move

    @property
    def rotate(self) -> int:
        """
        :return: number of clicks to do. Negative number represents the reverse order
        """
        return self._rotate


class Stack:
    """
    Defines the cards of playable cards for the game.
    """
    def __init__(self, stack_config):
        """

        :param stack_config: List of dicts with predefined format:
        example: {'card_name': {'move': 1, 'rotate': 0, 'qtty': 8}}
        """
        self._cards = list()
        self._stack_config = stack_config
        self.generate_new()

    @property
    def cards(self) -> [Card]:
        """
        A list of objects of "Card" class that represent the current stack
        :return: current list of cards in this stack
        """
        return self._cards

    def generate_new(self) -> None:
        """
        Generates a new stack for the game. This action is required
        every time when players have picked all cards from the stack
        :return: None, the generated stack is available through the
        cards ppty
        """
        for card_type in self._stack_config:
            for _ in range(0, self._stack_config[card_type]['qtty']):
                self.cards.append(Card(self._stack_config[card_type]['move'],
                                       self._stack_config[card_type]['rotate']))
        shuffle(self._cards)

    def pull_card(self) -> Card:
        """
        Pulls the card from the top of the stack
        :return: Card
        """
        if len(self.cards) == 0:
            self.generate_new()
        return self.cards.pop()
