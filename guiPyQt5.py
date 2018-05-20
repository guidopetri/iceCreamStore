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
		self.createToolbar()
		self.mainScreen()
		self.show()
		return

	def createToolbar(self):
		mainAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/icecream.png'),'Main',self)
		mainAct.triggered.connect(self.mainScreen)
		
		sundaeAct = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon('media/sundae.png'),'Sundae',self)
		sundaeAct.triggered.connect(self.sundaeScreen)

		self.toolbar = self.addToolBar('Toolbar')
		self.toolbar.setMovable(False)
		self.toolbar.addAction(mainAct)
		self.toolbar.addAction(sundaeAct)
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
		self.actionComboBox.currentIndexChanged.connect(self.updateMainItemCombo)

		self.amountComboBox = PyQt5.QtWidgets.QComboBox()
		self.itemComboBox.currentIndexChanged.connect(self.updateMainAmountCombo)

		self.runButton = PyQt5.QtWidgets.QPushButton('Do it')
		self.runButton.clicked.connect(lambda:self.buyIceCream() if self.actionComboBox.currentText()=='Buy' else self.sellIceCream())

		self.nextDayButton = PyQt5.QtWidgets.QPushButton('Next day')
		self.nextDayButton.clicked.connect(self.nextDay)
		self.nextDayButton.clicked.connect(self.updateMainItemCombo)
		self.nextDayButton.clicked.connect(self.updateMainAmountCombo)

		self.gridMain = PyQt5.QtWidgets.QGridLayout()
		self.resize(400,150)
		self.gridMain.addWidget(self.moneyLabel,0,0,1,3)
		self.gridMain.addWidget(self.highScoreLabel,0,3,1,3)
		self.gridMain.addWidget(self.actionLabel,1,0,1,2)
		self.gridMain.addWidget(self.itemLabel,1,2,1,2)
		self.gridMain.addWidget(self.amountLabel,1,4,1,2)
		self.gridMain.addWidget(self.actionComboBox,2,0,1,2)
		self.gridMain.addWidget(self.itemComboBox,2,2,1,2)
		self.gridMain.addWidget(self.amountComboBox,2,4,1,2)
		self.gridMain.addWidget(self.priceLabel,3,0,1,3)
		self.gridMain.addWidget(self.dayLabel,3,3,1,3)
		self.gridMain.addWidget(self.runButton,4,0,1,3)
		self.gridMain.addWidget(self.nextDayButton,4,3,1,3)

		self.updateMainItemCombo()
		self.updateMainAmountCombo()

		self.mainWidget = PyQt5.QtWidgets.QWidget(self)
		self.mainWidget.setLayout(self.gridMain)
		self.setCentralWidget(self.mainWidget)
		return

	def sundaeScreen(self):
		self.iceCream1Label = PyQt5.QtWidgets.QLabel('Ice cream')
		self.iceCream1Label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.iceCream2Label = PyQt5.QtWidgets.QLabel('Ice cream')
		self.iceCream2Label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.resultLabel = PyQt5.QtWidgets.QLabel('Result')
		self.resultLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.iceCream1Combo = PyQt5.QtWidgets.QComboBox()
		self.iceCream1Amount = PyQt5.QtWidgets.QComboBox()
		self.iceCream1HBox = PyQt5.QtWidgets.QHBoxLayout()
		self.iceCream1HBox.addWidget(self.iceCream1Combo)
		self.iceCream1HBox.addWidget(self.iceCream1Amount)
		self.iceCream2Combo = PyQt5.QtWidgets.QComboBox()
		self.iceCream2Amount = PyQt5.QtWidgets.QComboBox()
		self.iceCream2HBox = PyQt5.QtWidgets.QHBoxLayout()
		self.iceCream2HBox.addWidget(self.iceCream2Combo)
		self.iceCream2HBox.addWidget(self.iceCream2Amount)
		self.plusLabel = PyQt5.QtWidgets.QLabel('+')
		self.plusLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.equalsLabel = PyQt5.QtWidgets.QLabel('=')
		self.equalsLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
		self.sundaeName = PyQt5.QtWidgets.QLineEdit()
		self.createButton = PyQt5.QtWidgets.QPushButton('Create!')

		self.updateIceCreamSundaeCombos()
		self.updateAmountSundaeCombos()

		self.iceCream1Combo.currentIndexChanged.connect(self.updateAmountSundaeCombos)
		self.iceCream2Combo.currentIndexChanged.connect(self.updateAmountSundaeCombos)
		self.createButton.clicked.connect(self.createSundae)

		self.gridSundae = PyQt5.QtWidgets.QGridLayout()
		self.gridSundae.setRowStretch(0,1)
		#self.resize(400,100)
		self.gridSundae.addWidget(self.iceCream1Label,1,0,1,1)
		self.gridSundae.addWidget(self.iceCream2Label,1,2,1,1)
		self.gridSundae.addWidget(self.resultLabel,1,4,1,1)
		self.gridSundae.addLayout(self.iceCream1HBox,2,0,1,1)
		self.gridSundae.addWidget(self.plusLabel,2,1,1,1)
		self.gridSundae.addLayout(self.iceCream2HBox,2,2,1,1)
		self.gridSundae.addWidget(self.equalsLabel,2,3,1,1)
		self.gridSundae.addWidget(self.sundaeName,2,4,1,1)
		self.gridSundae.addWidget(self.createButton,3,4,1,1)

		self.sundaeWidget = PyQt5.QtWidgets.QWidget(self)
		self.sundaeWidget.setLayout(self.gridSundae)
		self.setCentralWidget(self.sundaeWidget)

	def createSundae(self):
		if self.iceCream1Combo.currentText() == self.iceCream2Combo.currentText():
			maxQuantity = self.iceCreamTubs[self.iceCream1Combo.currentText()].quantity
			if (int(self.iceCream1Amount.currentText())+int(self.iceCream2Amount.currentText())) <= maxQuantity:
				self.sundaes[self.sundaeName.text()] = classes.sundae({self.iceCream1Combo.currentText():int(self.iceCream1Amount.currentText())+int(self.iceCream2Amount.currentText())},1)
			else:
				dialog = lackOfIceCreamDialog()
				dialog.show()
				dialog.exec_()
				return
		else:
			self.sundaes[self.sundaeName.text()] = classes.sundae({self.iceCream1Combo.currentText():int(self.iceCream1Amount.currentText()),self.iceCream2Combo.currentText():int(self.iceCream2Amount.currentText())},1)
		self.iceCreamTubs[self.iceCream1Combo.currentText()].eaten(int(self.iceCream1Amount.currentText()))
		self.iceCreamTubs[self.iceCream2Combo.currentText()].eaten(int(self.iceCream2Amount.currentText()))
		self.updateIceCreamSundaeCombos()
		self.sundaeName.clear()
		return

	def updateIceCreamSundaeCombos(self):
		for item in self.iceCreamTubs.values():
			if item.quantity >= 1:
				self.iceCream1Combo.addItem(item.flavor.value)
				self.iceCream2Combo.addItem(item.flavor.value)
		return

	def updateAmountSundaeCombos(self):
		self.iceCream1Amount.clear()
		self.iceCream2Amount.clear()
		try:
			self.iceCream1Amount.addItems([str(number) for number in range(1,self.iceCreamTubs[self.iceCream1Combo.currentText()].quantity+1)])
		except KeyError:
			self.iceCream1Amount.addItem('0')
		try:
			if self.iceCream1Combo.currentText() == self.iceCream2Combo.currentText():
				self.iceCream2Amount.addItems([str(number) for number in range(0,self.iceCreamTubs[self.iceCream2Combo.currentText()].quantity)])
			else:
				self.iceCream2Amount.addItems([str(number) for number in range(1,self.iceCreamTubs[self.iceCream2Combo.currentText()].quantity+1)])
		except KeyError:
			self.iceCream2Amount.addItem('0')
		return

	def updateMainItemCombo(self):
		if self.actionComboBox.currentText() == 'Buy':
			self.itemComboBox.clear()
			self.itemComboBox.addItems([x for x in self.iceCreamTubs.keys()])
		elif self.actionComboBox.currentText() == 'Sell':
			self.itemComboBox.clear()
			self.itemComboBox.addItems([x.flavor.value for x in self.iceCreamTubs.values()])
			self.itemComboBox.addItems([x for x in self.sundaes.keys()])
		return

	def updateMainAmountCombo(self):
		if self.actionComboBox.currentText() == 'Buy':
			self.amountComboBox.clear()
			self.amountComboBox.addItems([str(x) for x in range(1,int(self.money/self.price)+1)])
		elif self.actionComboBox.currentText() == 'Sell':
			self.amountComboBox.clear()
			try:
				self.amountComboBox.addItems([str(x) for x in range(1,self.iceCreamTubs[self.itemComboBox.currentText()].quantity+1)])
			except KeyError:
				try:
					self.amountComboBox.addItems([str(x) for x in range(1,self.sundaes[self.itemComboBox.currentText()].count+1)])
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
		self.sundaes = {}
		for item in classes.FlavorNames:
			self.iceCreamTubs[item.value] = classes.iceCream(item,classes.Qualities('great'),0)
		self.date = 1
		return

	def buyIceCream(self):
		if self.money >= self.price*int(self.amountComboBox.currentText()):
			self.iceCreamTubs[classes.FlavorNames(self.itemComboBox.currentText()).value].add(int(self.amountComboBox.currentText())) # = classes.iceCream(classes.FlavorNames(self.itemComboBox.currentText()),classes.Qualities('great'),int(self.amountComboBox.currentText()))
			self.money -= self.price*int(self.amountComboBox.currentText())
			self.moneyLabel.setText('Money: %s'%self.money)
			self.updateMainAmountCombo()
		else:
			dialog = lackOfFundsDialog()
			dialog.show()
			dialog.exec_()
		return

	def sellIceCream(self):
		try:
			attempt = self.iceCreamTubs[self.itemComboBox.currentText()]
			self.money += self.price*int(self.amountComboBox.currentText())
			self.iceCreamTubs[self.itemComboBox.currentText()].eaten(int(self.amountComboBox.currentText()))
			self.moneyLabel.setText('Money: %s'%self.money)
			self.updateMainAmountCombo()
		except KeyError:
			attempt = self.sundaes[self.itemComboBox.currentText()]
			income = sum([x*self.price*1.5 for x in attempt.iceCreamsDict.values()])
			self.money += income
			attempt.count = 0
			self.moneyLabel.setText('Money: %s'%self.money)
			self.updateMainAmountCombo()
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

class lackOfIceCreamDialog(PyQt5.QtWidgets.QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Message')
		textLabel = PyQt5.QtWidgets.QLabel("You don't have enough ice cream for that!")
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