import os
from typing import Any
from enum import Enum
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pyngrok import ngrok
from emo_platform import Client, Tokens, WebHook, EmoPlatformError


load_dotenv()
PLATFORM_API_URL = os.getenv('PLATFORM_API_URL')
PLATFORM_API_REFRESH_TOKEN = os.getenv('PLATFORM_API_REFRESH_TOKEN')
HTTP_SERVER_HOST = os.getenv('HTTP_SERVER_HOST')
HTTP_SERVER_PORT = os.getenv('HTTP_SERVER_PORT')
ROOM_ID = os.getenv('ROOM_ID')

app = FastAPI()
client = Client(
	endpoint_url = PLATFORM_API_URL,
	tokens=Tokens(refresh_token = PLATFORM_API_REFRESH_TOKEN)
	)
room = client.create_room_client(ROOM_ID)

class GameMode(Enum):
	NEUTRAL = 0
	SELECT = 1
	RPS = 2
	EMONATOR = 3
	MGE = 4

game_mode = GameMode.NEUTRAL


@client.event('trigger_word.detected')
def trigger_word_callback(body):
	print(body)

@client.event('vui_command.detected')
def vui_command_callback(body):
	print(body)
	# script_dir = os.path.dirname(os.path.abspath(__file__))
	# audio_data_path = f'{script_dir}/../assets/gameover.mp3'
	# room.send_audio_msg(audio_data_path)
	global game_mode
	if game_mode != GameMode.NEUTRAL:
		game_mode = GameMode.NEUTRAL
		print('ゲームを中止')

@client.event('record_button.pressed')
def record_button_callback(body):
	global game_mode
	if game_mode == GameMode.SELECT:
		game_mode = GameMode.RPS
		print('emoちゃんじゃんけん開始')

@client.event('play_button.pressed')
def play_button_callback(body):
	global game_mode
	if game_mode == GameMode.SELECT:
		game_mode = GameMode.EMONATOR
		print('エモネイター開始')

@client.event('function_button.pressed')
def function_button_callback(body):
	global game_mode
	if game_mode == GameMode.SELECT:
		game_mode = GameMode.MGE
		print('メタルギアエモちゃん開始')

@client.event('accel.detected')
def accel_sensor_callback(body):
	global game_mode
	if game_mode == GameMode.NEUTRAL and body.data.accel.kind == 'upside_down':
		game_mode = GameMode.SELECT
		print('ゲーム開始')
	

# @client.event('illuminance.changed')
# def illuminance_sensor_callback(body):
# 	print(body)

@client.event('radar.detected')
def radar_sensor_callback(body):
	print(body)


secret_key = client.start_webhook_event()

@app.get('/health')
async def do_submit():
	return {'health': 'OK'}

@app.post('/')
async def receive_webhook(request: Request):
	if secret_key == request.headers['X-Platform-Api-Secret']:
		body = await request.json()
		try:
			cb_func, emo_webhook_body = client.get_cb_func(body)
		except EmoPlatformError:
			return {'message': 'emo platform error'}
		cb_func(emo_webhook_body)


def main():
	import uvicorn
	public_url = ngrok.connect(int(HTTP_SERVER_PORT)).public_url
	client.create_webhook_setting(WebHook(public_url))
	uvicorn.run('main:app', host=HTTP_SERVER_HOST, port=int(HTTP_SERVER_PORT), reload=True)


if __name__ == '__main__':
	main()
