#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum
import re
import sys
import traceback
import random

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

money = 5.0
iceCreamTubs = []
while True:
	print("you have %s cash left"%money)
	price = random.randrange(1,5)/2
	choice = input("what would you like to do?\n1. buy ice cream\n2. sell ice cream for %s\n3. quit\n"%price)
	if choice not in ['1','2','3']:
		choice = input("try again\n")
	if choice == '1':
		iceCreamTubs.append(buyIceCream())
		money -=1
	elif choice == '2':
		try:
			money += sellIceCream([x for x in iceCreamTubs if not x.empty][0],price)
		except IndexError:
			print("you don't have any ice cream to sell!")
	elif choice == '3':
		break;

print("you ate all the ice cream!")

sys.exit()