from enums import RpsHand, RpsJudge
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()
room = emo_client.room


class EmoRps:
    winning, life = 0, 5
    gameover_callback = None

    def __init__(self, callback):
        self.gameover_callback = callback

    def do_rps(self, my_hand):
        emo_hand = RpsHand.gen_hand()
        
        if my_hand == emo_hand:
            judge = RpsJudge.DRAW
        elif my_hand == RpsHand.ROCK:
            if emo_hand == RpsHand.SCISSORS:
                self.winning += 1
                judge = RpsJudge.WIN
            elif emo_hand == RpsHand.PAPER:
                self.winning = 0
                self.life -= 1
                judge = RpsJudge.LOSE
        elif my_hand == RpsHand.PAPER:
            if emo_hand == RpsHand.ROCK:
                self.winning += 1
                judge = RpsJudge.WIN
            elif emo_hand == RpsHand.SCISSORS:
                self.winning = 0
                self.life -= 1
                judge = RpsJudge.LOSE
        elif my_hand == RpsHand.SCISSORS:
            if emo_hand == RpsHand.PAPER:
                self.winning += 1
                judge = RpsJudge.WIN
            elif emo_hand == RpsHand.ROCK:
                self.winning = 0
                self.life -= 1
                judge = RpsJudge.LOSE
        
        msg_hands = f'ぽん！、君は{my_hand.value}、ぼくは{emo_hand.value}'
        print(msg_hands)
        # room.send_msg(msg_hands)
        if judge == RpsJudge.DRAW:
            print(strings_resource['rps']['draw_continue'])
            # room.send_msg(strings_resource['rps']['draw_continue'])
            return
        
        msg_result = f'君の{judge.value}だ。'
        print(msg_result)
        # room.send_msg(msg_result)
        if self.winning == 3:
            print(strings_resource['rps']['win_ending'])
            # room.send_msg(strings_resource['rps']['win_ending'])
            self.gameover_callback()
        elif self.life == 0:
            print(strings_resource['rps']['lose_ending'])
            # room.send_msg(strings_resource['rps']['lose_ending'])
            self.gameover_callback()
        else:
            if judge == RpsJudge.WIN:
                msg_winning = f'今{self.winning}連勝中だよ。{strings_resource['rps']['continue']}'
                print(msg_winning)
                # room.send_msg(msg_winning)
                return

            msg_lose = f'チャンスはあと{self.life}回だよ。{strings_resource['rps']['continue']}'
            print(msg_lose)
            # room.send_msg(msg_lose)
