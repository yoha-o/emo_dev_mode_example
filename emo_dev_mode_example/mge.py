import os
from time import sleep
from emo_client import EmoClient
from configs import StringsLoader


strings_resource = StringsLoader().resources
emo_client = EmoClient()
room = emo_client.room
script_dir = os.path.dirname(os.path.abspath(__file__))


class MetalGearEmo:
    during_game = False
    guard_level = 0
    unchanged_time = 0
    gameover_callback = None

    def __init__(self, callback):
        self.gameover_callback = callback

    def countdown(self, callback):
        print(strings_resource['mge']['countdown_begin'])
        room.send_msg(strings_resource['mge']['countdown_begin'])
        for _ in range(10,-1, -1):
            sleep(1)
        print(strings_resource['mge']['countdown_end'])
        room.send_msg(strings_resource['mge']['countdown_end'])
        self.during_game = True
        callback()

    def count_unchanged(self):
        while True:
            if not self.during_game: break
            sleep(1)
            self.unchanged_time += 1
            if self.unchanged_time == 20:
                if self.guard_level > 0:
                    self.guard_level -= 1
                    self._clearup_intruder()
                self.unchanged_time = 0
                

    def detect_illuminance_intruder(self, illuminance):
        if not self.during_game : return
        self.guard_level += 1
        self.unchanged_time = 0
        if self.guard_level >= 2:
            self._find_intruder()
        else:
            self._caution_intruder()

    def detect_radar_intruder(self, radar):
        print(radar)
        if not self.during_game : return
        if radar.near_begin:
            self._find_intruder()
            return

        if radar.begin:
            self.guard_level += 1
            self.unchanged_time = 0
            if self.guard_level >= 2:
                self._find_intruder()
            else:
                self._caution_intruder()
        if radar.end:
            if self.guard_level > 0:
                self.guard_level -= 1
                self.unchanged_time = 0
                self._clearup_intruder()

    def detect_door_intruder(self):
        if not self.during_game : return
        self.guard_level += 1
        self.unchanged_time = 0
        if self.guard_level >= 2:
            self._find_intruder()
        else:
            self._caution_intruder()

    def detect_human_intruder(self):
        if not self.during_game : return
        self.guard_level += 1
        self.unchanged_time = 0
        if self.guard_level >= 2:
            self._find_intruder()
        else:
            self._caution_intruder()

    def push_bocco_button(self):
        if not self.during_game : return
        self.gameover_callback
        self.during_game = False
        print(strings_resource['mge']['win_ending'])
        room.send_msg(strings_resource['mge']['win_ending'])

    def _caution_intruder(self):
        print(strings_resource['mge']['caution'])
        room.send_msg(strings_resource['mge']['caution'])

    def _clearup_intruder(self):
        print(strings_resource['mge']['clearup'])
        room.send_msg(strings_resource['mge']['clearup'])

    def _find_intruder(self):
        self.gameover_callback()
        self.during_game = False
        audio_alert_path = f'{script_dir}/../assets/alert.mp3'
        room.send_audio_msg(audio_alert_path)
        print(strings_resource['mge']['found'])
        room.send_msg(strings_resource['mge']['found'])
        audio_gameover_path = f'{script_dir}/../assets/gameover.mp3'
        room.send_audio_msg(audio_gameover_path)
