from fastapi import FastAPI, Request
from pyngrok import ngrok
from emo_platform import WebHook, EmoPlatformError
from enums import GameMode, RpsHand, EmonatorAns
from emo_client import EmoClient
from configs import EnvLoader, StringsLoader
import rps
import emonator
import mge


env_loader = EnvLoader()
strings_resource = StringsLoader().resources
emo_client = EmoClient()
app = FastAPI()

client = emo_client.client
room = emo_client.room
game_mode = GameMode.NEUTRAL


# @client.event('trigger_word.detected')
# def trigger_word_callback(body):
# 	print(body)


@client.event('vui_command.detected')
def vui_command_callback(body):
	global game_mode

	if game_mode != GameMode.NEUTRAL:
		game_mode = GameMode.NEUTRAL
		print(strings_resource['emo_games']['cancel'])
		room.send_msg(strings_resource['emo_games']['cancel'])


@client.event('record_button.pressed')
def record_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.RPS
		print(strings_resource['rps']['start'])
		room.send_msg(strings_resource['rps']['start'])
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.ROCK, gameover_callback)
	elif game_mode == GameMode.EMONATOR:
		emonator.answer_question(EmonatorAns.YES, gameover_callback)
	elif game_mode == GameMode.MGE:
		game_mode = GameMode.NEUTRAL
		print(strings_resource['mge']['win_ending'])
		room.send_msg(strings_resource['mge']['win_ending'])


@client.event('play_button.pressed')
def play_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.EMONATOR
		print(strings_resource['emonator']['start'])
		room.send_msg(strings_resource['emonator']['start'])
		emonator.play(gameover_callback)
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.SCISSORS, gameover_callback)
	elif game_mode == GameMode.EMONATOR:
		emonator.answer_question(EmonatorAns.NO, gameover_callback)
	elif game_mode == GameMode.MGE:
		mge.countdown()


@client.event('function_button.pressed')
def function_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.MGE
		print(strings_resource['mge']['start'])
		room.send_msg(strings_resource['mge']['start'])
	elif game_mode == GameMode.EMONATOR:
		emonator.answer_question(EmonatorAns.IDK, gameover_callback)
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.PAPER, gameover_callback)


@client.event('accel.detected')
def accel_sensor_callback(body):
	global game_mode

	if game_mode == GameMode.NEUTRAL and body.data.accel.kind == 'upside_down':
		game_mode = GameMode.SELECT
		print(strings_resource['emo_games']['start'])
		room.send_msg(strings_resource['emo_games']['start'])
	elif game_mode == GameMode.EMONATOR:
		if body.data.accel.kind == 'lift':
			emonator.answer_question(EmonatorAns.PY, gameover_callback)
		elif body.data.accel.kind == 'lying_down':
			emonator.answer_question(EmonatorAns.PN, gameover_callback)
		elif body.data.accel.kind == 'shaken':
			emonator.answer_question(EmonatorAns.BACK, gameover_callback)
	

# @client.event('illuminance.changed')
# def illuminance_sensor_callback(body):
# 	print(body)


@client.event('radar.detected')
def radar_sensor_callback(body):
	if game_mode == GameMode.MGE:
		mge.detectIntruder(body.data.radar, gameover_callback)



def gameover_callback():
	global game_mode
	game_mode = GameMode.NEUTRAL


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
	public_url = ngrok.connect(int(env_loader.get('HTTP_SERVER_PORT'))).public_url
	client.create_webhook_setting(WebHook(public_url))
	uvicorn.run('main:app', host=env_loader.get('HTTP_SERVER_HOST'), port=int(env_loader.get('HTTP_SERVER_PORT')))


if __name__ == '__main__':
	main()
