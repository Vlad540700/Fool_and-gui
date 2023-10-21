import random
from typing import Any, List, Union

from gui_fool_game import set_number_players, select_card_gui, answer_game


class Player:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def return_name(self) -> str:
        return self.name


class Card:
    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return self.rank + self.suit

    def return_card_name(self) -> str:
        return self.rank + self.suit

    def __eq__(self, other: Union['Card', 'TrumpСard']) -> bool:
        return self.rank == other.rank and self.suit == other.suit


class TrumpСard(Card):
    def __init__(self, rank, suit, trump=True) -> None:
        super().__init__(rank, suit)
        self.trump = trump


class Hand:
    def __init__(self) -> None:
        self.__cards = []

    def __str__(self) -> str:
        if self.__cards:
            rep = ""
            for card in self.__cards:
                rep += str(card) + '\t'
        else:
            rep = '<пусто>'
        return rep

    def list_cards_in_hand(self) -> List[Union[Card, TrumpСard]]:
        return self.__cards

    def number_of_cards(self) -> int:
        return len(self.__cards)

    def clear(self):
        self.__cards = []

    def add(self, card: Union[Card, TrumpСard]):
        self.__cards.append(card)

    def removal(self, card: Union[Card, TrumpСard]):
        self.__cards.remove(card)

    def give(self, card: Union[Card, TrumpСard], other_hand: 'Hand'):
        self.__cards.remove(card)
        other_hand.add(card)


class Table(Hand):
    def discard_card_table(self, hand: Hand, card: Union[Card, TrumpСard]):
        hand.removal(card)
        self.add(card)

    def checking_table_rank(self, card: Union[Card, TrumpСard]) -> bool:
        detector = False
        for i in self.list_cards_in_hand():
            if i.rank == card.rank:
                detector = True
        return detector

    def take_cards_table(self, hand: Hand):
        for rounds in range(self.number_of_cards()):
            if self.list_cards_in_hand():
                top_card = self.list_cards_in_hand[0]
                self.give(top_card, hand)


class Game:
    face_value_cards = {
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["S", "H", "D", "C"]

    def __init__(self):
        self.__players: List[Player] = []
        self.__hands: List[Hand] = []
        self.__trump_suit = random.choice(self.SUITS)
        self.__deck: List[Union[Card, TrumpСard]] = []

    def game_settings(self) -> int:
        num, name_players = set_number_players()
        players = []
        hands = []
        for i in range(num):
            player = Player(name_players[i])
            players.append(player)
            hand = Hand()
            hands.append(hand)
        self.__players = players
        self.__hands = hands
        self.create_shuffle_distribute()
        return self.first_one_walks()

    def create_an_ordered_deck_of_cards(self):
        for suit in self.SUITS:
            for rank in self.RANKS:
                if suit == self.__trump_suit:
                    self.__deck.append(TrumpСard(rank, suit))
                else:
                    self.__deck.append(Card(rank, suit))

    def shuffle_deck(self):
        random.shuffle(self.__deck)

    def deal_cards_up_to_6(self):
        i = 0
        for hand in self.__hands:
            if self.number_of_cards_in_hand(i) < 6:
                for rounds in range(6-self.number_of_cards_in_hand(i)):
                    if self.__deck:
                        top_card = self.__deck[0]
                        self.__deck.remove(top_card)
                        hand.add(top_card)
            i += 1

    def create_shuffle_distribute(self):
        self.create_an_ordered_deck_of_cards()
        self.shuffle_deck()
        self.deal_cards_up_to_6()

    def number_of_cards_in_hand(self, player_index: int) -> int:
        return self.__hands[player_index].number_of_cards()

    def first_one_walks(self) -> int:
        minimum_trump_card = self.face_value_cards["A"]
        player_index = ''
        trump_card_present = False
        for person in range(len(self.__players)):
            trumps_hand = []
            for card_ in self.__hands[person].list_cards_in_hand():
                if type(card_) == TrumpСard:
                    trumps_hand.append(card_.rank)
            if trumps_hand:
                trump_card_present = True
                for j in range(len(trumps_hand)):
                    if trumps_hand[j] in self.face_value_cards:
                        trumps_hand[j] = self.face_value_cards[trumps_hand[j]]
                minimum_value_in_hand = min(trumps_hand)
                if minimum_value_in_hand <= minimum_trump_card:
                    minimum_trump_card = minimum_value_in_hand
                    player_index = person
        if trump_card_present is False:
            self.create_shuffle_distribute()
            self.first_one_walks()
        else:
            return player_index

    def order_of_move(self, player_index: int, variant: int) -> int:
        if variant == 1:
            if player_index == len(self.__players)-1:
                player_index = 0
            else:
                player_index += 1
        elif variant == 2:
            if player_index == 0:
                player_index = len(self.__players)-1
            else:
                player_index -= 1
        return player_index

    def compare_face_value_cards(
            self, protection_card: str, attack_card: str
    ) -> bool:
        a1 = None
        a2 = None
        if protection_card in self.face_value_cards:
            a1 = self.face_value_cards[protection_card]
        if attack_card in self.face_value_cards:
            a2 = self.face_value_cards[attack_card]
        if a2 < a1:
            return True
        return False

    def toss_card_to_taker(self, player_index: int, playing_field: Table):
        throw_card_loser = select_card_gui(
            *self.get_player_information(player_index, playing_field),
            1
        )
        while throw_card_loser != "Bito":
            selected_game_card = self.return_card_class(throw_card_loser)
            if playing_field.checking_table_rank(selected_game_card):
                playing_field.discard_card_table(
                    self.__hands[player_index],
                    selected_game_card
                )
            throw_card_loser = select_card_gui(
                *self.get_player_information(player_index, playing_field),
                1
            )

    def protect_yourself_card(
            self, player_index: int, playing_field: Table, game_card: str
    ) -> int:
        selected_game_card = self.return_card_class(game_card)
        if (playing_field.list_cards_in_hand()[-1].suit
                == selected_game_card.suit):
            if self.compare_face_value_cards(
                selected_game_card.rank,
                playing_field.list_cards_in_hand()[-1].rank
            ):
                player_index = self.make_turn(
                    selected_game_card, player_index, playing_field, 2
                )
        elif (
            playing_field.list_cards_in_hand()[-1].suit
            != selected_game_card.suit and
            type(selected_game_card) == TrumpСard
        ):
            player_index = self.make_turn(
                selected_game_card, player_index, playing_field, 2
            )
        return player_index

    def attack_or_bito(
            self,
            player_index: int,
            playing_field: Table,
            option: int
    ) -> str:
        return select_card_gui(
            *self.get_player_information(player_index, playing_field),
            option
        )

    def selected_card_from_hand_fistandgui(
            self,
            player_index: int,
            playing_field: List[Any],
            option=0
    ) -> Union[TrumpСard, Card]:
        select_card = select_card_gui(
            *self.get_player_information(player_index, playing_field),
            option
        )
        return self.return_card_class(select_card)

    def first_move(self, player_index: int, playing_field: Table) -> int:
        selected_game_card = self.selected_card_from_hand_fistandgui(
            player_index,
            playing_field
        )
        return self.make_turn(
            selected_game_card, player_index, playing_field, 1
        )

    def take_cards_table(self, player_index: int, table: Table):
        for rounds in range(table.number_of_cards()):
            if table.list_cards_in_hand():
                top_card = table.list_cards_in_hand()[0]
                table.give(top_card, self.__hands[player_index])

    def win_and_answer_game(self, player_index: int) -> str:
        name_player = self.__players[player_index].return_name()
        return answer_game(name_player)

    def attack_card_in_table(
            self,
            player_index: int,
            playing_field: Table,
            game_card: str
    ) -> int:
        select_card = self.return_card_class(game_card)
        if playing_field.checking_table_rank(select_card):
            player_index = self.make_turn(
                select_card, player_index, playing_field, 1
            )
        return player_index

    def get_player_information(
            self, player_index: int, playing_field: Table
    ) -> tuple:
        name_player = self.__players[player_index].return_name()
        cards_on_table = playing_field.list_cards_in_hand()
        cards_on_hand = [
            card.return_card_name()
            for card in self.__hands[player_index].list_cards_in_hand()
        ]
        number_cards_deck = len(self.__deck)
        trump_suit = self.__trump_suit
        return (
            name_player,
            cards_on_table,
            cards_on_hand,
            number_cards_deck,
            trump_suit
        )

    def return_card_class(self, game_card: str) -> Union[TrumpСard, Card]:
        if game_card[-1] == self.__trump_suit:
            return TrumpСard(game_card[0:-1], game_card[-1])
        else:
            return Card(game_card[0:-1], game_card[-1])

    def make_turn(
            self,
            selected_game_card: Union[Card, TrumpСard],
            player_index: int,
            playing_field: Table,
            order_variant: int
    ) -> int:
        playing_field.discard_card_table(
            self.__hands[player_index], selected_game_card
        )
        player_index = self.order_of_move(player_index, order_variant)
        return player_index


def main():
    match = Game()
    player_index = match.game_settings()
    playing_field = Table()
    while match.number_of_cards_in_hand(player_index) > 0:
        if playing_field.number_of_cards() == 0:
            player_index = match.first_move(player_index, playing_field)
        elif playing_field.number_of_cards() % 2 == 1:
            take_the_cards = match.attack_or_bito(
                player_index,
                playing_field,
                2
            )
            if take_the_cards == 'Takecards':
                player_index = match.order_of_move(
                    player_index,
                    2
                )
                match.toss_card_to_taker(player_index, playing_field)
                if match.number_of_cards_in_hand(player_index) == 0:
                    continue
                player_index = match.order_of_move(
                    player_index,
                    1
                )
                match.take_cards_table(player_index, playing_field)
                player_index = match.order_of_move(
                    player_index,
                    1
                )
                match.deal_cards_up_to_6()
                continue
            else:
                player_index = match.protect_yourself_card(
                    player_index,
                    playing_field,
                    take_the_cards
                )
        elif (
            playing_field.number_of_cards() % 2 == 0 and
            playing_field.number_of_cards() != 0
        ):
            bito = match.attack_or_bito(player_index, playing_field, 1)
            if bito == 'Bito':
                playing_field.clear()
                player_index = match.order_of_move(
                    player_index,
                    1
                )
                match.deal_cards_up_to_6()
                continue
            else:
                player_index = match.attack_card_in_table(
                    player_index,
                    playing_field,
                    bito
                )
    again = match.win_and_answer_game(player_index)

    if again == 'Yes':
        main()


if __name__ == '__main__':
    main()
