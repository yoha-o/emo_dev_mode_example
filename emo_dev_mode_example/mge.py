import os
from time import sleep
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()
room = emo_client.room


class MetalGearEmo:
    gameover_callback = None

    def __init__(self, callback):
        self.gameover_callback = callback

    def countdown():
        room.send_msg(strings_resource['mge']['countdown_begin'])
        for _ in range(10,-1, -1):
            sleep(1)
        room.send_msg(strings_resource['mge']['countdown_end'])


    def detectIntruder(self, radar):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if radar.begin == True and radar.near_begin == False:
            room.send_msg(strings_resource['mge']['caution'])
        elif radar.end == True and radar.near_end == False:
            room.send_msg(strings_resource['mge']['clearup'])
        elif radar.near_begin == True:
            self.gameover_callback()
            audio_alert_path = f'{script_dir}/../assets/alert.mp3'
            room.send_audio_msg(audio_alert_path)
            room.send_msg(strings_resource['mge']['found'])
            audio_gameover_path = f'{script_dir}/../assets/gameover.mp3'
            room.send_audio_msg(audio_gameover_path)
