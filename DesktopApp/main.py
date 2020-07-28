import sys
import json
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMainWindow, QApplication, QButtonGroup
from main_design_code import Ui_MainWindow

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.true = 0
        self.false = 0
        self.setGeometry(550,130,880,840)
        self.ui.btnBrowse.clicked.connect(self.onClickedBrowse)
        self.ui.btnAsk.clicked.connect(self.onClickedOrientation)
        self.ui.btnCheck.clicked.connect(lambda : self.onClickedCheck(key,val))
        self.ui.btnFinish.clicked.connect(self.onClickedFinish)
        self.ui.btnAdd.clicked.connect(lambda : self.addWord(file_))
        self.ui.btnDelete.clicked.connect(lambda : self.deleteWord(file_))
        self.ui.btnSave.clicked.connect(lambda : self.saveFile(file_))
        self.ui.btnCreate.clicked.connect(self.createFile)
        self.ui.rbWordDefinition.pressed.connect(self.onClickedAsk)
        self.ui.rbDefinitionWord.pressed.connect(self.onClickedAsk2)

        self.group = QButtonGroup()
        self.group.addButton(self.ui.rbWordDefinition)
        self.group.addButton(self.ui.rbDefinitionWord) 

        try:
            self.ui.wordInput.returnPressed.connect(lambda : self.onClickedCheck(key,val))
            self.ui.etAddDefinition.returnPressed.connect(lambda : self.addWord(file_))
            self.ui.etDeleteWord.returnPressed.connect(lambda : self.deleteWord(file_))
            self.ui.etFilneName.returnPressed.connect(lambda : self.saveFile(file_))
        except KeyError:
            pass

    def createFile(self):
        global file_
        file_ = {}
        global tempFile
        tempFile = {}
        self.ui.lblFileCreated.setText("Your file has been created. Before you can start the game, you must add a word below. You can save your file later if you wish.")
        self.ui.btnAdd.setEnabled(True)
        if len(file_) > 0:
            self.ui.btnSave.setEnabled(True)
            self.ui.btnAsk.setEnabled(True)
        return file_

    def saveFile(self, file_):
        fileName = self.ui.etFilneName.text()
        try:
            with open(fileName, "w", encoding="utf-8") as f:
                json.dump(file_, f)
                self.ui.lblFileSaved.setText(f"File {fileName} has been saved.")
        except FileNotFoundError:
            self.ui.lblFileSaved.setText("The filename cannot be a space. Please enter a usable name.")
        return file_

    def deleteWord(self, file_):
        wordToDeleted = self.ui.etDeleteWord.text()
        try: 
            file_.pop(wordToDeleted) 
            self.ui.lblWordDeleted.setText(f"{wordToDeleted} has been deleted.")
            self.ui.etDeleteWord.setText("")
            self.ui.btnSave.setEnabled(True)
        except KeyError:
            self.ui.lblWordDeleted.setText(f"The word {wordToDeleted} doesn't already exist in your file.")
            self.ui.etDeleteWord.setText("")
        if len(file_) == 0:
            self.ui.btnSave.setEnabled(False)
            self.ui.btnAsk.setEnabled(False)
            self.ui.btnCheck.setEnabled(False)
            self.ui.btnFinish.setEnabled(False)
            self.ui.btnDelete.setEnabled(False)
            self.ui.rbWordDefinition.setEnabled(False)
            self.ui.rbDefinitionWord.setEnabled(False)
        return file_

    def addWord(self,file_):
        WordToAdd = self.ui.etAddWord.text()
        definitionToAdd = self.ui.etAddDefinition.text()
        if len(WordToAdd) == 0 or len(definitionToAdd) == 0:
            self.ui.lblWordAdded.setText("You cannot add a space. Please enter a word and its meaning.")
        else:
            file_[WordToAdd] = definitionToAdd
            self.ui.lblWordAdded.setText(f"{WordToAdd} has been added.")
            self.ui.etAddWord.setText("")
            self.ui.etAddDefinition.setText("")
            self.ui.btnAsk.setEnabled(True)
            tempFile.update(file_)
        if len(file_) > 0:
            self.ui.btnDelete.setEnabled(True)
            self.ui.btnSave.setEnabled(True)
            self.ui.rbWordDefinition.setEnabled(True)
            self.ui.rbDefinitionWord.setEnabled(True)
        return file_
    
    def onClickedFinish(self):
        self.ui.lblResult.setText(f"{self.true} true, {self.false} false")
        self.ui.btnCheck.setEnabled(False)
        self.ui.rbWordDefinition.setEnabled(True)
        self.ui.rbDefinitionWord.setEnabled(True)

    def onClickedBrowse(self):
        filen = QFileDialog.getOpenFileName()
        path = filen[0]
        fileName2 = path.split("/")
        global file_
        global tempFile
        tempFile = {}
        with open(path, encoding= "utf-8") as f:
            file_ = json.load(f)
            self.ui.lblBrowseRead.setText(f"{fileName2[-1]} has been read.")
            self.ui.etFilneName.setText(fileName2[-1])
        tempFile.update(file_)
        if len(file_) > 0:
            self.ui.btnDelete.setEnabled(True)
        self.ui.btnAsk.setEnabled(True)
        self.ui.btnAdd.setEnabled(True)
        self.ui.rbWordDefinition.setEnabled(True)
        self.ui.rbDefinitionWord.setEnabled(True)
        self.ui.btnBrowse.setEnabled(False)
        self.ui.btnCreate.setEnabled(False)

    def onClickedOrientation(self):
        if self.ui.rbWordDefinition.isChecked():
            self.group.setExclusive(True)        
            self.ui.btnAsk.clicked.connect(self.onClickedAsk)
        elif self.ui.rbDefinitionWord.isChecked():
            self.group.setExclusive(True)        
            self.ui.btnAsk.clicked.connect(self.onClickedAsk2)

    def onClickedAsk(self):
        self.ui.wordInput.clear()
        global key,val
        key, val = random.choice(list(tempFile.items()))
        self.ui.lblAnswer.setText(" ")
        self.ui.lblQuestionWord.setText(key)
        self.ui.btnCheck.setEnabled(True)
        self.ui.btnFinish.setEnabled(True)
        self.ui.rbDefinitionWord.setEnabled(False)
        return key, val
        
    def onClickedAsk2(self):
        self.ui.wordInput.clear()
        global key,val
        key, val = random.choice(list(tempFile.items()))
        self.ui.lblAnswer.setText(" ")
        self.ui.lblQuestionWord.setText(val)
        self.ui.btnCheck.setEnabled(True)
        self.ui.btnFinish.setEnabled(True)
        self.ui.rbWordDefinition.setEnabled(False)
        return key, val

    def onClickedCheck(self,key,val):
        reply = self.ui.wordInput.text()
        self.ui.btnCheck.setEnabled(False)
        
        if self.ui.rbWordDefinition.isChecked():
            if reply == val:
                self.ui.lblAnswer.setText("Right")
                self.true += 1
                try:
                    tempFile.pop(key)
                except KeyError:
                    pass
            else:
                self.ui.lblAnswer.setText(f"Wrong.  The answer is {val}.")
                self.false += 1
        elif self.ui.rbDefinitionWord.isChecked():
            if reply == key:
                self.ui.lblAnswer.setText("Right")
                self.true += 1
                try:
                    tempFile.pop(key)
                except KeyError:
                    pass
            else:
                self.ui.lblAnswer.setText(f"Wrong. The answer is {key}.")
                self.false += 1

        if len(tempFile) == 0:
            self.ui.btnAsk.setEnabled(False)
            self.ui.btnCheck.setEnabled(False)
            self.ui.lblResult.setText(f"You used all the words.{self.true} true, {self.false} false")

def flashCard():
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())
flashCard()
