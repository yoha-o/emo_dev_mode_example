from enum import Enum


class GameMode(Enum):
	NEUTRAL = 0
	SELECT = 1
	RPS = 2
	EMONATOR = 3
	MGE = 4


class RpsHand(Enum):
	ROCK = (0, 'グー')
	SCISSORS = (1, 'チョキ')
	PAPER = (2, 'パー')

	@classmethod
	def from_value(cls, value):
		for item in cls:
			if item.value[0] == value:
			    return item 


class RpsJudge(Enum):
	DRAW = 'あいこ'
	WIN = 'かち'
	LOSE = 'まけ'
