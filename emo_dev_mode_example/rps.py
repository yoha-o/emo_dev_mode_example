import random as rand
from dataclasses import dataclass
from enums import RpsHand, RpsResult


winning = 0
lose = 0


def choose(my_hand, callback):
    global winning
    global lose

    emo_hand = RpsHand.from_value(rand.randint(0, 2))
    if my_hand == emo_hand:
        callback(RpsStatus(my_hand, emo_hand, RpsResult.DRAW, winning, lose))
    elif my_hand == RpsHand.ROCK:
        if emo_hand == RpsHand.SCISSORS:
            winning += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.WIN, winning, lose))
        elif emo_hand == RpsHand.PAPER:
            winning = 0
            lose += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.LOSE, winning, lose))
    elif my_hand == RpsHand.PAPER:
        if emo_hand == RpsHand.ROCK:
            winning += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.WIN, winning, lose))
        elif emo_hand == RpsHand.SCISSORS:
            winning = 0
            lose += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.LOSE, winning, lose))
    elif my_hand == RpsHand.SCISSORS:
        if emo_hand == RpsHand.PAPER:
            winning += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.WIN, winning, lose))
        elif emo_hand == RpsHand.ROCK:
            winning = 0
            lose += 1
            callback(RpsStatus(my_hand, emo_hand, RpsResult.LOSE, winning, lose))


@dataclass
class RpsStatus:
    my_hand: RpsHand
    emo_hand: RpsHand
    result: RpsResult
    winning: int
    lose: int
