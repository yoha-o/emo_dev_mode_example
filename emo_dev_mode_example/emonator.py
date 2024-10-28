from akinator_python import Akinator
from enums import EmonatorAns
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()
room = emo_client.room


class Emonator:
    akinator = Akinator()
    isFinalQuestion = False
    gameover_callback = None

    def __init__(self, callback):
        self.gameover_callback = callback

    def play(self):
        self.akinator.start_game()
        try:
            msg_q = self.akinator.question
            print(msg_q)
            # room.send_msg(msg_q)
        except Exception as _:
            self.gameover_callback()
            print(strings_resource['emo_games']['error'])
            # room.send_msg(strings_resource['emo_games']['error'])

    def answer_question(self, ans):
        print(f'回答：{ans.value[1]}')
        if self.isFinalQuestion:
            if ans == EmonatorAns.NO:
                # akinator.exclude()
                self.gameover_callback()
                print(strings_resource['emonator']['incorrect_ans'])
                # room.send_msg(strings_resource['emonator']['incorrect_ans'])
            elif ans == EmonatorAns.YES:
                self.gameover_callback()
                print(strings_resource['emonator']['correct_ans'])
                # room.send_msg(strings_resource['emonator']['correct_ans'])
            else:
                self.gameover_callback()
                print(strings_resource['emonator']['correct_ans'])
                # room.send_msg(strings_resource['emonator']['correct_ans'])
        else:
            try:
                if ans == EmonatorAns.BACK:
                    self.akinator.go_back()
                    q = self.akinator.question
                    print(q)
                    # room.send_msg(q)
                else:
                    self.akinator.post_answer(ans.value[0])
                    if self.akinator.answer_id:
                        self.isFinalQuestion = True
                        msg_final_q = f'君が思い浮かべているのは・・・{self.akinator.description}の{self.akinator.name}だね？合っていたらおなかの上のボタン、違っていたら真ん中のボタンを押してね。'
                        print(msg_final_q)
                        # room.send_msg(msg_final_q)
                    else:
                        q = self.akinator.question
                        print(q)
                        # room.send_msg(q)
            except Exception as _:
                self.gameover_callback()
                print(strings_resource['emo_games']['error'])
                # room.send_msg(strings_resource['emo_games']['error'])
