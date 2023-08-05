# -*- coding: utf-8 -*-
""" Provides the Game class as part of the PokerNowLogConverter data model """

import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, DefaultDict

from action import Action
from card import Card
from hand import Hand
from player import Player
from seat import Seat
from utils import currencyCCToSymbol


class Game:
    """ A class representing a game of poker, which is comprised of many hands of poker.

    The Game class is initialised using a list of strings which comprise a PokerNow log. The initialiser reads the
    log line by line, creating Hand objects for each hand in the log, which are stored in a list of hands.

    Once the game object is initialised, the hero name or aliases can be set, which propagates to each hand in the list.

    Finally, the game can be output in the desired format (currently only PokerStars format) using the
    format_as_pokerstars_log() function.

    Attributes:
        self.hand_list (List[Hand]): The list of hands that happened during this game.
        self.currency (str): The currency used during this game. (e.g GBP)
        self.currency_symbol (str): The currency symbol used during this game. (e.g £)
        self.timezone (str): The timezone of this game (e.g GMT)
        self.original_file_path (str): If this game was constructed using a log file, this contains the path.
        self.seen_players (Set[Player]): The set of players observed in all of the hands in this game. It is
                                         calculated after all hands have been constructed.

    """

    def __init__(self, poker_now_log: List[List[str]], currency: str = "USD", timezone: str = "ET",
                 original_filename: str = None):
        """ The initialiser for a game object. Requires PokerNow log strings as input to parse

        Args:
            poker_now_log (List[List[str]]): The list of PokerNow log lines to parse.
            currency (str): The currency used in this game (e.g USD)
            timezone (str): The timezone of this game (e.g GMT)
            original_filename (str): If this game was constructed using a log file, this contains the path.
        """
        self.hand_list: List[Hand] = []
        self.currency: str = currency
        self.currency_symbol: str = currencyCCToSymbol[currency]
        self.timezone: str = timezone
        self.original_file_path: str = original_filename

        # The hand currently being parsed during initialisation. This initial Hand object won't actually be
        # used, it should encounter a -- starting hand -- statement straight away.
        current_hand: Hand = Hand()
        # The game state of the hand being parsed
        current_hand_state: str = "before Flop"
        # The current largest bet in this street of the hand being parsed
        current_hand_street_max_bet: float = 0

        # Helper dictionary to keep track of what a given player did last in this hand while parsing.
        # The key is the player_name_with_id attribute.
        prev_action_dict: DefaultDict[str, float] = defaultdict(float)
        street_action_dict: Dict[str, List[Action]] = {}

        # Iterate over the log, building a new Hand object for each played hand
        for row in poker_now_log:
            line = row[0]

            if "-- starting hand " in line:
                # Initialise new hand object
                current_hand = Hand()
                prev_action_dict = defaultdict(float)
                street_action_dict = {"before Flop": current_hand.pre_flop_actions,
                                      "on the Flop": current_hand.flop_actions,
                                      "on the Turn": current_hand.turn_actions,
                                      "on the River": current_hand.river_actions,
                                      "at Showdown": current_hand.showdown_actions}
                current_hand_state = "before Flop"
                current_hand_street_max_bet = 0

                if "Hold\'em" in line:
                    current_hand.hand_type = "Hold\'em No Limit"
                else:
                    current_hand.hand_type = "Omaha Pot Limit"

                if "dealer:" in line:
                    dealer_name_with_id = line.split("dealer: \"")[1].split("\") --")[0]
                    dealer_name = dealer_name_with_id.split(" @ ")[0]
                    dealer_id = dealer_name_with_id.split(" @ ")[1]
                    current_hand.dealer = Player(player_name=dealer_name, player_name_with_id=dealer_name_with_id,
                                                 player_id=dealer_id)

                current_hand.hand_start_datetime = datetime.fromisoformat(row[1][:-1])
                current_hand.hand_number = int(line.split("hand #")[1].split(" (")[0])

            elif "-- ending hand " in line:
                self.hand_list.append(current_hand)
                if current_hand.dealer:
                    current_hand.get_seat_by_player_name_with_id(
                        current_hand.dealer.player_name_with_id).seat_desc += " (button)"

            elif "raises" in line:
                line = line.replace(" and go all in", "")
                line = line.replace(" and all in", "")
                line = line.replace("with ", "to ")
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                raise_amount = float(line.split("to ")[1])
                difference = raise_amount - current_hand_street_max_bet
                current_hand_street_max_bet = raise_amount
                prev_action_dict[player_name_with_id] = raise_amount

                street_action_dict[current_hand_state].append(
                    Action(player=p_obj, bet_amount=raise_amount, bet_difference=difference, action="raise"))

                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                if p_seat:
                    p_seat.seat_did_bet = True

            elif "bets" in line:
                line = line.replace(" and go all in", "")
                line = line.replace(" and all in", "")
                line = line.replace(" with", "")
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                bet_amount = float(line.split("bets ")[1])
                current_hand_street_max_bet = bet_amount
                prev_action_dict[player_name_with_id] = bet_amount

                street_action_dict[current_hand_state].append(Action(player=p_obj, bet_amount=bet_amount, action="bet"))

                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                if p_seat:
                    p_seat.seat_did_bet = True

            elif "calls" in line:
                line = line.replace(" and go all in", "")
                line = line.replace(" and all in", "")
                line = line.replace(" with", "")
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                call_amount = float(line.split("calls ")[1])
                difference = call_amount - prev_action_dict[player_name_with_id]
                prev_action_dict[player_name_with_id] = call_amount

                street_action_dict[current_hand_state].append(
                    Action(player=p_obj, bet_amount=difference, action="call"))

                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                if p_seat:
                    p_seat.seat_did_bet = True

            elif "checks" in line:
                # print(line)
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)

                street_action_dict[current_hand_state].append(Action(player=p_obj, action="check"))

                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                if p_seat:
                    p_seat.seat_did_bet = True

            elif line.startswith("Uncalled bet"):
                player_name_with_id = line.split(" \"")[1].split("\"")[0]
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                uncalled_bet_amount = float(line.split("Uncalled bet of ")[1].split(" returned")[0])
                current_hand.uncalledBetSize = uncalled_bet_amount
                current_hand_street_max_bet -= uncalled_bet_amount

                street_action_dict[current_hand_state].append(
                    Action(player=p_obj, bet_amount=uncalled_bet_amount, action="uncalled bet"))

                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                if p_seat:
                    p_seat.seat_did_bet = True

            elif "folds" in line:
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                p_seat.seat_summary = f"folded {current_hand_state}"
                if not p_seat.seat_did_bet:
                    p_seat.seat_summary += " (didn\'t bet)"

                street_action_dict[current_hand_state].append(Action(player=p_obj, action="fold"))

            elif " big blind of " in line:
                line = line.replace(" and go all in", "")
                line = line.replace("missed ", "")
                big_blind_amount = float(line.split("\" posts a big blind of ")[1])
                big_blind_player_name_with_id = line.split("\" ")[0].split("\"")[1]
                # big_blind_player_name = line.split("\" ")[0].split("\"")[1].split(" @ ")[0]
                big_blind_seat = next((seat for seat in current_hand.seats if
                                       seat.seat_player.player_name_with_id == big_blind_player_name_with_id), None)
                big_blind_seat.seat_did_bet = True
                big_blind_seat.seat_desc = " (big blind)"
                if big_blind_amount > current_hand_street_max_bet:
                    current_hand_street_max_bet = big_blind_amount
                prev_action_dict[big_blind_player_name_with_id] = big_blind_amount

                current_hand.big_blind_seats.append(big_blind_seat)
                current_hand.big_blind_amount = big_blind_amount
                current_hand.big_blind_players.append(
                    current_hand.get_player_by_player_name_with_id(big_blind_player_name_with_id))

            elif " small blind of " in line:
                line = line.replace(" and go all in", "")
                if "missing " in line:
                    line = line.replace("missing ", "")
                    small_blind_amount = float(line.split("\" posts a small blind of ")[1])
                    small_blind_player_name_with_id = line.split("\" ")[0].split("\"")[1]
                    # small_blind_player_name = line.split("\" ")[0].split("\"")[1].split(" @ ")[0]
                    small_blind_seat = current_hand.get_seat_by_player_name_with_id(small_blind_player_name_with_id)
                    small_blind_seat.seat_did_bet = True
                    small_blind_seat.seat_desc = " (small blind)"
                    if small_blind_amount > current_hand_street_max_bet:
                        current_hand_street_max_bet = small_blind_amount
                    prev_action_dict[small_blind_player_name_with_id] = small_blind_amount

                    current_hand.missing_small_blinds.append(
                        current_hand.get_player_by_player_name_with_id(small_blind_player_name_with_id))
                else:
                    small_blind_amount = float(line.split("\" posts a small blind of ")[1])
                    small_blind_player_name_with_id = line.split("\" ")[0].split("\"")[1]
                    # small_blind_player_name = line.split("" ")[0].split(""")[1].split(" @ ")[0]
                    small_blind_seat = next((seat for seat in current_hand.seats if
                                             seat.seat_player.player_name_with_id == small_blind_player_name_with_id),
                                            None)
                    small_blind_seat.seat_did_bet = True
                    small_blind_seat.seat_desc = " (small blind)"
                    if small_blind_amount > current_hand_street_max_bet:
                        current_hand_street_max_bet = small_blind_amount
                    prev_action_dict[small_blind_player_name_with_id] = small_blind_amount

                    current_hand.small_blind_seat = small_blind_seat
                    current_hand.small_blind_amount = small_blind_amount
                    current_hand.small_blind_player = current_hand.get_player_by_player_name_with_id(
                        small_blind_player_name_with_id)

            elif line.startswith("Players stacks"):
                # Legacy log format has an s on Players (and other changes)
                seat_number = 0
                players = line.split("Players stacks: ")[1].split(" | ")
                for player in players:
                    seat_number += 1
                    player_name_with_id = player.split("\"")[1].split("\"")[0]
                    player_name = player_name_with_id.split(" @ ")[0]
                    player_id = player_name_with_id.split(" @ ")[1]
                    player_obj = Player(player_name=player_name, player_name_with_id=player_name_with_id,
                                        player_id=player_id)
                    stack_size = int(player.split("\" (")[1].split(")")[0])

                    current_hand.players.append(player_obj)
                    current_hand.seats.append(
                        Seat(seat_player=player_obj, seat_number=seat_number, stack_size=stack_size))

            elif line.startswith("Player stacks"):
                players = line.split("Player stacks: ")[1].split(" | ")
                for player in players:
                    player_name_with_id = player.split(" \"")[1].split("\"")[0]
                    player_name = player_name_with_id.split(" @ ")[0]
                    player_id = player_name_with_id.split(" @ ")[1]
                    player_obj = Player(player_name=player_name, player_name_with_id=player_name_with_id,
                                        player_id=player_id)
                    seat_number = int(player.split(" \"")[0].split("#")[1])
                    stack_size = int(player.split("\" (")[1].split(")")[0])

                    current_hand.players.append(player_obj)
                    current_hand.seats.append(
                        Seat(seat_player=player_obj, seat_number=seat_number, stack_size=stack_size))
            elif line.startswith("Your hand"):
                hole_cards = [Card(x) for x in line.split("Your hand is ")[1].split(", ")]
                # list(
                # map(lambda x: Card(x), line.split("Your hand is ")[1].split(", ")))
                current_hand.hole_cards = hole_cards
            elif line.startswith("flop:") or line.startswith("Flop:"):
                flop_cards = [Card(x) for x in line.split("[")[1].split("]")[0].split(", ")]
                # flop_cards = list(
                #     map(lambda x: Card(x), line.split("[")[1].split("]")[0].split(", ")))
                current_hand.flop_cards = flop_cards
                current_hand.board.extend(flop_cards)
                current_hand_state = "on the Flop"
                current_hand_street_max_bet = 0
                prev_action_dict = defaultdict(float)
            elif line.startswith("turn:") or line.startswith("Turn:"):
                turn_card = Card(line.split("[")[1].split("]")[0])
                current_hand.turn_card = turn_card
                current_hand.board.append(turn_card)
                current_hand_state = "on the Turn"
                current_hand_street_max_bet = 0
                prev_action_dict = defaultdict(float)
            elif line.startswith("river:") or line.startswith("River:"):
                river_card = Card(line.split("[")[1].split("]")[0])
                current_hand.river_card = river_card
                current_hand.board.append(river_card)
                current_hand_state = "on the River"
                current_hand_street_max_bet = 0
                prev_action_dict = defaultdict(float)
            elif "\" shows a " in line:
                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)

                cards = f"[{' '.join(list(map(lambda x: Card(x).card_str, line.split('shows a ')[1].split('.')[0].split(', '))))}]"
                p_seat.seat_hole_cards = cards

                street_action_dict[current_hand_state].append(Action(player=p_obj, action="show", cards_shown=cards))

            elif "\" collected " in line or "\" gained " in line or " wins " in line:
                line = line.replace("gained", "collected")
                current_hand_state = "at Showdown"

                if " wins " in line:
                    # Legacy log format
                    collected_amount = float(line.split("\" wins ")[1].split(" with")[0])
                else:
                    collected_amount = float(line.split("\" collected ")[1].split(" from pot")[0])

                # PokerNow seems to calculate collected amount wrong when there are missing small blinds, so subtract
                # them here
                # TODO: What happens with a split pot and missing small blind?
                if len(current_hand.missing_small_blinds) > 0:
                    collected_amount -= (current_hand.small_blind_amount * len(current_hand.missing_small_blinds))

                current_hand.total_pot += collected_amount

                player_name_with_id = line.split("\" ")[0].split("\"")[1]
                p_seat = current_hand.get_seat_by_player_name_with_id(player_name_with_id)
                p_seat.collected_amount += collected_amount

                p_obj = current_hand.get_player_by_player_name_with_id(player_name_with_id)
                street_action_dict[current_hand_state].append(
                    Action(player=p_obj, action="collect", bet_amount=collected_amount))

                if " with " in line:
                    if "(hand: " in line:
                        hole_cards = " ".join(
                            list(map(lambda x: Card(x).card_str, line.split("(hand: ")[1].split(")")[0].split(", "))))
                        p_seat.seat_hole_cards = f"[{hole_cards}]"

                    winning_hand = line.split("with ")[1].split(" (")[0]
                    p_seat.seat_summary = f"showed {p_seat.seat_hole_cards} and won " \
                                          f"({self.currency_symbol}{p_seat.collected_amount:,.2f}) " \
                                          f"with {winning_hand}"
                else:
                    p_seat.seat_summary = f"collected ({self.currency_symbol}{p_seat.collected_amount:,.2f})"

            else:
                if not (
                        "joined" in line or "requested" in line or "quits" in line or "created" in line
                        or "approved" in line or "changed" in line or "enqueued" in line or " stand up " in line
                        or " sit back " in line or " canceled the seat " in line):
                    logging.warning("State not considered: %s", line)

            if current_hand:
                current_hand.raw_strings.append(line)

        self.seen_players = set()
        self.refresh_seen_players()

    def set_hero(self, player_name: str):
        """ Sets the hero for every hand in this game.

        This function should be called before outputting a log, as otherwise the "Dealt [cards] to Hero" line
        will not be correct.

        Args:
            player_name (str): This can either be in the PokerNow default format of "Player @ ID" or an alias
                can be used instead, as long as the alias has already been set previously.

        Returns:
            int: Returns the number of hands in which this hero was located.
            This is useful for identifying if the hero was not input correctly (or an alias was not set correctly).
        """
        found_hero_count = 0
        for hand in self.hand_list:
            found = hand.set_hero(player_name)
            if found:
                found_hero_count += 1
        return found_hero_count

    def update_player_aliases(self, player_name_with_id: str, alias: str):
        """ Adds an alias to player mapping to every hand in this game.

        Once an alias is set, it will be used instead of the old "Player @ ID" format when outputting as a new log.
        If a player does not have an alias when the game is output, the standard "Player @ ID" will be used instead.

        Args:
            player_name_with_id (str): The player name in the logs, should be in the format "Player @ ID"
            alias (str): The new name which this player will now be known as.
        Returns:
            int: Returns the number of hands in which this player was located.
            This is useful for identifying if the player name was not set correctly.
        """
        found_match_count = 0
        for hand in self.hand_list:
            player = hand.get_player_by_player_name_with_id(player_name_with_id)
            if player:
                found_match_count += 1
                player.alias_name = alias
        return found_match_count

    def find_hand_with_player(self, player: Player):
        """ Finds any hand that contains a certain player

        Used by the interactive mode to show an example hand containing a player, to aid identification.

        Args:
            player (obj:Player): The player of interest

        Returns:
            obj:Hand: Returns the Hand this player was found in, or None if the player is not found in any hand.
        """
        for hand in self.hand_list:
            if player in hand.players:
                return hand
        return None

    def refresh_seen_players(self):
        """Updates the seen_players class attribute, checking all hands in the hand list."""
        self.seen_players = set()
        for hand in self.hand_list:
            for player in hand.players:
                self.seen_players.add(player)

    def format_as_pokerstars_log(self) -> List[str]:
        """ Converts a Game object to a list of strings representing each hand in the game in the PokerStars format

        Returns:
            List[str]: A list of strings representing the game. Each hand is output in turn, with three blank lines
            separating hands.
        """
        output_lines = []

        for hand in self.hand_list:
            hand_pokerstars_output = hand.format_as_pokerstars_hand(currency=self.currency,
                                                                    currency_symbol=self.currency_symbol,
                                                                    timezone=self.timezone)
            output_lines.extend(hand_pokerstars_output)

            # End with blank lines
            output_lines.append("")
            output_lines.append("")
            output_lines.append("")

        return output_lines
