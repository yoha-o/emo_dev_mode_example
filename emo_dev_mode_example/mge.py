import os
from time import sleep
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()

room = emo_client.room


def countdown():
    print(strings_resource['mge']['countdown_begin'])
    for _ in range(10,-1, -1):
        sleep(1)
    print(strings_resource['mge']['countdown_end'])


def detectIntruder(radar, callback):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if radar.begin == True and radar.near_begin == False:
        print(strings_resource['mge']['caution'])
    elif radar.end == True and radar.near_end == False:
        print(strings_resource['mge']['clearup'])
    elif radar.near_begin == True:
        callback()
        audio_alert_path = f'{script_dir}/../assets/alert.mp3'
        room.send_audio_msg(audio_alert_path)
        print(strings_resource['mge']['found'])
        room.send_msg(strings_resource['mge']['found'])
        audio_gameover_path = f'{script_dir}/../assets/gameover.mp3'
        room.send_audio_msg(audio_gameover_path)
