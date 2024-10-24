import os
from fastapi import FastAPI, Request
from pyngrok import ngrok
from emo_platform import Client, Tokens, WebHook, EmoPlatformError
from enums import GameMode, RpsHand, RpsResult
from configs import EnvLoader, StringsLoader
import rps


env_loader = EnvLoader()
strings_loader = StringsLoader()

app = FastAPI()
client = Client(
	endpoint_url = env_loader.get('PLATFORM_API_URL'),
	tokens=Tokens(refresh_token = env_loader.get('PLATFORM_API_REFRESH_TOKEN'))
	)
room = client.create_room_client(env_loader.get('ROOM_ID'))

game_mode = GameMode.NEUTRAL


# @client.event('trigger_word.detected')
# def trigger_word_callback(body):
# 	print(body)


@client.event('vui_command.detected')
def vui_command_callback(body):
	global game_mode

	if game_mode != GameMode.NEUTRAL:
		game_mode = GameMode.NEUTRAL
		strings_loader._strings_resource
		print(strings_loader._strings_resource['emo_games']['cancel'])


@client.event('record_button.pressed')
def record_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.RPS
		print(strings_loader._strings_resource['rps']['start'])
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.ROCK, rps_callback)
	if game_mode == GameMode.MGE:
		game_mode = GameMode.NEUTRAL
		print(strings_loader._strings_resource['emo_games']['happy_end'])


@client.event('play_button.pressed')
def play_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.EMONATOR
		print('エモネイター開始')
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.PAPER, rps_callback)


@client.event('function_button.pressed')
def function_button_callback(body):
	global game_mode

	if game_mode == GameMode.SELECT:
		game_mode = GameMode.MGE
		print(strings_loader._strings_resource['mge']['start'])
	elif game_mode == GameMode.RPS:
		rps.choose(RpsHand.SCISSORS, rps_callback)


@client.event('accel.detected')
def accel_sensor_callback(body):
	global game_mode

	if game_mode == GameMode.NEUTRAL and body.data.accel.kind == 'upside_down':
		game_mode = GameMode.SELECT
		print(strings_loader._strings_resource['emo_games']['start'])
	

# @client.event('illuminance.changed')
# def illuminance_sensor_callback(body):
# 	print(body)


@client.event('radar.detected')
def radar_sensor_callback(body):
	global game_mode

	if game_mode == GameMode.MGE:
		script_dir = os.path.dirname(os.path.abspath(__file__))
		if body.data.radar.begin == True and body.data.radar.near_begin == False:
			print(strings_loader._strings_resource['mge']['caution'])
		elif body.data.radar.end == True and body.data.radar.near_end == False:
			print(strings_loader._strings_resource['mge']['clearup'])
		elif game_mode == GameMode.MGE and body.data.radar.near_begin == True:
			game_mode = GameMode.NEUTRAL
			audio_alert_path = f'{script_dir}/../assets/alert.mp3'
			room.send_audio_msg(audio_alert_path)
			print(strings_loader._strings_resource['mge']['found'])
			room.send_msg(strings_loader._strings_resource['mge']['found'])
			audio_gameover_path = f'{script_dir}/../assets/gameover.mp3'
			room.send_audio_msg(audio_gameover_path)


def rps_callback(status):
	global game_mode

	print('ぽん！、君は' + status.my_hand.value[1] + '、ぼくは' + status.emo_hand.value[1])
	if status.result == RpsResult.DRAW:
		print(strings_loader._strings_resource['rps']['draw_continue'])
	else:
		print('君の' + status.result.value + 'だ。')
		if status.winning == 3:
			print(strings_loader._strings_resource['emo_games']['happy_end'])
			game_mode = GameMode.NEUTRAL
		elif status.life == 0:
			print(strings_loader._strings_resource['emo_games']['bad_end'])
			game_mode = GameMode.NEUTRAL
		else:
			if status.result == RpsResult.WIN:
				print(f'今{status.winning}連勝中だよ。{strings_loader._strings_resource['rps']['continue']}')
			else:
				print(f'チャンスはあと{status.life}回だよ。{strings_loader._strings_resource['rps']['continue']}')


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
