#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

import classes
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtGui
import files
import random

class MainWindow(PyQt5.QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.init_backend()
		self.init_UI()
		return

	def init_UI(self):
		self.resize(400,150)
		self.center()
		self.setWindowTitle('Ice cream for everyone!')
		self.mainScreen()
		self.show()
		return

	def mainScreen(self):
		self.actionLabel = PyQt5.QtWidgets.QLabel('Action')
		self.actionLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.itemLabel = PyQt5.QtWidgets.QLabel('Item')
		self.itemLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.amountLabel = PyQt5.QtWidgets.QLabel('Amount')
		self.amountLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.moneyLabel = PyQt5.QtWidgets.QLabel('Money: %s'%self.money)
		self.moneyLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.priceLabel = PyQt5.QtWidgets.QLabel('Ice cream price: %s'%self.price)
		self.priceLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.highScoreLabel = PyQt5.QtWidgets.QLabel('High Score: %s'%self.highScore)
		self.highScoreLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.dayLabel = PyQt5.QtWidgets.QLabel('Day: %s'%self.date)
		self.dayLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

		self.actionComboBox = PyQt5.QtWidgets.QComboBox()
		self.actionComboBox.addItems(['Buy','Sell'])

		self.itemComboBox = PyQt5.QtWidgets.QComboBox()
		self.actionComboBox.currentIndexChanged.connect(self.updateItemCombo)

		self.amountComboBox = PyQt5.QtWidgets.QComboBox()
		self.itemComboBox.currentIndexChanged.connect(self.updateAmountCombo)

		self.runButton = PyQt5.QtWidgets.QPushButton('Do it')
		self.runButton.clicked.connect(lambda:self.buyIceCream() if self.actionComboBox.currentText()=='Buy' else self.sellIceCream())

		self.nextDayButton = PyQt5.QtWidgets.QPushButton('Next day')
		self.nextDayButton.clicked.connect(self.nextDay)
		self.nextDayButton.clicked.connect(self.updateItemCombo)
		self.nextDayButton.clicked.connect(self.updateAmountCombo)

		self.grid = PyQt5.QtWidgets.QGridLayout()
		self.grid.addWidget(self.moneyLabel,0,0,1,3)
		self.grid.addWidget(self.highScoreLabel,0,3,1,3)
		self.grid.addWidget(self.actionLabel,1,0,1,2)
		self.grid.addWidget(self.itemLabel,1,2,1,2)
		self.grid.addWidget(self.amountLabel,1,4,1,2)
		self.grid.addWidget(self.actionComboBox,2,0,1,2)
		self.grid.addWidget(self.itemComboBox,2,2,1,2)
		self.grid.addWidget(self.amountComboBox,2,4,1,2)
		self.grid.addWidget(self.priceLabel,3,0,1,3)
		self.grid.addWidget(self.dayLabel,3,3,1,3)
		self.grid.addWidget(self.runButton,4,0,1,3)
		self.grid.addWidget(self.nextDayButton,4,3,1,3)

		self.updateItemCombo()
		self.updateAmountCombo()

		self.mainWidget = PyQt5.QtWidgets.QWidget(self)
		self.mainWidget.setLayout(self.grid)
		self.setCentralWidget(self.mainWidget)
		return

	def updateItemCombo(self):
		if self.actionComboBox.currentText() == 'Buy':
			self.itemComboBox.clear()
			self.itemComboBox.addItems([x.value for x in classes.FlavorNames])
		elif self.actionComboBox.currentText() == 'Sell':
			self.itemComboBox.clear()
			self.itemComboBox.addItems([x.flavor.value for x in self.iceCreamTubs.values()])
		return

	def updateAmountCombo(self):
		if self.actionComboBox.currentText() == 'Buy':
			self.amountComboBox.clear()
			self.amountComboBox.addItems([str(x) for x in range(1,int(self.money/self.price)+1)])
		elif self.actionComboBox.currentText() == 'Sell':
			self.amountComboBox.clear()
			try:
				self.amountComboBox.addItems([str(x) for x in range(1,self.iceCreamTubs[self.itemComboBox.currentText()].quantity+1)])
			except KeyError:
				self.amountComboBox.addItems([str(0)])
		if self.amountComboBox.currentText() == '':
			self.runButton.setEnabled(False)
		else:
			self.runButton.setEnabled(True)
		return

	def center(self):
		qr = self.frameGeometry()
		cp = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		return

	def init_backend(self):
		self.money = files.loadMoney()
		self.price = random.randrange(1,6)/2
		self.highScore = files.loadScore()
		self.iceCreamTubs = {}
		for item in classes.FlavorNames:
			self.iceCreamTubs[item.value] = classes.iceCream(item,classes.Qualities('great'),0)
		self.date = 1
		return

	def buyIceCream(self):
		if self.money >= self.price*int(self.amountComboBox.currentText()):
			self.iceCreamTubs[classes.FlavorNames(self.itemComboBox.currentText()).value].add(int(self.amountComboBox.currentText())) # = classes.iceCream(classes.FlavorNames(self.itemComboBox.currentText()),classes.Qualities('great'),int(self.amountComboBox.currentText()))
			self.money -= self.price*int(self.amountComboBox.currentText())
			self.moneyLabel.setText('Money: %s'%self.money)
			self.updateAmountCombo()
		else:
			dialog = lackOfFundsDialog()
			dialog.show()
			dialog.exec_()
		return

	def sellIceCream(self):
		self.money += self.price*int(self.amountComboBox.currentText())
		self.iceCreamTubs[self.itemComboBox.currentText()].eaten(int(self.amountComboBox.currentText()))
		self.moneyLabel.setText('Money: %s'%self.money)
		self.updateAmountCombo()
		return

	def nextDay(self):
		if self.date == 7:
			dialog = finishGameDialog(self.money,self.highScore)
			dialog.show()
			dialog.exec_()
			PyQt5.QtWidgets.qApp.quit()
		if self.date < 7:
			self.price = random.randrange(1,6)/2
			self.priceLabel.setText('Ice cream price: %s'%self.price)
			self.date +=1
			self.dayLabel.setText('Day: %s'%self.date)
		if self.date == 7:
			self.nextDayButton.setText('Finish game')
		return

class lackOfFundsDialog(PyQt5.QtWidgets.QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Message')
		textLabel = PyQt5.QtWidgets.QLabel("You don't have enough money for that!")
		buttonOk = PyQt5.QtWidgets.QPushButton('Darn it!')
		buttonOk.clicked.connect(self.done)

		grid = PyQt5.QtWidgets.QGridLayout()
		grid.addWidget(textLabel,0,0)
		grid.addWidget(buttonOk,1,0)
		self.setLayout(grid)
		return

class finishGameDialog(PyQt5.QtWidgets.QDialog):
	def __init__(self,money,highScore):
		super().__init__()
		self.setWindowTitle('Congrats!')
		if money == highScore:
			textLabel = PyQt5.QtWidgets.QLabel("You made %s! You tied the high score of %s!"%(money,highScore))
		elif money < highScore and highScore-money < 10:
			textLabel = PyQt5.QtWidgets.QLabel("You made %s! That's so close to the high score of %s!"%(money,highScore))
		elif money < highScore:
			textLabel = PyQt5.QtWidgets.QLabel("You made %s! A long way until the high score of %s!"%(money,highScore))
		elif money > highScore:
			textLabel = PyQt5.QtWidgets.QLabel("You made %s! You beat the high score of %s!"%(money,highScore))
			files.saveScore(money)
		buttonOk = PyQt5.QtWidgets.QPushButton('Finish game')
		buttonOk.clicked.connect(self.done)

		grid = PyQt5.QtWidgets.QGridLayout()
		grid.addWidget(textLabel,0,0)
		grid.addWidget(buttonOk,1,0)
		self.setLayout(grid)
		return