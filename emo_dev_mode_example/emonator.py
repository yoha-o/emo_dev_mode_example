from akinator_python import Akinator
from enums import EmonatorAns
from emo_client import EmoClient
from configs import StringsLoader


akinator = Akinator()
strings_resource = StringsLoader().resources
emo_client = EmoClient()
room = emo_client.room

isFinalQuestion = False


def play(callback):
    akinator.start_game()
    try:
        print(akinator.question)
    except Exception as _:
        callback()
        print(strings_resource['emo_games']['error'])


def answer_question(ans, callback):
    global isFinalQuestion

    print(f'回答：{ans.value[1]}')
    if isFinalQuestion:
        isFinalQuestion = False
        if ans == EmonatorAns.NO:
            # akinator.exclude()
            callback()
            print(strings_resource['emonator']['incorrect_ans'])
        elif ans == EmonatorAns.YES:
            callback()
            print(strings_resource['emonator']['correct_ans'])
        else:
            callback()
            print(strings_resource['emonator']['correct_ans'])
    else:
        try:
            if ans == EmonatorAns.BACK:
                akinator.go_back()
                print(akinator.question)
            else:
                akinator.post_answer(ans.value[0])
                print(akinator.question)
                if akinator.answer_id:
                    isFinalQuestion = True
                    print(f'君が思い浮かべているのは・・・{akinator.description}の{akinator.name}だね？合っていたらおなかの上のボタン、違っていたら真ん中のボタンを押してね。')
        except Exception as _:
            callback()
            print(strings_resource['emo_games']['error'])
