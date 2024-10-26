from emo_platform import Client, Tokens
from configs import EnvLoader
env_loader = EnvLoader()


class EmoClient:
    _instance = None
    client = None
    room = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmoClient, cls).__new__(cls)
            cls._instance._create_client()
        return cls._instance

    def _create_client(self):
        self.client = Client(
        	endpoint_url = env_loader.get('PLATFORM_API_URL'),
	        tokens=Tokens(refresh_token = env_loader.get('PLATFORM_API_REFRESH_TOKEN'))
	    )
        self.room = self.client.create_room_client(env_loader.get('ROOM_ID'))
