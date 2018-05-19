#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

import json

def loadMoney():
	try:
		with open('money.ini','r') as file:
			money = json.loads(file.read())
	except IOError:
		money = 5.0
	return money

def saveMoney(money):
	with open('money.ini','w') as file:
		json.dump(money,file)
	return

def saveScore(score):
	with open('highscore.ini','w') as file:
		json.dump(score,file)
	return

def loadScore():
	try:
		with open('highscore.ini','r') as file:
			score = json.loads(file.read())
	except IOError:
		score = 0
	return score