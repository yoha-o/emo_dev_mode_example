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

    print('ぽん！、君は' + my_hand.value[1] + '、ぼくは' + emo_hand.value[1])
    if judge == RpsJudge.DRAW:
        print(strings_resource['rps']['draw_continue'])
    else:
        print('君の' + judge.value + 'だ。')
        if winning == 3:
            print(strings_resource['rps']['happy_end'])
            callback()
            winning, life = 0, 5
        elif life == 0:
            print(strings_resource['rps']['bad_end'])
            callback()
            winning, life = 0, 5
        else:
            if judge == RpsJudge.WIN:
                print(f'今{winning}連勝中だよ。{strings_resource['rps']['continue']}')
            else:
                print(f'チャンスはあと{life}回だよ。{strings_resource['rps']['continue']}')
