import os
from dotenv import load_dotenv
import json, http.server
from pyngrok import ngrok
from emo_platform import Client, Tokens, WebHook, EmoPlatformError

load_dotenv()
PLATFORM_API_URL = os.getenv('PLATFORM_API_URL')
PLATFORM_API_REFRESH_TOKEN = os.getenv('PLATFORM_API_REFRESH_TOKEN')
HTTP_SERVER_PORT = os.getenv('HTTP_SERVER_PORT')

client = Client(
    endpoint_url = PLATFORM_API_URL,
    tokens=Tokens(refresh_token = PLATFORM_API_REFRESH_TOKEN)
    )

public_url = ngrok.connect(int(HTTP_SERVER_PORT)).public_url
client.create_webhook_setting(WebHook(public_url))


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

class Handler(http.server.BaseHTTPRequestHandler):
	def _send_status(self, status):
		self.send_response(status)
		self.send_header('Content-type', 'text/plain; charset=utf-8')
		self.end_headers()
		
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(b'Hello, World!')
		
	def do_POST(self):
		if not secret_key == self.headers["X-Platform-Api-Secret"]:
			self._send_status(401)
			return
		
		content_len = int(self.headers['content-length'])
		request_body = json.loads(self.rfile.read(content_len).decode('utf-8'))

		try:
			cb_func, emo_webhook_body = client.get_cb_func(request_body)
		except EmoPlatformError:
			self._send_status(501)
			return
		
		cb_func(emo_webhook_body)
		
		self._send_status(200)

with http.server.HTTPServer(('', int(HTTP_SERVER_PORT)), Handler) as httpd:
	httpd.serve_forever()


def main():
    print("Hello, world!")


if __name__ == "__main__":
    main()
