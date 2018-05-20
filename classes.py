#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

from enum import Enum

class FlavorNames(Enum):
	strawberry='Strawberry'
	vanilla='Vanilla'
	chocolate='Chocolate'

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
		return

	def eaten(self,quantity):
		if quantity <= self.quantity:
			self.quantity -= quantity
			if self.quantity == 0:
				self.empty = True
		else:
			raise ValueError("we don't have that much ice cream!")
		return

	def add(self,quantity):
		self.quantity += quantity
		return

class sundae():
	def __init__(self,iceCreamsDict,count):
		self.iceCreamsDict = iceCreamsDict
		self.count = count
		return
