import numpy as np
from math import comb
from enum import Enum
from .question import Question

class CardContent(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    FACE = 13

class CardSuit(Enum):
    DIAMOND = 0
    SPADE = 1
    CLUB = 2
    HEART = 3
    RED = 4
    BLACK = 5

class Card:
    def __init__(self, content: CardContent=None, suit: CardSuit=None) -> None:
        self.content = content
        self.suit = suit
        self.face = content in set([CardContent.JACK, CardContent.QUEEN, CardContent.KING, CardContent.FACE])
        self.colour = suit in set([CardSuit.RED, CardSuit.BLACK])
        self.probability = self.calc_probability()

    def __repr__(self) -> str:
        card_string = self.suit._name_ + ' ' if self.suit else ''
        card_string += self.content._name_ if self.content else ''
        return card_string.lower().rstrip()

    def calc_probability(self) -> int:
        amount = 52
        if self.content:
            amount = 12 if self.content == CardContent.FACE else 4
        if self.suit:
            amount /= 2 if self.colour else 4
        return amount

    def calc_overlap(self, other: object) -> int:
        if (self.face and other.content == CardContent.FACE) or (self.content == CardContent.FACE and other.face):              # face overlap
            return 4
        elif (self.colour and other.suit) or (self.suit and other.colour):              # colour overlap
            return 13
        elif self.content and (not self.suit) and (not other.content) and other.suit:   # alternating none's overlap case 1
            overlap = 12 if self.face else 4
            overlap /= 2 if other.colour else 4
            return overlap
        elif (not self.content) and self.suit and other.content and (not other.suit):   # alternating none's overlap case 2
            overlap = 12 if other.face else 4
            overlap /= 2 if self.colour else 4
            return overlap
        return 0

class ProbabilitiesQuestionType(Enum):
    SINGLE_EVENT = 0
    COUNTING = 1
    DEPENDANT = 2
    INDEPENDANT = 3
    MUT_EXC = 4
    NON_MUT_EXC = 5

    @staticmethod
    def random_type():
        return np.random.choice(list(ProbabilitiesQuestionType))

class ProbabilitiesQuestion(Question):
    def __init__(self, question_type) -> None:
        self.question_type = question_type

        if self.question_type == ProbabilitiesQuestionType.SINGLE_EVENT:
            cards = [self.random_card()]
        elif self.question_type == ProbabilitiesQuestionType.COUNTING:
            amount = np.random.randint(2, 5)
            cards = [self.random_card(minimum_numerator=amount)]
        elif self.question_type == ProbabilitiesQuestionType.DEPENDANT:
            overlap = np.random.randint(2)
            cards = [self.random_card()]
            cards += [self.random_card(other_card=cards[0], overlap=overlap)]
        elif self.question_type == ProbabilitiesQuestionType.NON_MUT_EXC:
            cards = [self.random_card()]
            cards += [self.random_card(other_card=cards[0], overlap=True)]
        else:
            cards = [self.random_card()]
            cards += [self.random_card(other_card=cards[0], overlap=False)]

        self.prompt_base_key = {
            ProbabilitiesQuestionType.SINGLE_EVENT: 'What is the probability of drawing a %data% card from a standard deck of cards?',
            ProbabilitiesQuestionType.COUNTING: 'What is the probability of drawing %data% %data% cards from a standard deck of cards if %data% cards are randomly selected?',
            ProbabilitiesQuestionType.DEPENDANT: 'What is the probability of drawing a %data% card and a %data% card from a standard deck of cards, assuming that the first is not replaced?',
            ProbabilitiesQuestionType.INDEPENDANT: 'What is the probability of drawing a %data% card and a %data% card from a standard deck of cards, assuming that the first is replaced and the deck is shuffled?',
            ProbabilitiesQuestionType.MUT_EXC: 'What is the probability of drawing a %data% card or a %data% card from a standard deck of cards?',
            ProbabilitiesQuestionType.NON_MUT_EXC: 'What is the probability of drawing a %data% card or a %data% card from a standard deck of cards?',
        }
        base = self.prompt_base_key[self.question_type]
        
        if question_type == ProbabilitiesQuestionType.COUNTING:
            data = [amount, cards[0], amount]
            answer = [self.calc_counting(cards, amount)]
        elif question_type == ProbabilitiesQuestionType.DEPENDANT:
            data = cards
            answer = [self.calc_dependant(cards, overlap)]
        else:
            data = cards
            self.answer_key = {
                ProbabilitiesQuestionType.SINGLE_EVENT: self.calc_single_event,
                ProbabilitiesQuestionType.DEPENDANT: self.calc_dependant,
                ProbabilitiesQuestionType.INDEPENDANT: self.calc_independant,
                ProbabilitiesQuestionType.MUT_EXC: self.calc_mut_exc,
                ProbabilitiesQuestionType.NON_MUT_EXC: self.calc_non_mut_exc,
            }
            answer = [self.answer_key[self.question_type](cards)]
        
        super().__init__(base, data, answer)

    def random_card(self, other_card: Card=None, overlap: bool=False, minimum_numerator: int=1) -> Card:
        content = None
        suit = None

        if not other_card:
            rand_num = np.random.randint(3)
            if rand_num != 0:
                content = np.random.choice(list(CardContent))
            if rand_num != 1:
                suit = np.random.choice(list(CardSuit))
        elif overlap:
            if other_card.content and other_card.suit:
                if np.random.randint(2):            # face overlap
                    other_card.content, other_card.face = CardContent.FACE, True
                    other_card.suit, other_card.colour = None, False
                    content = np.random.choice(list(CardContent)[-4:-1])
                else:                               # colour overlap
                    other_card.content, other_card.face = None, False
                    other_card.suit, other_card.colour = [CardSuit.BLACK, CardSuit.RED][np.random.randint(2)], True
                    suit = np.random.choice(list(CardSuit)[:-2])
            else:                                   # alternating none for suit and content
                if not other_card.content:
                    content = np.random.choice(list(CardContent))
                else:
                    suit = np.random.choice(list(CardSuit))
        else:
            if other_card.content and other_card.suit:
                rand_num = np.random.randint(3)
                if rand_num != 0:
                    pool = list(CardContent)[:-1]
                    if other_card.face:
                        other_card.content, other_card.face = np.random.choice(pool), False
                    pool.remove(other_card.content)
                    content = np.random.choice(pool)
                if rand_num != 1:
                    pool = list(CardSuit)[:-2]
                    if other_card.colour:
                        other_card.suit, other_card.colour = np.random.choice(pool), False
                    pool.remove(other_card.suit)
                    suit = np.random.choice(pool)
            else:                                   # different only suit or content
                if other_card.content:
                    pool = list(CardContent)
                    pool.remove(other_card.content)
                    content = np.random.choice(pool)
                else:
                    pool = list(CardSuit)
                    pool.remove(other_card.suit)
                    suit = np.random.choice(pool)

        if minimum_numerator and content and suit:
            card = Card(content, suit)
            if minimum_numerator > card.probability:
                if np.random.randint(2):
                    content = None
                else:
                    suit = None

        return Card(content, suit)

    def calc_single_event(self, cards: list[Card]):
        card = cards[0]
        return card.probability / 52

    def calc_counting(self, cards: list[Card], amount: int) -> float:
        card = cards[0]
        return comb(int(card.probability), amount) / comb(52, amount)

    def calc_dependant(self, cards: list[Card], overlap: bool) -> float:
        card1, card2 = cards[0], cards[1]
        if overlap:
            return (card1.probability * (card2.probability - 1)) / (52 * 51)
        return (card1.probability * card2.probability) / (52 * 51)

    def calc_independant(self, cards: list[Card]) -> float:
        card1, card2 = cards[0], cards[1]
        return (card1.probability * card2.probability) / (52 * 52)

    def calc_mut_exc(self, cards: list[Card]) -> float: 
        card1, card2 = cards[0], cards[1]
        return (card1.probability + card2.probability) / 52

    def calc_non_mut_exc(self, cards: list[Card]) -> float:
        card1, card2 = cards[0], cards[1]
        return ((card1.probability + card2.probability) - card1.calc_overlap(card2)) / 52


if __name__ == '__main__':                              # Testing each type
    for q_type in list(ProbabilitiesQuestionType):
        q = ProbabilitiesQuestion(q_type)
        print(q.prompt, q.answer)