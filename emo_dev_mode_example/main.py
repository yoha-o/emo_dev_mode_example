import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pyngrok import ngrok
from emo_platform import Client, Tokens, WebHook, EmoPlatformError


load_dotenv()
PLATFORM_API_URL = os.getenv('PLATFORM_API_URL')
PLATFORM_API_REFRESH_TOKEN = os.getenv('PLATFORM_API_REFRESH_TOKEN')
HTTP_SERVER_PORT = os.getenv('HTTP_SERVER_PORT')

app = FastAPI()
client = Client(
	endpoint_url = PLATFORM_API_URL,
	tokens=Tokens(refresh_token = PLATFORM_API_REFRESH_TOKEN)
	)


@client.event('trigger_word.detected')
def trigger_word_callback(data):
	print(data)

@client.event('vui_command.detected')
def vui_command_callback(data):
	print(data)

@client.event('record_button.pressed')
def record_button_callback(data):
	print(data)

@client.event('play_button.pressed')
def play_button_callback(data):
	print(data)

@client.event('function_button.pressed')
def function_button_callback(data):
	print(data)

@client.event('accel.detected')
def accel_sensor_callback(data):
	print(data)

@client.event('illuminance.changed')
def illuminance_sensor_callback(data):
	print(data)

@client.event('radar.detected')
def radar_sensor_callback(data):
	print(data)

@client.event('function_button.pressed')
def function_button_callback(data):
	print(data)


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
		return {'message': 'success'}


def main():
	import uvicorn
	public_url = ngrok.connect(int(HTTP_SERVER_PORT)).public_url
	client.create_webhook_setting(WebHook(public_url))
	uvicorn.run(app, host='0.0.0.0', port=int(HTTP_SERVER_PORT))


if __name__ == '__main__':
	main()
