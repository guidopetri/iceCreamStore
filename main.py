#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum
import re
import sys
import traceback
import random
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui
import json

try:
	with open('money.ini','r') as file:
		money = json.loads(file.read())
except:
	money = 5.0
random.seed(1)

class FlavorNames(Enum):
	strawberry='strawberry'
	vanilla='vanilla'
	chocolate='chocolate'

class Qualities(Enum):
	great='great'
	good='good'
	ok='ok'
	bad='bad'
	terrible='terrible'

class iceCream():
	def __init__(self,flavor,quality,quantity):
		self.flavor = flavor
		self.quality = quality
		self.quantity = quantity
		self.empty = False

	def eaten(self,quantity):
		if quantity <= self.quantity:
			self.quantity -= quantity
			if self.quantity == 0:
				self.empty = True
		else:
			raise ValueError("we don't have that much ice cream!")

class sundae():
	def __init__(self,iceCreamsDict):
		self.iceCreamsDict = iceCreamsDict

def isNumber(string):
	if re.match(r'^\d+(\.\d+)?$',string):
		return True
	else:
		return False

def buyIceCream():
	flavorStr = input("which flavor do you want to buy?\n")
	while True:
		try:
			flavor = FlavorNames(flavorStr)
			break;
		except ValueError:
			flavorStr = input("sorry, we don't have that flavor. which flavor do you want to buy instead?\n")
	qualityStr = input("which quality do you want to buy %s ice cream in?\n"%flavor.name)
	while True:
		try:
			quality = Qualities(qualityStr)
			break;
		except ValueError:
			qualityStr = input("sorry, i don't know of anywhere that sells that quality ice cream. which quality would you like to buy instead?\n")
	quantityStr = input("how much %s %s ice cream do you want to buy?\n"%(quality.name,flavor.name))
	while not isNumber(quantityStr):
		quantityStr = input("sorry, i can only understand numbers. how much %s %s ice cream do you want to buy?\n"%(quality.name,flavor.name))
	quantity = float(quantityStr)
	return iceCream(flavor,quality,quantity)

def sellIceCream(tub,price):
	eatAmount = input("how much %s %s ice cream do you want to sell? we still have %s left.\n" %(tub.quality.name,tub.flavor.name,tub.quantity))
	while not isNumber(eatAmount):
		eatAmount = input("sorry, i can only understand numbers. how much %s %s ice cream do you want to sell? we still have %s left.\n" %(tub.quality.name,tub.flavor.name,tub.quantity))
	eatAmount = float(eatAmount)
	try:
		tub.eaten(eatAmount)
		income = eatAmount*price
	except ValueError:
		print(traceback.format_exc())
	return income

def createSundae():
	print([(x.flavor.name,x.quantity) for x in iceCreamTubs if not x.empty])
	iceCreamToCombine1 = input("which ice cream would you like to combine?\n")
	try:
		iceCreamToCombine1 = int(iceCreamToCombine1)
	except ValueError:
		pass
	while True:
			try:
				test = iceCreamTubs[iceCreamToCombine1-1]
				break;
			except:
				iceCreamToCombine1 = input("sorry, try again. which ice cream would you like to combine?\n")
				try:
					iceCreamToCombine1 = int(iceCreamToCombine1)
				except ValueError:
					pass
	amount1 = input("how much of %s ice cream?"%iceCreamTubs[iceCreamToCombine1-1].flavor.name)
	try:
		amount1 = int(amount1)
	except ValueError:
		pass
	while amount1 > iceCreamTubs[iceCreamToCombine1].quantity:
		amount1 = input("sorry, you don't have that much %s ice cream. how much instead?"%iceCreamTubs[iceCreamToCombine1-1].flavor.name)
		try:
			amount1 = int(amount1)
		except ValueError:
			pass
	iceCreamToCombine2 = input("which other ice cream would you like to combine?\n")
	try:
		iceCreamToCombine2 = int(iceCreamToCombine2)
	except ValueError:
		pass
	while True:
			try:
				test = iceCreamTubs[iceCreamToCombine2-1]
				break;
			except:
				iceCreamToCombine2 = input("sorry, try again. which ice cream would you like to combine?\n")
				try:
					iceCreamToCombine2 = int(iceCreamToCombine2)
				except ValueError:
					pass
	amount2 = input("how much of %s ice cream?"%iceCreamTubs[iceCreamToCombine2-1].flavor.name)
	try:
		amount2 = int(amount2)
	except ValueError:
		pass
	while amount2 > iceCreamTubs[iceCreamToCombine2].quantity:
		amount2 = input("sorry, you don't have that much %s ice cream. how much instead?"%iceCreamTubs[iceCreamToCombine2-1].flavor.name)
		try:
			amount2 = int(amount2)
		except ValueError:
			pass
	return sundae({iceCreamTubs[iceCreamToCombine1-1]:amount1,iceCreamTubs[iceCreamToCombine2-1]:amount2})

def sellSundae(sundaeToSell,price):
	income = 0
	for value in sundaeToSell.iceCreamsDict.values():
		income += value*price*1.5
	return income

iceCreamTubs = []
sundaesDict = {}
while True:
	print("you have %s cash left"%money)
	price = random.randrange(1,5)/2
	choice = input("what would you like to do?\n1. buy ice cream\n2. sell ice cream for %s\n3. quit\n4. create sundae\n5. sell sundae\n"%price)
	if choice not in ['1','2','3','4','5']:
		choice = input("try again\n")
	if choice == '1':
		iceCreamTubs.append(buyIceCream())
		money -=1
	elif choice == '2':
		print([(x.flavor.name,x.quantity) for x in iceCreamTubs if not x.empty])
		iceCreamToSell = input("which ice cream would you like to sell?\n")
		while True:
			try:
				test = iceCreamTubs[iceCreamToSell]
				break;
			except IndexError:
				iceCreamToSell = input("sorry, try again. which ice cream would you like to sell?\n")
		money += sellIceCream(iceCreamTubs[iceCreamToSell],price)
	elif choice == '3':
		break;
	elif choice == '4':
		sundaesDict[len(sundaesDict)] = createSundae()
	elif choice == '5':
		money += sellSundae(sundaesDict[len(sundaesDict)-1],price)
with open('money.ini','w') as file:
	json.dump(money,file)
print("exiting!")

sys.exit()
