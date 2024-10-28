import random as rand
from enums import RpsHand, RpsJudge
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()

room = emo_client.room
winning, life = 0, 5


def choose(my_hand, callback):
    global winning, life

    emo_hand = RpsHand.from_value(rand.randint(0, 2))
    judge = None

    if my_hand == emo_hand:
        judge = RpsJudge.DRAW
    elif my_hand == RpsHand.ROCK:
        if emo_hand == RpsHand.SCISSORS:
            winning += 1
            judge = RpsJudge.WIN
        elif emo_hand == RpsHand.PAPER:
            winning = 0
            life -= 1
            judge = RpsJudge.LOSE
    elif my_hand == RpsHand.PAPER:
        if emo_hand == RpsHand.ROCK:
            winning += 1
            judge = RpsJudge.WIN
        elif emo_hand == RpsHand.SCISSORS:
            winning = 0
            life -= 1
            judge = RpsJudge.LOSE
    elif my_hand == RpsHand.SCISSORS:
        if emo_hand == RpsHand.PAPER:
            winning += 1
            judge = RpsJudge.WIN
        elif emo_hand == RpsHand.ROCK:
            winning = 0
            life -= 1
            judge = RpsJudge.LOSE
    
    _result(my_hand, emo_hand, judge, callback)


def _result(my_hand, emo_hand, judge, callback):
    global winning, life

    msg_hands = f'ぽん！、君は{my_hand.value[1]}、ぼくは{emo_hand.value[1]}'
    print(msg_hands)
    room.send_msg(msg_hands)
    if judge == RpsJudge.DRAW:
        print(strings_resource['rps']['draw_continue'])
        room.send_msg(strings_resource['rps']['draw_continue'])
    else:
        msg_result = f'君の{judge.value}だ。'
        print(msg_result)
        room.send_msg(msg_result)
        if winning == 3:
            print(strings_resource['rps']['win_ending'])
            room.send_msg(strings_resource['rps']['win_ending'])
            callback()
            winning, life = 0, 5
        elif life == 0:
            print(strings_resource['rps']['lose_ending'])
            room.send_msg(strings_resource['rps']['lose_ending'])
            callback()
            winning, life = 0, 5
        else:
            if judge == RpsJudge.WIN:
                msg_winning = f'今{winning}連勝中だよ。{strings_resource['rps']['continue']}'
                print(msg_winning)
                room.send_msg(msg_winning)
            else:
                msg_lose = f'チャンスはあと{life}回だよ。{strings_resource['rps']['continue']}'
                print(msg_lose)
                room.send_msg(msg_lose)
