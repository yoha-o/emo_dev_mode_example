from enum import Enum
import random as rand


class GameMode(Enum):
	NEUTRAL = 0
	SELECT = 1
	RPS = 2
	EMONATOR = 3
	MGE = 4


class RpsHand(Enum):
	ROCK = ('グー')
	SCISSORS = ('チョキ')
	PAPER = ('パー')

	@classmethod
	def gen_hand(cls):
		rps_id = rand.randint(0, 2)
		match rps_id:
			case 0: return RpsHand.ROCK
			case 1: return RpsHand.SCISSORS
			case 2: return RpsHand.PAPER


class RpsJudge(Enum):
	DRAW = 'あいこ'
	WIN = 'かち'
	LOSE = 'まけ'


class EmonatorAns(Enum):
	YES = ('y', 'はい')
	NO = ('n', 'いいえ')
	IDK = ('idk', 'わからない')
	PY = ('p', 'たぶんそう・部分的にそう')
	PN = ('pn', 'たぶん違う・そうでもない')
	BACK = ('b', '前の質問に戻る')
